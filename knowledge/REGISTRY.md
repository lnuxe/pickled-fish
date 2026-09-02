# Knowledge Registry · 知识包总目录

文件系统 RAG：先读本文件与 [index.md](index.md)，再打开目标 `PACK.md`。  
自定义包 → [`custom/`](custom/) · 安装脚本 → `scripts/add-pack.sh`

> 理论包 ≠ 诊疗。涉及创伤/家暴/自伤请建议专业帮助。对方明确拒绝时停止接触优先于任何技法。

---

## A. 心理学 / 关系科学（理论与评估）

| id | 路径 | 许可 | 内容 |
|----|------|------|------|
| `psych-foundations` | [packs/psych-foundations](packs/psych-foundations/) | MIT (本仓地图) | 依恋/Gottman/NVC/Sternberg/表露/沟通 → 路由表 |
| `attachment-ecr` | [packs/attachment-ecr](packs/attachment-ecr/) | MIT | ECR-R 依恋风格对话评估 |
| `chatrel` | [packs/chatrel](packs/chatrel/) | MIT | Sternberg·Knapp·ECR-R·Gottman·社交渗透·EWS·LIWC 方法论文档 |
| `lovelab` | [packs/lovelab](packs/lovelab/) | MIT | Gottman / NVC / 认知扭曲 / 依恋 / 动力 |
| `dating-master` | [packs/dating-master](packs/dating-master/) | MIT | 语用学 · 依恋 · 信号博弈 |
| `rel-consult` | [packs/rel-consult](packs/rel-consult/) | MIT | 关系咨询框架 + 伦理护栏 |
| `nvc` | [packs/nvc](packs/nvc/) | MIT | 非暴力沟通改写 |
| `howtotalk` | [packs/howtotalk](packs/howtotalk/) | MIT | 13 沟通/谈判/影响力框架 |

## B. 恋爱 / 社交实操（教练向）

| id | 路径 | 许可 | 内容 |
|----|------|------|------|
| `qingsheng` | [../skills/qingsheng](../skills/qingsheng/) | MIT | 中文恋爱教练 · 七阶段 · 挽回 · 展示面 |
| `partner` | [packs/partner](packs/partner/) | MIT | 伴侣维护 · 场景话术 · 关系健康 |
| `local-chat` | qingsheng `local-chat-pipeline` | MIT | 整段导出 chat.txt 统计管线 |

## C. 工程 / 导出

| id | 路径 | 许可 | 内容 |
|----|------|------|------|
| `wechat-export` | [../skills/wechat-mac-export](../skills/wechat-mac-export/) | MIT | macOS 微信本地导出 |

## D. 可选远端（不默认 vendoring）

| id | 上游 | 许可 | 说明 |
|----|------|------|------|
| `psych-summaries` | [cognitivetech/Psychology-Summaries](https://github.com/cognitivetech/Psychology-Summaries) | CC0-1.0 | 依恋/创伤/多迷走等书籍摘要（体量大，按需安装） |
| `love-skill` | [pajamadot/love-skill](https://github.com/pajamadot/love-skill) / [pajama-studio/love-skill](https://github.com/pajama-studio/love-skill) | 查上游 | 13 心理框架双语咨询 |
| `dating-coach-cn` | [ddyuan-spec/dating-coach-skill](https://github.com/ddyuan-spec/dating-coach-skill) | **未声明** | 全链路教练；安装前自审合规与版权 |
| `htgawg` | [Mayuqi-crypto/HowToGetAlongWithGirls](https://github.com/Mayuqi-crypto/HowToGetAlongWithGirls) | **未声明** | dating-coach + 知识库；无 LICENSE 时不建议再分发 |
| `nvc-alt` | [gusujushi/gusujushi-nonviolent-communication](https://github.com/gusujushi/gusujushi-nonviolent-communication) | MIT | 另一套 NVC skill |
| `nvc-coach-jl` | [jlengrand/my-skills](https://github.com/jlengrand/my-skills) (`skills/nvc-coach`) | 查上游 | 轻量 NVC 改写教练 |
| `ex-skill` | [therealXiaomanChu/ex-skill](https://github.com/therealXiaomanChu/ex-skill) | 查上游 | 前任/ closure 向（与 partner 同源生态） |

```bash
bash scripts/add-pack.sh psych-summaries https://github.com/cognitivetech/Psychology-Summaries
bash scripts/add-pack.sh love-skill https://github.com/pajamadot/love-skill
```

---

## 路由启发式（kb-rag）

| 用户意图 | 优先 pack |
|----------|-----------|
| 要理论基础 /「用什么心理学看」 | `psych-foundations` → 再跳具体包 |
| 依恋类型 / 追逃 | `attachment-ecr` + `dating-master` |
| 情侣吵架 / 四骑士 / NVC 打分 | `lovelab` 或 `nvc` |
| 谈判式沟通 / 职场+感情说话技巧 | `howtotalk` |
| 伴侣聊天量化框架 | `chatrel` docs |
| 关系咨询结构 + 伦理 | `rel-consult` |
| 怎么回 / 挽回 / 展示面（中文实操） | `qingsheng` |
| 长期关系维护 | `partner` |
| 导出微信 | `wechat-export` |
| 整段 chat.txt | `local-chat` → 再选理论/实操包 |

同轮深读 **≤2** 个 pack 入口；输出标注 `packs_used`。

---

## 自定义包

见 [packs/_template](packs/_template/) 与 [custom/README.md](custom/README.md)。  
