# wechat-mac-export

Cursor Agent Skill：在 **macOS** 上导出**本人**微信 4.x 本地聊天记录的操作说明。

> **先读 [DISCLAIMER.md](DISCLAIMER.md)。** 非官方、仅限自有账号与设备、可能违反平台协议、风险自负。

## 安装到 Cursor

```bash
git clone https://github.com/lnuxe/wechat-mac-export.git ~/.cursor/skills/wechat-mac-export
```

或把本仓库内容复制到 `~/.cursor/skills/wechat-mac-export/`（需包含 `SKILL.md`）。

## 核心路径（摘要）

WeChat **4.1.10+** 本地库为 SQLCipher 加密；内存扫密钥（如部分工具的 `keys`）常得到 **0 keys（属预期）**。

已验证思路：

1. [wcdb-key-tool](https://github.com/TANGandXUE/wcdb-key-tool)（LLDB 抓 passphrase → PBKDF2）解密本机库  
2. [WxEcho](https://github.com/chang-xinhai/WxEcho) / `@walkerch/wxecho` 按联系人导出 `chat.txt`

详情见 [SKILL.md](SKILL.md)。故障见 [troubleshooting.md](troubleshooting.md)。

## 不要提交什么

切勿把以下内容推送到任何公开仓库：

- `wechat-passphrase.json` / 密钥文件  
- 解密后的 `*.db`  
- 导出的 `chat.txt` / `chat.json`  

本仓库 `.gitignore` 已覆盖常见敏感名。

## License

[MIT](LICENSE)。第三方工具（WxEcho、wcdb-key-tool 等）各有其许可证，请自行遵守。
