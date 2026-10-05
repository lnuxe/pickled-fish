---
name: wechat-win-export
description: >-
  Export Windows WeChat (3.x / 4.x) local chat records via PyWxDump decrypt +
  export, then normalize to chat.txt for pickled-fish's local-chat pipeline.
  Use when the user asks to read WeChat chats on Windows, decrypt db_storage /
  WeChat Files, export a contact's messages, find 聊天记录, or mentions
  PyWxDump / wxdump / SQLCipher / 微信解密 on Windows.
---

# Windows 微信聊天记录导出

> **免责声明**：仅限导出**你本人账号、你控制的 Windows 机器**上的本地数据。可能违反微信用户协议。完整条款见仓库根目录 [DISCLAIMER.md](../../DISCLAIMER.md)。使用即表示同意。

导出完成后若需关系分析，读取同仓库 [../qingsheng/SKILL.md](../qingsheng/SKILL.md) 与 [../qingsheng/references/local-chat-pipeline.md](../qingsheng/references/local-chat-pipeline.md)，或根目录总控 [../../SKILL.md](../../SKILL.md)。

**仅 Windows。** 对应 macOS 流程见 [../wechat-mac-export/SKILL.md](../wechat-mac-export/SKILL.md)。Windows 微信 3.x 与 4.x 的库均为 SQLCipher 加密，本流程用 **PyWxDump**（Windows 生态里 `wcdb-key-tool + wxecho` 的等价物）：

```
PyWxDump（读进程取 key → 解密 db）→ wxdump export（CSV）
  → scripts/export_chat.py（规范化）→ chat.txt
```

聊天数据极敏感：只在用户本机操作，默认不上传；切勿将密钥或导出文件提交到 git / 上传公网。

---

## 何时用本 skill

- 用户要在 **Windows** 上导出某人微信聊天 / 找本地聊天记录
- 解密失败、`key` 拿不到、`export` 找不到库
- 用户已有 PyWxDump 导出的 CSV，想变成下游可读的 `chat.txt`

**不要用**：iOS/Android 手机库解密（本流程不支持）；macOS 导出走 `wechat-mac-export`；用户只要截图/粘贴分析时，不必走解密。

**不要协助**：未经授权访问他人设备或账号。

---

## 依赖

| 工具 | 安装 |
|------|------|
| Python 3.10+ | https://www.python.org/（勾选 "Add to PATH"） |
| PyWxDump | `pip install pywxdump`（或 `pip install --upgrade pywxdump`） |
| 本 skill 脚本 | `skills/wechat-win-export/scripts/export_chat.py` |

