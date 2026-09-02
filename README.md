# mac-wechat-coach

Cursor Agent Skills 组合包：**本机导出 macOS 微信聊天** + **中文情感关系分析（情圣知识库）**。

> **先读 [DISCLAIMER.md](DISCLAIMER.md)。** 非官方 · 仅限本人账号/设备 · 可能违反微信协议 · 情感建议非专业咨询 · 风险自负。

## 仓库里有什么

| 路径 | 作用 |
|------|------|
| [SKILL.md](SKILL.md) | **总控 skill**：导出 → 解析 → 分析的一站式流程 |
| [skills/wechat-mac-export/](skills/wechat-mac-export/) | macOS 微信 4.x 本地库解密与导出 |
| [skills/qingsheng/](skills/qingsheng/) | 情圣恋爱教练知识库（源自 [tomwong001/qingsheng-skill](https://github.com/tomwong001/qingsheng-skill)，MIT） |
| [skills/qingsheng/references/local-chat-pipeline.md](skills/qingsheng/references/local-chat-pipeline.md) | **本仓新增**：整段 `chat.txt` 本地分析管线 |

## 安装

### 推荐：整仓装为一个 skill

```bash
git clone https://github.com/lnuxe/mac-wechat-coach.git ~/.cursor/skills/mac-wechat-coach
```

### 或拆成两个 skill（便于单独触发）

```bash
REPO=~/.cursor/skills/mac-wechat-coach
git clone https://github.com/lnuxe/mac-wechat-coach.git "$REPO"
ln -sfn "$REPO/skills/wechat-mac-export" ~/.cursor/skills/wechat-mac-export
ln -sfn "$REPO/skills/qingsheng" ~/.cursor/skills/qingsheng
```

也可运行：

```bash
bash scripts/install-skills.sh
```

## 典型用法

1. 「帮我导出和某某的微信聊天」→ 走 `wechat-mac-export`  
2. 「根据这份 chat.txt / 聊天记录分析关系、怎么回、要不要挽回」→ 走 `qingsheng` + `local-chat-pipeline`  
3. 「导出并分析」→ 走根目录总控 [SKILL.md](SKILL.md)

## 不要提交什么

- passphrase / 密钥、解密 `*.db`、导出的 `chat.txt` / `chat.json`  
- 真实联系人档案、截图里的隐私信息  

见 `.gitignore`。

## 致谢与许可

- 微信导出流程与总控编排：本仓库，[MIT](LICENSE)（Copyright lnuxe）  
- 情圣知识库：© tomwong001 and qingsheng-skill contributors，[MIT](skills/qingsheng/LICENSE) — 详见 [NOTICE](NOTICE)  
- 解密依赖第三方：[wcdb-key-tool](https://github.com/TANGandXUE/wcdb-key-tool)、[WxEcho](https://github.com/chang-xinhai/WxEcho)（各从其许可证）
