---
name: mac-wechat-coach
description: >-
  End-to-end macOS WeChat local chat export plus Chinese relationship coaching
  (qingsheng knowledge base). Use when the user wants to decrypt/export WeChat
  chats on Mac, analyze a chat.txt or relationship, ask 怎么回/她什么意思/挽回,
  or run the local export→analyze pipeline (wcdb, wxecho, 情圣, 聊天记录).
---

# mac-wechat-coach · 导出 + 情感分析总控

> 完整免责声明：[DISCLAIMER.md](DISCLAIMER.md)。仅限本人数据；情感建议非专业咨询；禁止骚扰。

把两件事串成一条管线：

```
macOS 微信本地库 ──[wechat-mac-export]──► chat.txt
                                              │
                                              ▼
                                    [qingsheng + local-chat-pipeline]
                                              │
                                              ▼
                                    阶段/信号/挽回/可发送回复
```

## 子 skill 位置（按需 Read）

| 场景 | 读取 |
|------|------|
| 解密 / 导出 / 0 keys / 路径 | [skills/wechat-mac-export/SKILL.md](skills/wechat-mac-export/SKILL.md) |
| 导出错排 | [skills/wechat-mac-export/troubleshooting.md](skills/wechat-mac-export/troubleshooting.md) |
| 关系分析、怎么回、阶段、挽回 | [skills/qingsheng/SKILL.md](skills/qingsheng/SKILL.md) |
| **整段导出记录**分析（本仓增强） | [skills/qingsheng/references/local-chat-pipeline.md](skills/qingsheng/references/local-chat-pipeline.md) |
| 挽回专项 | [skills/qingsheng/references/recovery-playbook.md](skills/qingsheng/references/recovery-playbook.md) |
| 七阶段 | [skills/qingsheng/references/stages.md](skills/qingsheng/references/stages.md) |

情圣知识库上游：https://github.com/tomwong001/qingsheng-skill （MIT，见 [NOTICE](NOTICE)）

---

## 工作流 A：只要导出

1. 按 `wechat-mac-export` 完成 decrypt + `wxecho export "昵称"`  
2. 确认产物 `~/Downloads/wxecho/<昵称>/chat.txt`  
3. **不要**把文件提交到 git  

## 工作流 B：已有 chat.txt / 粘贴 / 截图

1. 加载 `qingsheng` 原则（短回复、1–2 关键点 + 1 追问）  
2. 若是**长导出文件**（数千行+），先读 `local-chat-pipeline.md` 做统计与时间线，再进入情圣分析  
3. 意图含挽回/冷战/拉黑 → `/挽回` + recovery-playbook  

## 工作流 C：导出并分析（默认总控）

```
Task Progress:
- [ ] 1. 确认平台=macOS 微信，联系人昵称/备注
- [ ] 2. 导出 chat.txt（wechat-mac-export）
- [ ] 3. 本地统计 + 崩盘/边界时间线（local-chat-pipeline）
- [ ] 4. 情圣分析：阶段 / 信号 / 该不该回
- [ ] 5. 若需挽回：可能性 + 冷静期 + 一条可发送消息（或明确「先不联系」）
- [ ] 6. 提醒：密钥与 chat.txt 勿上传
```

### 分析输出约束（总控层强制）

- 一次给 **1–2 个关键点**，不要长篇报告堆砌  
- 涉及对方明确拒绝 / 报警 / 要求停止 → **优先安全边界**：停止联系建议优先于话术  
- 可发送消息必须是**可直接复制的短句**；事务收尾（快递/退款）与情感挽回**分开**  
- 禁止教用户 stalking、换号轰炸、未经同意上门  

---

## Agent 纪律

1. 首次微信 `extract` 需用户本机终端交互；Agent 只给命令与验路径。  
2. 先导出再分析时，用文件路径或抽样，避免一次把数万行全文塞进上下文；用脚本统计 + 关键片段。  
3. 不把真实 chat / passphrase 写入仓库。  
4. 子 skill 冲突时：安全边界 > 挽回话术；本机导出技术细节以 `wechat-mac-export` 为准。  
