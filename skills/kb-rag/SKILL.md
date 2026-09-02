---
name: kb-rag
description: >-
  Customizable filesystem RAG / knowledge-pack orchestration for mac-wechat-coach.
  Routes questions to qingsheng, dating-master, lovelab, or user packs under
  knowledge/. Use when the user mentions 知识库, RAG, 自定义包, pack, registry,
  切换知识库, or wants non-default coaching frameworks.
---

# kb-rag · 可定制知识库编排

> 免责声明见仓库 [DISCLAIMER.md](../../DISCLAIMER.md)。情感内容非专业咨询。

本 skill 实现 **index-first / progressive disclosure RAG**（文件系统即状态，无需向量库）。可选向量方案见 [references/vector-rag-optional.md](references/vector-rag-optional.md)。

## 何时启用

- 用户说：知识库 / RAG / 换一套框架 / 用 Gottman / 用信号博弈 / 自定义笔记  
- 总控 `mac-wechat-coach` 需要选 pack  
- 用户传入 `--pack=qingsheng,dating-master` 这类显式指定  

## 编排协议（每次）

```
Task Progress:
- [ ] 1. Read knowledge/index.md + knowledge/REGISTRY.md
- [ ] 2. Select 1–2 pack ids (or user override)
- [ ] 3. Read each pack’s PACK.md (or skill SKILL.md)
- [ ] 4. Open only matching references (grep/rg by keyword if needed)
- [ ] 5. Answer with 1–2 key points + cite pack ids used
- [ ] 6. If chat.txt export: also apply local-chat pipeline
```

### 选择规则

1. **用户显式指定** > 路由表启发式 > 默认 `qingsheng`  
2. 导出/解密问题 → 不要用情感 pack 硬答，转 `wechat-export`  
3. 多 pack 冲突时：安全边界（停止接触）> 各 pack 话术  
4. 自定义 `knowledge/custom/*` 优先于同名 bundled（若用户声明「用我的库」）  

### 检索方式（默认）

| 步骤 | 动作 |
|------|------|
| L0 | `REGISTRY.md` / `index.md` |
| L1 | 目标 `PACK.md` |
| L2 | `rg -n "关键词" pack目录` 定位文件 |
| L3 | `Read` 命中文件的相关段落 |

禁止：一次性 Read 整个 pack 所有 md。

### 输出要求

- 注明 `packs_used: [id, …]`  
- 引用写成「依据 dating-master/signaling」这类路径，不编造论文页码  
- 短回复优先；长报告仅当用户要求  

## 自定义包

```bash
bash scripts/add-pack.sh my-notes /path/to/notes   # 本地目录
bash scripts/add-pack.sh love-skill https://github.com/pajamadot/love-skill
cp -R knowledge/packs/_template knowledge/custom/my-pack
```

详见 [references/pack-spec.md](references/pack-spec.md)。

## 与总控关系

根目录 [SKILL.md](../../SKILL.md) 负责「导出 → 分析」大流程；**选哪套理论**由本 skill 决定。