> PyWxDump 主仓：[xaoyaoo/PyWxDump](https://github.com/xaoyaoo/PyWxDump)。CLI 子命令随版本变化，**以本机 `wxdump <子命令> -h` 与仓库 README 为准**；下面给的是当前主流用法，遇到差异先跑 `--help`。

---

## 完整流程（首次 / 微信更新后）

### 1. 定位账号数据目录

先确认微信版本，再定位：

**微信 4.x（新架构）：**

```powershell
# 主账号目录：体积大、mtime 最新的那个 wxid_*
Get-ChildItem "$env:USERPROFILE\Documents\xwechat_files" -Directory |
  Select-Object Name, LastWriteTime
# 主聊天库
Get-Item "$env:USERPROFILE\Documents\xwechat_files\<wxid_xxx>\db_storage\message\message_0.db"
```

典型结构：

```
...\xwechat_files\<wxid_xxx>\db_storage\
  contact\contact.db
  session\session.db
  message\message_0.db   # 主聊天库（量大时还有 message_1.db …）
```

**微信 3.x（旧架构）：**

```powershell
Get-ChildItem "$env:USERPROFILE\Documents\WeChat Files" -Directory |
  Select-Object Name, LastWriteTime
Get-Item "$env:USERPROFILE\Documents\WeChat Files\<wxid_xxx>\Msg\MSG0.db"
```

典型结构：

```
...\WeChat Files\<wxid_xxx>\Msg\
  MSG0.db          # 最近聊天
  MicroMsg.db      # 联系人等
  Multi\MSG*.db    # 历史分库
```

### 2. 确保微信已登录且在运行

PyWxDump 需要从**运行中的微信进程**里取密钥：先正常登录微信并保持打开，再往下走。

### 3. 取密钥 + 解密（推荐一键）

```powershell
# 一键：获取信息 + 密钥 + 解密到输出目录（以本机 --help 为准）
wxdump all

# 或分步（便于排查）：
wxdump info            # 查看版本 / wxid / key 等
wxdump decrypt         # 解密数据库到输出目录
```

- 部分版本在 4.x 上取 key 需要**管理员权限**：用「以管理员身份运行」的 PowerShell 再跑。
- 成功标志：输出里出现 `wxid_*` 与密钥；解密库出现在输出目录（常见为 `app_data\decrypt\` 或工具配置的 `out` 目录，见 `wxdump decrypt -h`）。

### 4. 导出目标联系人的聊天为 CSV

```powershell
# 优先用 UI（最稳）：wxdump ui → 选择账号 → 选择会话 → 导出 CSV
wxdump ui

# 或 CLI 导出（参数以 wxdump export -h 为准）
wxdump export --help
```

导出的 CSV 一般包含这些列（列名/顺序随版本不同）：

```
localId, TalkerId, Type, SubType, IsSender, CreateTime, Status,
StrContent, StrTime, Remark, NickName, Sender
```

### 5. 规范化成 chat.txt

```powershell
python scripts\export_chat.py --csv "导出的.csv" --out "chat.txt"
```

（`--out` 省略时，在 CSV 同目录生成 `chat.txt`。）

产物行格式（与 macOS 流程、下游管线一致）：

```
[2026-01-01 12:00:00] 我: 你好
[2026-01-01 12:00:01] 对方昵称: 你好
```

脚本会：按时间排序 → `IsSender=1` 标为「我」，否则取备注/昵称 → 纯文本直接写，图片/语音/视频/文件等非文本消息写成 `[图片]`、`[语音]`、`[文件: xxx]` 这类占位符。

### 6. 交给下游

将 `chat.txt` 交给同仓库 **qingsheng + local-chat-pipeline**（或用户指定的本地解析器）；**不要默认上传云端**。

---

## 快速路径（已有解密库 / 已导出 CSV）

- 已有 PyWxDump 的 CSV → 直接跑第 5 步的 `export_chat.py`。
- 已有解密库、想直接查联系人 → 用 `wxdump dbshow` 或 sqlite 查 `contact.db`：

```powershell
# 解密后的 contact.db 路径以 wxdump dbshow 输出为准
sqlite3 "<解密目录>\contact\contact.db" "SELECT username, nick_name, remark FROM contact WHERE nick_name LIKE '%关键词%' OR remark LIKE '%关键词%' LIMIT 10;"
```

---

## Agent 操作纪律

1. **首次取 key 可能需用户在本机完成**（管理员权限 + 登录态）；Agent 只给命令、检查产物路径。
2. 多账号时用「目录体积 + mtime」选主号（见第 1 步），再解密。
3. 解密库若 `permission denied`：先复制到用户可写目录（如 `%USERPROFILE%\wechat-decrypted`）再查 sqlite。
4. **不要**为了取 key 建议关闭杀软 / 内核隔离 / UAC；优先 PyWxDump 官方支持的路径。
5. **不要**默认走「内存扫密钥」类脚本兜底；4.x 请走 PyWxDump 当前版本支持的取 key 方式。
6. **不要**把 passphrase、解密库、导出聊天写入仓库或发给第三方。

---

## 验证清单

```
- [ ] 微信已登录且进程在运行
- [ ] wxdump info 能看到 wxid 与 key
- [ ] 解密目录下 contact/contact.db、message/message_0.db 可读
- [ ] wxdump export 产出目标会话 CSV
- [ ] export_chat.py 产出 chat.txt
- [ ] chat.txt 行格式大致为: [YYYY-MM-DD HH:MM:SS] 我|对方: ...
```

---

## 补充资料

- 路径与格式见 [paths.md](paths.md)
- 故障排查见 [troubleshooting.md](troubleshooting.md)
- 法律与协议风险见 [DISCLAIMER.md](../../DISCLAIMER.md)
