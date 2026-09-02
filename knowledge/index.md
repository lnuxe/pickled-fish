# Knowledge index

文件系统 RAG 根索引。Agent 回答知识相关问题时：**先读本文件与 [REGISTRY.md](REGISTRY.md)，再打开具体 pack。**

## Areas

| Area | Path | Summary |
|------|------|---------|
| Registry | [REGISTRY.md](REGISTRY.md) | 全部知识包目录与路由表 |
| Bundled packs | [packs/](packs/) | dating-master, lovelab, _template |
| Custom packs | [custom/](custom/) | 用户自建 / `add-pack.sh` 安装 |
| Qingsheng (bundled skill) | [../skills/qingsheng/](../skills/qingsheng/) | 中文恋爱教练主库 |
| Export tooling | [../skills/wechat-mac-export/](../skills/wechat-mac-export/) | 微信导出 |
| RAG orchestrator skill | [../skills/kb-rag/](../skills/kb-rag/) | 编排协议 |

## Navigation protocol

1. Read `REGISTRY.md` → pick pack id(s)  
2. Read that pack’s `PACK.md` (or skill root `SKILL.md` if no PACK.md)  
3. Open only listed `references/*` that match the question  
4. Never dump entire pack into context  
