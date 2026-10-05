---
name: wechat-win-export-v4
description: >-
  Windows 微信 4.1+ 聊天记录导出（PyWxDump 在 4.x 上已失效）。用 wx_key.dll hook
  SetDBKey 取密钥，再用 SQLCipher 参数解密 db_storage，定位会话表并导出 chat.txt。
  Use for 微信4.x导出, 聊天记录解密, db_storage, message_0.db, 消息表, 微信密钥,
  4.1.15, chat.txt, or when PyWxDump reports WeChat No Run.
---

# Windows 微信 4.1+ 聊天记录导出（实测可用流程）

> **免责声明**：仅限导出**你本人账号、你控制的机器**上的本地数据。聊天数据极敏感：
> 只在本机处理，不上传、不提交 git、不发给第三方。完整条款见仓库根
> [DISCLAIMER.md](../../DISCLAIMER.md)。

本 skill 是 [wechat-win-export](../wechat-win-export/SKILL.md) 在 **微信 4.1+** 上的替代路线。
实测环境：**Windows 11 + 微信 4.1.15.13，23/23 数据库全部解密成功，导出 4739 条消息**。

## 为什么不能用 PyWxDump / 内存扫 key

| 方法 | 在 4.1.15.13 上的结果 |
|------|----------------------|
| PyWxDump 3.1.46（PyPI 最新） | ❌ 源码写死 `if name == "WeChat.exe"`，4.x 进程名是 `Weixin.exe`，永远 `WeChat No Run` |
| 扫内存找 `x'<64hex>'` | ❌ 4.1.11+ 内存只存 passphrase、不存 raw key，整类工具失效 |
| 社区 4.1.12 的偏移方案 | ❌ `0x3486140` 在 4.1.15.13 上落在**函数中间**，不是入口 |
| 自己 hook KDF 配置函数 | ❌ 配置阶段抓不到；密钥只在 KDF 执行瞬间存在 |
| **`wx_key.dll` hook `SetDBKey`** | ✅ **有效**（见下） |

**关键事实**：微信 4.x 的 `SetDBKey` **只在进程启动时调用一次**，登录/退出登录不会触发。
所以取密钥必须"关微信 → 工具启动微信 → 立即 hook → 等登录"。

## 完整流程

### 1. 取密钥（唯一可靠的公开途径）

