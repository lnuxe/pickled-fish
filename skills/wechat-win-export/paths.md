# 路径与产物格式（Windows）

> 账号目录因人而异；以本机 `xwechat_files/wxid_*`（4.x）或 `WeChat Files/wxid_*`（3.x）为准。勿把真实 wxid、聊天内容写入公开仓库。

## 常见路径

| 项 | 路径 |
|----|------|
| PyWxDump CLI | `wxdump`（`pip install pywxdump`） |
| 微信 4.x 数据根 | `%USERPROFILE%\Documents\xwechat_files\<wxid_xxx>\` |
| 微信 4.x 主聊天库 | `...\xwechat_files\<wxid_xxx>\db_storage\message\message_0.db` |
| 微信 3.x 数据根 | `%USERPROFILE%\Documents\WeChat Files\<wxid_xxx>\` |
| 微信 3.x 主聊天库 | `...\WeChat Files\<wxid_xxx>\Msg\MSG0.db` |
| PyWxDump 解密输出 | 以 `wxdump decrypt -h` / 工具配置为准，常见 `app_data\decrypt\` |
| 本 skill 规范化脚本 | `skills\wechat-win-export\scripts\export_chat.py` |

## chat.txt 行格式（规范化后，与 macOS 流程一致）

```
[2026-01-01 12:00:00] 系统: ...
[2026-01-01 12:00:01] 对方昵称: 你好
[2026-01-01 12:00:02] 我: 你好
```

解析正则（参考）：

```
^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (我|[^:]+|系统): (.*)$
```

## PyWxDump CSV 常见列

| 列 | 含义 |
|----|------|
| `localId` | 本地消息序号 |
| `TalkerId` | 会话对象 wxid（群或好友） |
| `Type` / `SubType` | 消息类型（1 文本 / 3 图片 / 34 语音 / 43 视频 / 47 表情 / 49 应用消息 / 10000 系统） |
| `IsSender` | 1 = 自己发出，0 = 对方 |
| `CreateTime` | Unix 时间戳（秒或毫秒） |
| `StrContent` | 消息内容（非文本消息常为 XML） |
| `StrTime` | 格式化时间串（各版本格式不一，脚本优先用 `CreateTime`） |
| `Remark` / `NickName` / `Sender` | 备注 / 昵称 / 实际发送者（群聊时区分成员） |

> 列名与顺序随 PyWxDump 版本变化；`export_chat.py` 按表头读取，缺列会报错提示，不会静默错位。

## 能力边界

| 平台 | 本流程 |
|------|--------|
| Windows 微信 4.x | 适用（随版本可能失效，走 PyWxDump 当前版本） |
| Windows 微信 3.x | 适用 |
| macOS 桌面微信 4.x | 不适用 → 见 `../wechat-mac-export/` |
| iOS / Android | 不适用 |
| 未登录 / 无本地库 | 不适用 → 截图 / 粘贴 |
