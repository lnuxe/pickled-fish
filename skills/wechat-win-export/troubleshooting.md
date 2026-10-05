# 故障排查（Windows）

> **微信 4.1+ 请先看 [../wechat-win-export-v4/SKILL.md](../wechat-win-export-v4/SKILL.md)。**
> 本文件下方的 PyWxDump 流程在微信 4.x 上**已确认不可用**（见「`wxdump` 报
> `WeChat No Run`」一节）。4.1.x 的可用路线：`wx_key.dll` hook `SetDBKey` 取密钥 →
> 用 v4 skill 的参数解密 `db_storage` → 导出 `chat.txt`。
> 实测环境 4.1.15.13，23/23 个数据库解密成功。

## `wxdump` 不是内部或外部命令

PyWxDump 未安装或 Python Scripts 目录不在 PATH。

```powershell
pip install --upgrade pywxdump
# 仍不行则用模块方式运行：
python -m pywxdump --help
```

## `wxdump info` 拿不到 key / 输出为空

1. 微信未登录或进程已退出 → 正常登录微信并保持运行，再跑。
2. 4.x 需要管理员权限取 key → 用「以管理员身份运行」的 PowerShell 重跑。
3. 版本过新导致 PyWxDump 尚未适配 → 升级 PyWxDump：`pip install --upgrade pywxdump`，并看其 README 是否声明支持当前微信版本。

## `wxdump` 报 `WeChat No Run`（Windows 微信 4.x 必现）

**这不是环境问题，是 PyWxDump 不支持 4.x。** 已在微信 4.1.15.13 上实测确认：

- PyWxDump 3.1.46（PyPI 最新）在 `wx_core/wx_info.py` 里按
  `if name == "WeChat.exe"` 找进程，而 4.x 的进程名是 **`Weixin.exe`**，
  所以永远匹配不上；进程明明在运行也会输出 `[-] WeChat No Run`。
- 升级无效：`pip index versions pywxdump` 最高就是 3.1.46。
- 即使绕过进程名，它也认不出 4.x 的库结构（`db_storage/message/message_0.db`，
  而非 3.x 的 `Msg/MSG0.db`）。

**结论：Windows 微信 4.x 不要走 PyWxDump**，改用下面的 Frida 路线或 UI/OCR 兜底。

## 微信 4.1.11+ 改了密钥派生，内存扫 key 整体失效

4.1.11 起 `x'<64位hex>'` 形式的密钥缓存**不再存在**，password 以二进制形式
藏在 codec 配置函数的参数里，必须再经过 KDF 才是加密密钥：

```
password(32B) --PBKDF2-HMAC-SHA512, 256000 轮, salt=库文件头16字节--> enc_key
mac_key = PBKDF2-HMAC-SHA512(enc_key, salt^0x3a, 2 轮)
第1页布局: [0:16]=salt [16:4016]=密文 [4016:4032]=IV [4032:4096]=HMAC-SHA512
校验: HMAC(mac_key, page1[16:4032] || pgno(4B,LE)) == page1[4032:4096]
```

因此**所有"扫内存找 `x'...'`"类工具（含 PyWxDump 的 4.x 分支）全部失效**。

### 4.1.15.13 上已验证失效的社区锚点

社区流传的 4.1.12 方案在 4.1.15.13 上**没有一个能复用**，别再照抄偏移：

| 锚点 | 4.1.15.13 实测结果 |
|------|-------------------|
| `MMV1` 字符串引用 | 只命中一个异常/日志包装函数（参数是 GCC typeinfo），不是 codec 函数 |
| 社区偏移 `0x3486140` | 落在函数**中间**（`0x03486130` 之后 16 字节处），不是函数入口 |
| `sqlite3_*` / WCDB 符号名 | 被完全剥离，全库搜不到任何 `sqlite3` 字符串 |
| SQLCipher pragma 名字表 | 用 `lea` 引用，**没有指针表**可顺藤摸瓜 |
| SHA-512 IV 常量 | 按小端存储，且被拆成内联立即数散在代码流里（相邻 IV 相隔 13/14 字节），说明有常量拆分混淆 |

### 可靠做法：按常量机器码定位 KDF，再 hook **执行点**

不要找字符串、不要用别人的偏移，改用常量编码定位：

```python
# 256000 = 0x3E800，在 x86-64 下的立即数编码是 00 E8 03 00
# 但 192MB 的 DLL 里 104 处出现中，只有 2 处是真正的指令编码，
# 必须用 capstone 解码上下文才能筛出来（否则会误把数据当代码）
```

4.1.15.13 实测结果：那 2 处同属一个函数，**RVA `0x05839480`**，
正是 codec 配置例程（函数序言 `41 57 41 56 41 55 41 54 56 57 55 53 48 83 ec 48`）：

