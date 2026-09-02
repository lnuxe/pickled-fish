# 路径与产物格式

> 账号目录因人而异；以本机 `xwechat_files/wxid_*` 为准。勿把真实 wxid、聊天内容写入公开仓库。

## 常见路径

| 项 | 路径 |
|----|------|
| WxEcho CLI | `wxecho`（`npm i -g @walkerch/wxecho`） |
| WxEcho py | `$(npm root -g)/@walkerch/wxecho/py/` |
| wcdb-key-tool | 自行 clone，例如 `/tmp/wcdb-key-tool/wcdb_key_tool_macos.py` |
| passphrase 缓存 | `~/.wcdb-key-tool/wechat-passphrase.json` |
| 推荐解密目录 | `~/wechat-decrypted/` |
| 常见 root 解密目录 | `~/decrypted/` |
| 导出根目录 | `~/Downloads/wxecho/<联系人>/` |

## chat.txt 行格式（示例）

```
[2026-01-01 12:00:00] 系统: ...
[2026-01-01 12:00:01] 对方昵称: 你好
[2026-01-01 12:00:02] 我: 你好
```

解析正则（参考）：

```
^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (我|[^:]+|系统): (.*)$
```

## 消息表定位（高级）

联系人 `username`（形如 `wxid_…`）→ 表名：

```
Msg_ + md5(username)
```

在 `~/wechat-decrypted/message/message_0.db` 中查询。一般优先用官方文档/工具的 export，不必手写 SQL。

## 能力边界

| 平台 | 本流程 |
|------|--------|
| macOS 桌面微信 4.x | 适用（随版本可能失效） |
| Windows 微信 | 不适用 |
| iOS / Android | 不适用 |
| 未登录 / 无本地库 | 不适用 → 截图 / 粘贴 |
