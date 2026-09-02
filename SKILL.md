---
name: pickled-fish
description: >-
  macOS WeChat export plus pluggable psychology/relationship/social knowledge
  packs and filesystem RAG (qingsheng, Gottman, NVC, attachment, howtotalk,
  partner, custom KBs). Use for decrypt/export, chat.txt analysis, 怎么回/挽回,
  心理学/依恋/NVC/知识库/RAG/自定义包, or switching frameworks.
---

# pickled-fish · 泡菜鱼 · 导出 + 心理/关系知识库

> [DISCLAIMER.md](DISCLAIMER.md) · 仅限本人数据 · 非专业诊疗 · 禁止骚扰

```
微信导出 → local-chat 统计 → kb-rag（REGISTRY）→ 理论/实操/自定义 pack
```

## 模块

| 模块 | 路径 |
|------|------|
| 知识总目录 | [knowledge/REGISTRY.md](knowledge/REGISTRY.md) |
| 课程地图 | [knowledge/packs/psych-foundations](knowledge/packs/psych-foundations/) |
| RAG 编排 | [skills/kb-rag/SKILL.md](skills/kb-rag/SKILL.md) |
| 微信导出 | [skills/wechat-mac-export/SKILL.md](skills/wechat-mac-export/SKILL.md) |
| 默认中文实操 | [skills/qingsheng/SKILL.md](skills/qingsheng/SKILL.md) |

## 默认工作流

```
Task Progress:
- [ ] 1. 导出？→ wechat-mac-export
- [ ] 2. Read knowledge/REGISTRY.md（或先 psych-foundations 地图）
- [ ] 3. kb-rag 选 ≤2 个 pack
- [ ] 4. chat.txt？→ local-chat-pipeline
- [ ] 5. 分析：1–2 关键点 + packs_used + 可发送原文或「先不发」
```

### 安全

对方明确拒绝 / 报警 → **停联系**优先于任何 pack。  
事务收尾与情感挽回分开。勿提交密钥与 chat。

### 选包速查

- 理论基础 → `psych-foundations`
- 依恋 → `attachment-ecr` / `dating-master`
- 情侣冲突 → `lovelab` / `nvc`
- 沟通谈判 → `howtotalk`
- 怎么回/挽回 → `qingsheng`
- 关系维护 → `partner`
- 量化框架 → `chatrel` docs

---

## Agent 纪律

1. 选库必须经过 REGISTRY / kb-rag，禁止编造未读 pack 内容。
2. 同轮深读 ≤2 个 pack 入口。
3. 标注 `packs_used: [...]`。
