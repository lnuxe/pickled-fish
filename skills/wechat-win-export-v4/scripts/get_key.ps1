# 取密钥（Windows 微信 4.x）

微信 4.x 的 `SetDBKey` **只在进程启动时调用一次**，登录/退出登录都不会触发。
所以取密钥的时机是固定的：**关微信 → 工具启动微信 → 立即 hook → 等登录**。

## 为什么必须用 hook

| 方法 | 结果 |
|------|------|
| PyWxDump 3.1.46 | ❌ 写死 `WeChat.exe`，4.x 是 `Weixin.exe` |
| 扫内存 `x'<64hex>'` | ❌ 4.1.11+ 只存 passphrase，不存 raw key |
| 自己 hook KDF 配置函数 | ❌ 配置阶段抓不到，密钥只在执行瞬间存在 |
| hook `SetDBKey` | ✅ 有效 |

自研 Frida 路线在 4.1.15.13 上实测**全部失败**（`MMV1` 字符串引用落在异常处理
包装函数、社区偏移 `0x3486140` 落在函数中间、`sqlite3_*` 符号被剥离、
pragma 名表只有 `lea` 无指针表）。**不要重复这些尝试。**

## 推荐做法

用 [Ray0612/WeChat-Export-Tool](https://github.com/Ray0612/WeChat-Export-Tool)
的 `wx_key.dll`（MIT 组件）。注意：该工具**捆绑的 WCDB 解密服务在 4.1.15.13 上会
`INIT_FAIL` / 启动超时**，但**密钥提取是可用的** —— 取到密钥后用本 skill 的
`decrypt_wechat4.py` 自行解密即可。

### 步骤

1. 下载 release（约 240MB），解压
2. 运行 `WeChatExport.exe`
3. **微信数据目录**填 `xwechat_files` 所在目录（注意数据目录可能不在默认位置，
   例如装在 D 盘）
4. 点「**获取密钥**」→ 按提示**关闭微信** → 工具自动启动微信并注入 hook
5. 在微信点登录
6. 密钥写入 `%USERPROFILE%\Desktop\wx_export\key.txt`（64 位 hex）
   同时 `key_status.txt` 里是 `captured`

### 密钥是持久的

实测：微信重启后数据库 salt 不变、**同一把密钥仍可解密**。
所以只需要提取一次，之后直接复用。

## 用 PowerShell 直接驱动（可选）

```powershell
# 若已装 Node.js，可直接调用其脚本（工具自带）
cd <解压目录>\WeChatExport\scripts
node get_key.js
# 输出：%USERPROFILE%\Desktop\wx_export\key.txt
```

## 完成后

```powershell
python scripts/decrypt_wechat4.py --key <64位hex> `
  --db "<db_storage>\message\message_0.db" --out "message_0.dec"
```

若 `schema: readable`，说明密钥与参数都对。
