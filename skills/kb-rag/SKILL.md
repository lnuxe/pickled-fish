---
name: kb-rag
description: >-
  Filesystem RAG for pickled-fish: routes to psych-foundations, attachment-ecr,
  lovelab, nvc, howtotalk, partner, rel-consult, chatrel, dating-master,
  qingsheng, or custom packs. Use for 知识库, RAG, 心理学, 依恋, NVC, Gottman,
  自定义包, or switching frameworks.
---

# kb-rag · 可定制知识库编排

> 免责声明见仓库 [DISCLAIMER.md](../../DISCLAIMER.md)。理论包 ≠ 诊疗。

本 skill 实现 **index-first / progressive disclosure RAG**（文件系统即状态）。可选向量方案见 [references/vector-rag-optional.md](references/vector-rag-optional.md)。

## 何时启用

- 用户说：知识库 / RAG / 心理学 / 依恋 / NVC / Gottman / 换框架 / 自定义包  
- 总控 `pickled-fish` 需要选 pack  
- 用户传入 `--pack=qingsheng,attachment-ecr` 等显式指定  

## 编排协议（每次）

```
Task Progress:
- [ ] 1. Read knowledge/index.md + knowledge/REGISTRY.md
- [ ] 2. Select 1–2 pack ids (or user override)
- [ ] 3. Read each pack’s PACK.md (or skill SKILL.md)
- [ ] 4. Open only matching references (rg by keyword)
- [ ] 5. Answer with 1–2 key points + packs_used
- [ ] 6. If chat.txt: also apply local-chat pipeline
```

### 选择规则

1. **用户显式指定** > REGISTRY 路由表 > 默认 `qingsheng`  
2. 「用什么心理学看」→ 先 `psych-foundations`，再跳具体理论包  
3. 导出/解密 → 转 `wechat-export`，不要用情感 pack 硬答  
4. 多 pack 冲突：安全边界（停止接触）> 各 pack 话术  
5. `knowledge/custom/*` 在用户声明「用我的库」时优先于同名 bundled  

### 检索方式（默认）

| 步骤 | 动作 |
|------|------|
| L0 | `REGISTRY.md` / `index.md` |
| L1 | 目标 `PACK.md` |
| L2 | `rg -n "关键词" pack目录` |
| L3 | `Read` 命中段落 |

禁止：一次性 Read 整个 pack 所有 md。

### 输出要求

- 注明 `packs_used: [id, …]`  
- 引用写成「依据 attachment-ecr / nvc」这类路径  
- 短回复优先；长报告仅当用户要求  

## 自定义 / 远端包

```bash
bash scripts/add-pack.sh my-notes /path/to/notes
bash scripts/add-pack.sh psych-summaries https://github.com/cognitivetech/Psychology-Summaries
cp -R knowledge/packs/_template knowledge/custom/my-pack
```

远端列表见 REGISTRY 节 D。无 LICENSE 的仓库不要再分发。

详见 [references/pack-spec.md](references/pack-spec.md)。

## 与总控关系

根目录 [SKILL.md](../../SKILL.md) 负责「导出 → 分析」；**选哪套理论**由本 skill + REGISTRY 决定。
