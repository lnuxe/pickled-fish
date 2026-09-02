---
name: pickled-fish
description: >-
  macOS WeChat local export plus pluggable relationship knowledge packs and
  filesystem RAG orchestration (qingsheng, dating-master, lovelab, custom KBs).
  Use for WeChat decrypt/export, chat.txt analysis, 怎么回/挽回, 知识库/RAG/自定义包,
  or switching coaching frameworks (Gottman, attachment, signaling).
---

# pickled-fish · 导出 + 可插拔知识库

> [DISCLAIMER.md](DISCLAIMER.md) · 仅限本人数据 · 情感建议非专业咨询 · 禁止骚扰

```
微信本地库 ──wechat-export──► chat.txt
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
              local-chat 统计              kb-rag 选 pack
                    │                         │
                    └──────────► 分析 ◄───────┘
                         (qingsheng / dating-master / lovelab / custom)
```

## 模块

| 模块 | 路径 |
|------|------|
| 总控（本文件） | 导出→选库→分析 |
| 微信导出 | [skills/wechat-mac-export/SKILL.md](skills/wechat-mac-export/SKILL.md) |
| **知识库 RAG 编排** | [skills/kb-rag/SKILL.md](skills/kb-rag/SKILL.md) |
| 知识目录 | [knowledge/REGISTRY.md](knowledge/REGISTRY.md) |
| 情圣（默认情感包） | [skills/qingsheng/SKILL.md](skills/qingsheng/SKILL.md) |
| 全量 chat 管线 | [skills/qingsheng/references/local-chat-pipeline.md](skills/qingsheng/references/local-chat-pipeline.md) |

## 默认工作流

```
Task Progress:
- [ ] 1. 需要本地微信数据？→ wechat-mac-export
- [ ] 2. Read knowledge/REGISTRY.md → kb-rag 选 1–2 个 pack
- [ ] 3. 若有 chat.txt → local-chat-pipeline 统计/时间线
- [ ] 4. 按选中 pack 的 SKILL/references 分析
- [ ] 5. 输出 1–2 关键点 + packs_used + 可发送原文或「先不发」
```

### 安全（总控强制）

- 对方明确拒绝 / 报警 / 要求停止 → **停止接触优先于任何话术包**  
- 事务收尾（快递/退款）与情感挽回分开  
- 勿把密钥、chat.txt、自定义隐私包推送到公开 git  

### 切换知识库示例

- 「用信号博弈/依恋分析」→ pack `dating-master`  
- 「用 Gottman/NVC 看情侣对话」→ pack `lovelab`  
- 「还是情圣怎么回」→ pack `qingsheng`  
- 「用我自己的笔记」→ `knowledge/custom/<id>` + `scripts/add-pack.sh`  

---

## Agent 纪律

1. 选库走 **kb-rag**，禁止凭空混用未读取的 pack 内容。  
2. 同轮深读最多 1–2 个 pack 入口。  
3. 导出技术问题以 wechat-mac-export 为准。  
4. 标注 `packs_used: [...]`。  
