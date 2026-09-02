<div align="center">

# 泡菜鱼 · pickled-fish

**微信本机导出 · 心理/关系知识库 · 文件系统 RAG**

[English](README_EN.md) · [中文](README.md)

<br/>

[![GitHub stars](https://img.shields.io/github/stars/lnuxe/pickled-fish?style=for-the-badge&logo=github&color=e8a838)](https://github.com/lnuxe/pickled-fish/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-2d6a4f?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/macOS-WeChat%204.x-1d3557?style=for-the-badge)](skills/wechat-mac-export/)
[![Disclaimer](https://img.shields.io/badge/先读-DISCLAIMER-c1121f?style=for-the-badge)](DISCLAIMER.md)

<br/>

<sub>你听得到吗 · 先看懂，再开口</sub>

</div>

---

## 它是什么

泡菜鱼是跑在 **Cursor Agent** 上的技能包：先把你本人 Mac 微信里的聊天导出成可读的 `chat.txt`，再按问题从本地知识包里挑理论/话术，给出可执行的判断（怎么回、先不回、还是停联系）。

它不是聊天机器人，也不是云端咨询。核心是三块已经写进仓库的代码与文档：

1. **导出管线** — [`skills/wechat-mac-export`](skills/wechat-mac-export/)  
   针对 WeChat 4.1.10+：`wcdb-key-tool`（LLDB 抓 passphrase → PBKDF2）解密 `db_storage/*.db`，再用 `wxecho export "昵称"` 写出 `~/Downloads/wxecho/<联系人>/chat.txt`。
2. **整段聊天分析** — [`skills/qingsheng/references/local-chat-pipeline.md`](skills/qingsheng/references/local-chat-pipeline.md)  
   对上万行导出做时间线、话轮、冷场/转折点统计，避免只看截图断章取义。
3. **知识库编排** — [`skills/kb-rag`](skills/kb-rag/) + [`knowledge/REGISTRY.md`](knowledge/REGISTRY.md)  
   Index-first 文件系统 RAG：`REGISTRY → PACK.md → rg 关键词 → Read 段落`；同轮最多深读 **2** 个 pack，并强制标注 `packs_used`。

总控入口：根目录 [`SKILL.md`](SKILL.md)。  
使用前请读 [`DISCLAIMER.md`](DISCLAIMER.md)（仅限本人数据 · 非诊疗 · 禁止骚扰）。

---

## 端到端流程

```text
Mac WeChat 4.x
  db_storage/message_*.db
        │  wechat-mac-export
        │  (wcdb-key-tool → 明文库 → wxecho)
        ▼
  chat.txt / json / csv
        │  local-chat-pipeline
        │  (时间线 · 话轮 · 转折)
        ▼
  kb-rag 读 REGISTRY.md
        │  选 ≤2 个 pack
        ▼
  psych-foundations / attachment-ecr / nvc /
  lovelab / howtotalk / qingsheng / partner / …
        │
        ▼
  1–2 个关键点 + 可发送原文或「先不发」
  packs_used: [...]
```

典型问题怎么走代码路径：

| 你说 | Agent 实际打开 |
|:--|:--|
| 导出某某的聊天 | `skills/wechat-mac-export/SKILL.md` → `wxecho export` |
| 这一大段 chat.txt 什么意思 | `local-chat-pipeline.md` → 再选理论/实操 pack |
| 她什么意思 / 怎么回 / 挽回 | 默认 `skills/qingsheng/`（七阶段、挽回、展示面） |
| 用依恋 / Gottman / NVC 看 | `knowledge/packs/attachment-ecr` · `lovelab` · `nvc` |
| 谈判式沟通、难开口 | `knowledge/packs/howtotalk/`（13 个子框架） |
| 长期关系怎么维护 | `knowledge/packs/partner/` |
| 换一套我自己的笔记 | `scripts/add-pack.sh` → `knowledge/custom/<id>` |

---

## 仓库结构（对应功能）

```text
pickled-fish/
├── SKILL.md                 # 总控：导出 → 选库 → 分析
├── knowledge/
│   ├── REGISTRY.md          # 路由表（意图 → pack id）
│   ├── index.md             # 分类索引
│   ├── packs/               # 已捆绑的 MIT 知识包
│   └── custom/              # 你的私有包（默认不进公开 git）
├── skills/
│   ├── wechat-mac-export/   # macOS 微信解密与导出
│   ├── kb-rag/              # 选包与 progressive disclosure
│   └── qingsheng/           # 中文恋爱实操 + local-chat 管线
└── scripts/
    ├── install-skills.sh    # 软链到 ~/.cursor/skills/
    └── add-pack.sh          # git/本地目录装进 custom/
```

### 已捆绑知识包

| Pack | 路径 | 具体能力 |
|:--|:--|:--|
| `psych-foundations` | `knowledge/packs/psych-foundations/` | 依恋/Gottman/NVC/Sternberg 等课程地图 → 跳转表 |
| `attachment-ecr` | `knowledge/packs/attachment-ecr/` | ECR-R 依恋风格对话评估 |
| `dating-master` | `knowledge/packs/dating-master/` | 语用学 · 依恋 · 信号博弈 |
| `lovelab` | `knowledge/packs/lovelab/` | Gottman 四骑士 / NVC / 认知扭曲 / 动力 |
| `chatrel` | `knowledge/packs/chatrel/docs/` | Sternberg·Knapp·社交渗透·EWS 等方法论 |
| `rel-consult` | `knowledge/packs/rel-consult/` | 关系咨询协议 + 伦理护栏 |
| `nvc` | `knowledge/packs/nvc/` | 非暴力沟通四步改写 |
| `howtotalk` | `knowledge/packs/howtotalk/` | 13 套沟通/谈判/影响力 SKILL |
| `partner` | `knowledge/packs/partner/` | 伴侣画像、场景话术、关系健康指标 |
| `qingsheng` | `skills/qingsheng/` | 怎么回、挽回、展示面、Autopilot 子命令 |

可选远端大库（不默认 vendoring）见 [REGISTRY 节 D](knowledge/REGISTRY.md)。

---

## 安装

```bash
git clone https://github.com/lnuxe/pickled-fish.git ~/.cursor/skills/pickled-fish
bash ~/.cursor/skills/pickled-fish/scripts/install-skills.sh
```

`install-skills.sh` 会软链四个入口到 `~/.cursor/skills/`：`pickled-fish`、`wechat-mac-export`、`qingsheng`、`kb-rag`。

按需安装远端包：

```bash
bash ~/.cursor/skills/pickled-fish/scripts/add-pack.sh psych-summaries \
  https://github.com/cognitivetech/Psychology-Summaries
```

导出依赖（本机）：`@walkerch/wxecho`、[wcdb-key-tool](https://github.com/TANGandXUE/wcdb-key-tool)、Python 3。步骤见 [`skills/wechat-mac-export/SKILL.md`](skills/wechat-mac-export/SKILL.md)。

---

## Stars

[![Star History Chart](https://api.star-history.com/svg?repos=lnuxe/pickled-fish&type=Date&legend=top-left)](https://www.star-history.com/#lnuxe/pickled-fish&Date)

<p align="center">
  <a href="https://github.com/lnuxe/pickled-fish">
    <img src="https://img.shields.io/github/stars/lnuxe/pickled-fish?label=Star%20this%20repo&style=social" alt="Star" />
  </a>
</p>

---

## 许可与边界

[LICENSE](LICENSE) · [NOTICE](NOTICE)（上游 pack 致谢）· [DISCLAIMER](DISCLAIMER.md)

对方明确拒绝 / 报警时，**停联系**优先于任何 pack 话术。密钥、`chat.txt`、自定义隐私包不要提交公开仓库。

---

<div align="center">

**[English →](README_EN.md)**

</div>
