---
name: wechat-mac-export
description: >-
  Export macOS WeChat 4.x local chat records via wcdb-key-tool decrypt + WxEcho
  export. Use when the user asks to read WeChat chats, decrypt db_storage,
  export a contact's messages, find 聊天记录, run wechat-export, or mentions
  wcdb / wxecho / SQLCipher / 微信解密 on Mac.
---

# macOS 微信聊天记录导出

> **免责声明**：仅限导出**你本人账号、你控制的 Mac**上的本地数据。可能违反微信用户协议。完整条款见仓库根目录 [DISCLAIMER.md](../../DISCLAIMER.md)。使用即表示同意。

导出完成后若需关系分析，读取同仓库 [../qingsheng/SKILL.md](../qingsheng/SKILL.md) 与 [../qingsheng/references/local-chat-pipeline.md](../qingsheng/references/local-chat-pipeline.md)，或根目录总控 [../../SKILL.md](../../SKILL.md)。

**仅 macOS。** WeChat 4.1.10+ 的 `db_storage/*.db` 均为 SQLCipher 加密；**部分工具的内存扫密钥对 4.1.10+ 无效（0 keys 属正常）**。验证通过路径：

```
wcdb-key-tool（LLDB 抓 passphrase → PBKDF2）→ 明文 SQLite
  → 指向导出工具的 decrypted_dir → 按联系人导出
```

聊天数据极敏感：只在用户本机操作，默认不上传；切勿将密钥或导出文件提交到 git / 上传公网。

---

## 何时用本 skill

- 用户要导出某人微信聊天 / 找本地聊天记录
- 解密失败、`0 keys`、`export` 找不到库

**不要用**：iOS/Android 手机库解密（本流程不支持）；用户只要截图/粘贴分析时，不必走解密。

**不要协助**：未经授权访问他人设备或账号。

---

## 快速路径（已有 passphrase + 解密库）

若存在 `~/.wcdb-key-tool/wechat-passphrase.json` 且 `~/wechat-decrypted/` 可用：

```bash
wxecho export "联系人昵称或备注"
```

输出通常在：`~/Downloads/wxecho/<联系人>/chat.txt`（及 json/csv，视工具版本而定）。

---

## 完整流程（首次 / 微信更新后）

### 0. 依赖

| 工具 | 安装 |
|------|------|
| WxEcho | `npm install -g @walkerch/wxecho` |
| wcdb-key-tool | `git clone --depth 1 https://github.com/TANGandXUE/wcdb-key-tool.git /tmp/wcdb-key-tool` |
| Python 3 | 系统自带即可 |

### 1. 定位账号 `db_storage`

```bash
ls -lt ~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/*/db_storage/message/message_0.db
```

选**数据量大、mtime 最新**的账号目录（多账号时勿选空库/临时号）。

典型结构：

```
.../xwechat_files/<wxid_xxx>/db_storage/
  contact/contact.db
  session/session.db
  message/message_0.db   # 主聊天库
```

### 2. 重签名微信（微信更新后必做）

```bash
sudo codesign --force --deep --sign - /Applications/WeChat.app
```

然后 **Cmd+Q 完全退出**微信。

### 3. 抓 passphrase + 解密（推荐）

在**系统终端**跑（需交互登录；自动化 Agent 通常无法代输密码/扫码）：

```bash
sudo python3 /tmp/wcdb-key-tool/wcdb_key_tool_macos.py extract --decrypt \
  --db-dir ~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/<主账号wxid>/db_storage
```

脚本会重启微信 → 用户扫码/登录 → LLDB 捕获 passphrase → 派生密钥 → 解密。

成功标志：

- `~/.wcdb-key-tool/wechat-passphrase.json` 存在
- 解密库出现（常见 `~/decrypted/`，可能属 root）

### 4. 修正权限与路径

```bash
# 拷到用户可写目录（推荐）
rm -rf ~/wechat-decrypted
sudo cp -R ~/decrypted ~/wechat-decrypted
sudo chown -R "$(whoami)" ~/wechat-decrypted
```

把导出工具配置中的 `decrypted_dir` 指到此处（编辑对应 `config.json`）。

### 5. 导出联系人

```bash
# ✅ 位置参数（以当前 WxEcho CLI 为准）
wxecho export "联系人昵称或备注"

# ❌ 常见错误（旧文档）
# wxecho export -n "联系人昵称或备注"
```

或直接调用其 Python 脚本（路径随 npm 全局安装位置变化）：

```bash
python3 "$(npm root -g)/@walkerch/wxecho/py/export_chat.py" -n "联系人昵称或备注"
```

产物示例：`~/Downloads/wxecho/<昵称>/chat.txt`

### 6. 交给下游

将 `chat.txt` 交给同仓库 **qingsheng + local-chat-pipeline**（或用户指定的本地解析器）；**不要默认上传云端**。

---

## Agent 操作纪律

1. **首次 extract 需用户在本机终端完成**（sudo + 重登）；Agent 只给命令、检查产物路径。
2. 多账号时先用 `du -sh` / `ls -lt message_0.db` 选主号，再解密。
3. 解密库若 `permission denied`：先 copy 到 `~/wechat-decrypted` 或 `/tmp/wechat-decrypted`，再查 sqlite。
4. **不要**建议关闭 SIP 仅为跑其他 key-scan 工具（本流程不需要关 SIP）。
5. **不要**默认走内存扫密钥（4.1.10+ → 0 keys）。
6. **不要**把 passphrase、解密库、导出聊天写入仓库或发给第三方。

---

## 验证清单

```
- [ ] WeChat 已重签名且当前账号已登录过一次（有 passphrase）
- [ ] ~/wechat-decrypted/contact/contact.db 可读
- [ ] sqlite3 能搜到目标昵称
- [ ] export 产出 chat.txt
- [ ] chat.txt 行格式大致为: [YYYY-MM-DD HH:MM:SS] 我|对方: ...
```

快速抽查联系人：

```bash
sqlite3 ~/wechat-decrypted/contact/contact.db \
  "SELECT username, nick_name, remark FROM contact
   WHERE nick_name LIKE '%关键词%' OR remark LIKE '%关键词%' LIMIT 10;"
```

---

## 补充资料

- 故障排查见 [troubleshooting.md](troubleshooting.md)
- 路径与格式见 [paths.md](paths.md)
- 法律与协议风险见 [DISCLAIMER.md](DISCLAIMER.md)
