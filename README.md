# pickled-fish

macOS **微信本机导出** + **可插拔情感/关系知识库** + **文件系统 RAG 编排**。

> **先读 [DISCLAIMER.md](DISCLAIMER.md)。** 非官方 · 仅限本人账号/设备 · 可能违反微信协议 · 情感建议非专业咨询 · 风险自负。

## 架构

| 层 | 内容 |
|----|------|
| 导出 | [skills/wechat-mac-export](skills/wechat-mac-export/)（wcdb-key-tool + WxEcho 路径） |
| 编排 | [skills/kb-rag](skills/kb-rag/)：按意图选择知识包，progressive disclosure |
| 知识包 | [knowledge/REGISTRY.md](knowledge/REGISTRY.md) |
| 总控 | [SKILL.md](SKILL.md) |

默认 **不依赖向量数据库**；大私有语料可按 kb-rag 文档挂本地 `search.py`。

## 已收录 / 可安装的知识包

**随仓（MIT）：**

- [qingsheng-skill](https://github.com/tomwong001/qingsheng-skill) — 中文恋爱教练  
- [dating-master-skill](https://github.com/YixiaJack/dating-master-skill) — 语用学 / 依恋 / 信号博弈  
- [lovelab-skills](https://github.com/thc1006/lovelab-skills) — Gottman / NVC / 认知 / 依恋  

**可选安装（`scripts/add-pack.sh`）：**

- [love-skill](https://github.com/pajamadot/love-skill)  
- [partner-skill](https://github.com/NatalieCao323/partner-skill)  
- [dating-coach-skill](https://github.com/ddyuan-spec/dating-coach-skill)  
- 任意本地笔记目录（复制 `_template`）

## 安装

```bash
git clone https://github.com/lnuxe/pickled-fish.git ~/.cursor/skills/pickled-fish
bash ~/.cursor/skills/pickled-fish/scripts/install-skills.sh
```

添加自定义包：

```bash
bash scripts/add-pack.sh my-kb ~/Documents/my-relationship-notes
# 或
bash scripts/add-pack.sh love-skill https://github.com/pajamadot/love-skill
```

## 典型用法

1. 「导出和某某的微信」→ wechat-export  
2. 「根据 chat.txt 分析，用情圣」→ local-chat + qingsheng  
3. 「换依恋/信号博弈视角」→ kb-rag → dating-master  
4. 「情侣吵架用 Gottman」→ lovelab  
5. 「只用我自己的知识库」→ custom pack  

## 致谢与许可

见 [NOTICE](NOTICE)、[LICENSE](LICENSE)。上游包版权归原作者；本仓编排与导出文档 Copyright lnuxe。