用 [Ray0612/WeChat-Export-Tool](https://github.com/Ray0612/WeChat-Export-Tool) 的
`wx_key.dll`（其 GUI 的 WCDB 服务在本版本起不来，但**密钥提取可用**）：

1. 启动工具 → 填微信数据目录 → 点「获取密钥」
2. 按提示**关闭微信**，工具会自动启动微信并注入 hook
3. 在微信点登录，工具捕获密钥并写入：
   `%USERPROFILE%\Desktop\wx_export\key.txt`（64 位 hex）

> 密钥是**账号级持久化**的：重启微信后 salt 不变、同一把密钥仍可解密，
> 不必每次重新提取。

### 2. 解密（本 skill 的核心，参数已实测）

**用 `scripts/decrypt_freshest.py`，不要自己拼解密+WAL 合并**：

```powershell
python scripts/decrypt_freshest.py `
  --key <64位hex> `
  --db "<db_storage>\message\message_0.db" `
  --out "message_0.dec"
```

它会**同时**解出「只用主库」和「主库+全部 WAL 帧」两份，比较各自的
**最新消息时间**与**消息总行数**，取更新的那份，并把被拒的那份及理由打印出来。
这一步是为坑 3 加的硬防护——**实测该防护成功识别并拒绝了会把数据倒退 6 天、
少 8570 行的 WAL 合并**。

单库解密与自检用 `scripts/decrypt_wechat4.py`（同样会跑页对齐/页头/抽样/schema 检查）。

**实测参数（4.1.15.13）：**

```
page_size   = 4096
reserve     = 80          # = IV(16) + HMAC(64)
IV 偏移      = 4016        # ★ 不是 4032！
页1 密文      = [16:4016]，明文 = SQLite magic + 解密体，必须补齐到 4096
页N 密文      = [0:4016]
KDF         = PBKDF2-HMAC-SHA512 × 256000, salt = 库文件头 16 字节
mac_salt    = salt XOR 0x3a
```

### 3. 定位会话表

**不要**假设表名是 `Msg_<MD5(wxid)>` —— 实测该哈希与 wxid 的 MD5 不吻合。
可靠做法：读 `contact.db` 的 `contact` 表拿到目标 `username`，
再在消息库里用 `Name2Id` 反查（见脚本 `scripts/find_conversation.py`）。

### 4. 导出 chat.txt

`scripts/export_chat4.py` 做发言人归属：`real_sender_id` 索引消息库的 `Name2Id`，
解析出的 username 等于**自己的 wxid** 就是「我」，等于对方 wxid 就是对方，
解析不到的（系统消息）单独标注。产物格式与下游 `local-chat-pipeline` 一致：

```
[2026-01-01 12:00:00] 我: 你好
[2026-01-01 12:00:01] 对方昵称: 你好
```

> **不要把真实聊天内容、真实昵称或 wxid 写进仓库**（包括文档示例）。
> 本 skill 的所有文档只使用占位符，`.gitignore` 已挡 `chat.txt`/`*.db`/密钥，
> 但**文档正文里的引用不会被挡**——提交前请自行搜一遍联系人名与 wxid。

## 五个踩过的坑（每一个都导致过错误结论）

### 坑 1：IV 偏移错 16 字节

`reserve=80` 时，**IV 在 4016、HMAC 在 4032-4096**。若按 HMAC 在前、IV 在后
（即 IV 取 4032）解密，**页 1 看起来仍然正常**（头部元数据自洽：`reserved_space=80`、
页数吻合、magic 正确），但**页 2 以后全是随机字节**。这种"页 1 正确、其余全错"
正是 IV 偏移错误的特征。

### 坑 2：页 1 未补齐 4096 字节 → 全文件错位

页 1 的密文只有 4000 字节（`[16:4016]`），加 16 字节 magic 后是 **4016 字节，不是 4096**。
若不补齐，从页 2 起每页错位 80 字节，整个文件不可读。
**自检信号**：文件大小 `% 4096 != 0`。

### 坑 3：把过期 WAL 帧覆盖到已更新的主库上（最隐蔽，已加硬防护）

微信运行期间 WAL 里既有**比主库新的**帧，也可能有 4MB 的**过期副本**。
无条件把全部 WAL 帧按页号覆盖主库，**会把新数据覆盖回旧状态**——
实测把一条到 `2026-10-06 01:48` 的会话倒退回了 `2026-09-30 19:03`，
凭空"丢失"了 749 条消息。**而且主库与 WAL 的 mtime 完全相同**，
所以无法靠时间戳判断该不该合并。

**防护（已实现在 `decrypt_freshest.py`）**：两条路径都跑，按
**最新消息时间 → 消息总行数** 依次比较，取更新的那份。
实测该判据有效：

```
[main-only       ] newest=2026-10-06 04:18:03 rows=155831   ← 选中
[wal-merged(1018f)] newest=2026-10-06 04:18:03 rows=147261   ← 拒绝（少 8570 行）
```

注意两者"最新时间"可能相同（别的活跃会话会拉高 max），
所以**行数是必要的第二判据**，不能只比时间。

### 坑 4：WAL salt 轮换 ≠ 结束

单个 WAL 文件里 salt 会**多次轮换**（每次重启写新 salt）。若遇到 salt 变化就
`break`，会丢掉绝大部分帧（实测 1018 帧只读到 51 帧）。

### 坑 5：用"HEADER 魔术字"当唯一判据

只检查解密结果开头是不是 `SQLite format 3\0` 会**误判**。必须用更硬的判据：
解析页头（b-tree 类型字节 + 页号自洽 + 单元格指针在界内），
最终以 **sqlite3 能否读出 schema** 为准。

## 验证清单

```
- [ ] key.txt 是 64 位 hex
- [ ] 解密后每个 .db 文件大小 % 4096 == 0
- [ ] 页 1 头：magic 正确、page_size=4096、reserved_space=80、db_size_pages == 实际页数
- [ ] 随机抽查页 N：首字节 ∈ {0x02,0x05,0x0a,0x0d}
- [ ] sqlite3 能 SELECT count(*) FROM sqlite_master
- [ ] 会话表的 max(create_time) 与微信界面里看到的最新消息**时间一致**（关键！）
```

最后一条是**唯一能证伪"数据是否最新"的检查**：如果导出结果的最新时间早于你在
微信里看到的，说明读到了过期状态（多半是坑 3）。

## 附：macOS

macOS 微信 4.x 走 [../wechat-mac-export/](../wechat-mac-export/SKILL.md)
（`wcdb-key-tool` + `wxecho`）。

## 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/get_key.ps1` | 调用 wx_key.dll 取密钥（说明与前置步骤） |
| `scripts/decrypt_freshest.py` | **首选**：解密并自动择优（防坑 3），输出最新消息时间与行数 |
| `scripts/decrypt_wechat4.py` | 单库解密 + 完整自检（参数参考实现） |
| `scripts/find_conversation.py` | 由联系人名/wxid 定位消息表 |
| `scripts/export_chat4.py` | 导出 chat.txt（含发言人归属） |