```
mov edx, 0x3e800  -> call 0x1835695c0   # 设置加密 KDF 迭代数
mov ecx, 0x3e800  -> call 0x1835695a0   # 设置 HMAC KDF 迭代数
```

从子函数反汇编可读出 codec 上下文结构布局：

| 偏移 | 含义 | 依据 |
|------|------|------|
| `+0x04` | KDF 迭代数 | `mov [rcx+4], edx` |
| `+0x28` | 页数 | 由 `+0x14`/`+0x30` 算出后写入 |
| `+0x30` | page size | `mov [rcx+0x30], edx` |
| `+0x60` | codec 指针链 | `[[[rcx+0x60]+8]]+0x50]` |

**关键教训（踩过的坑）**：`0x05839480` 是**配置阶段**，那一刻 password
尚未写入或已被释放；把它的上下文按一级/二级指针 dump 后穷举
（实测 15,041 + 7,334 + 21,892 个候选，含 4 种 mac_salt 与 5 种 reserve
组合）**全部无命中**。密码与派生密钥只在 **KDF 执行的那一瞬间**存在于
寄存器/栈上。

所以要 hook 的是**内层 KDF 执行点**（`0x035695c0` 一类，
即 `mov [rcx+4], edx` 的参数写入点，或再往下的 PBKDF2 调用），
在密钥刚写入、尚未释放的时刻抓，并同时 dump 栈。**加深指针层级没有用，时机才是决定性的。**

### Frida spawn 的两个必踩坑

1. **必须在挂起状态下 `script.load()`，再 `device.resume()`。**
   先 `resume` 再 `load` 的话，等 hook 装好时微信早已打开数据库、
   密钥早已设置完毕，函数不再被调用 → 永远 `hits=0`。
2. **`Weixin.dll` 在 spawn 时尚未映射**，直接 `Interceptor.attach` 会报
   `access violation`。要在脚本里轮询 `Process.findModuleByName("Weixin.dll")`，
   并且用 `target.readByteArray(4)` 确认页已映射后再 attach。

另外：密钥设置发生在**登录之后**（登录前库不会打开），所以 hook 挂好后
需要用户手动点一次「进入微信」。

## 解密后 `permission denied` / 读不到库

解密输出可能落在受保护目录，或文件被占用。

1. 先看 `wxdump decrypt -h` 的默认输出目录，用 `wxdump dbshow` 确认产物。
2. 复制到用户可写目录再查：

```powershell
Copy-Item -Recurse -Force "<解密目录>" "$env:USERPROFILE\wechat-decrypted"
```

3. 微信运行中会占用源库，但解密是读副本/内存，一般不影响；若报锁，先完全退出微信再解密。

## `wxdump export` 找不到库 / 导出空

1. 先完成 `decrypt`，并确认解密目录里有 `contact\contact.db` 与 `message\message_0.db`。
2. 用 `wxdump dbshow` 列出解密库与账号，确认选的是主号。
3. 导出语法以本机 `wxdump export -h` 为准（CLI 随版本变化）；不确定就 `wxdump ui` 走界面。

## `export_chat.py` 报「缺少列」/ 输出乱码

1. CSV 列名与本 skill 记录的常见列不同 → 按实际表头修正脚本里的列映射，或升级 PyWxDump 到脚本适配的版本。
2. 乱码：确认 CSV 是 UTF-8（带/不带 BOM 均可）；脚本用 `utf-8-sig` 读，若源是 GBK 先转码：

```powershell
# 仅当源 CSV 确为 GBK 时
Get-Content -Encoding Default "in.csv" | Set-Content -Encoding UTF8 "in_utf8.csv"
```

## 导出到错账号

机器上可能有多个 `wxid_*`。以 `message_0.db`（4.x）/ `MSG0.db`（3.x）**体积 + mtime** 选主号：

```powershell
Get-ChildItem "$env:USERPROFILE\Documents\xwechat_files" -Directory |
  ForEach-Object {
    $db = Join-Path $_.FullName "db_storage\message\message_0.db"
    [PSCustomObject]@{ Wxid=$_.Name; DbMB= if(Test-Path $db){[math]::Round((Get-Item $db).Length/1MB,1)}else{0}; Mtime= if(Test-Path $db){(Get-Item $db).LastWriteTime}else{$null} }
  } | Format-Table -AutoSize
```

## 微信更新后再次失败

更新可能更换密钥派生方式或数据目录，旧解密库过期：

1. 升级 PyWxDump：`pip install --upgrade pywxdump`
2. 重新跑 `wxdump all`（或 `info` → `decrypt`）
3. 重新 `export` + `export_chat.py`
