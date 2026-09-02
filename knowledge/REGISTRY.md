# Knowledge Registry · 知识包目录

本仓库用**文件系统 RAG**（progressive disclosure）：先读本目录与各包 `PACK.md` / `index.md`，再按需打开正文。无需向量库即可编排；需要向量 RAG 时见 [skills/kb-rag/references/vector-rag-optional.md](../skills/kb-rag/references/vector-rag-optional.md)。

自定义包放在 [`custom/`](custom/)（默认不强制提交隐私内容）。

---

## Bundled packs（已随仓）

| id | 路径 | 许可 | 适用 |
|----|------|------|------|
| `qingsheng` | [`../skills/qingsheng/`](../skills/qingsheng/) | MIT (tomwong001) | 中文恋爱教练、话术、七阶段、挽回 |
| `local-chat` | [`../skills/qingsheng/references/local-chat-pipeline.md`](../skills/qingsheng/references/local-chat-pipeline.md) | MIT (lnuxe) | 整段 macOS 导出 `chat.txt` 统计与时间线 |
| `dating-master` | [`packs/dating-master/`](packs/dating-master/) | MIT (YixiaJack) | 语用学 / 依恋 / 信号博弈「上帝视角」洞察 |
| `lovelab` | [`packs/lovelab/`](packs/lovelab/) | MIT (thc1006) | Gottman / NVC / 依恋 / 认知扭曲 · 伴侣对话分析 |
| `wechat-export` | [`../skills/wechat-mac-export/`](../skills/wechat-mac-export/) | MIT (lnuxe) | macOS 微信本地导出（非情感理论） |

## Remote packs（可选安装，不默认 vendoring）

| id | 上游 | 许可 | 说明 |
|----|------|------|------|
| `love-skill` | [pajamadot/love-skill](https://github.com/pajamadot/love-skill) | 查上游 | 13 心理框架 + 干预协议，中英 |
| `partner-skill` | [NatalieCao323/partner-skill](https://github.com/NatalieCao323/partner-skill) | MIT | 关系维护 / RQI / 场景话术 |
| `dating-coach` | [ddyuan-spec/dating-coach-skill](https://github.com/ddyuan-spec/dating-coach-skill) | 查上游 | 搭讪到约会全链路 |

安装远端包：

```bash
bash scripts/add-pack.sh love-skill https://github.com/pajamadot/love-skill
# → knowledge/custom/love-skill 或 knowledge/packs/<id>
```

---

## 路由启发式（编排器用）

| 用户意图 | 优先加载 |
|----------|----------|
| 导出/解密微信 | `wechat-export` |
| 整段 chat.txt / 本地统计 | `local-chat` → 再选理论包 |
| 「怎么回 / 阶段 / 挽回 / 展示面」偏男性社交教练 | `qingsheng` |
| 「她话里什么意思 / 信号真假 / 依恋追逃」偏洞察 | `dating-master` |
| 「情侣吵架 / Gottman / NVC / 双方视角」 | `lovelab` 或 `love-skill` |
| 用户指定 pack id / 自定义目录 | 只读该包 + `kb-rag` 协议 |

可多包并用，但**同轮最多深读 1–2 个 pack 的入口 SKILL**，其余只读 `PACK.md` 摘要，避免上下文爆炸。

---

## 自定义包最低要求

见 [`packs/_template/`](packs/_template/)。每个包需要：

1. `PACK.md`（元数据 + 何时用 + 入口文件列表）  
2. 至少一个 `SKILL.md` 或 `index.md`  
3. `LICENSE` 或在 `PACK.md` 声明许可来源  
