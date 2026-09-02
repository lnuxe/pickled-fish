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

<sub>把聊天变成可检索的证据 · 把证据接到可切换的理论包 · 再决定怎么回——或先不回。</sub>

</div>

---

## 一句话

> 非官方工具：从**你自己的** Mac 微信导出聊天，再用可插拔知识包做分析。  
> **不是**诊疗，**不是**骚扰助手。使用前请读 [DISCLAIMER](DISCLAIMER.md)。

---

## 它做什么

| | |
|:--|:--|
| **导出** | macOS 微信 4.x 本机库 → `chat.txt` |
| **编排** | `kb-rag` 按问题选 ≤2 个知识包 |
| **理论** | 依恋 · Gottman · NVC · Sternberg · 沟通谈判… |
| **实操** | 情圣话术 · 伴侣维护 · 整段聊天管线 |
| **扩展** | `custom/` + `add-pack.sh` 接你自己的笔记 |

```text
  WeChat (本地) ──export──► chat.txt
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
              时间线 / 统计           REGISTRY 选包
                    │                     │
                    └─────────► 洞察 ◄────┘
                         packs_used: […]
```

---

## 安装

```bash
git clone https://github.com/lnuxe/pickled-fish.git ~/.cursor/skills/pickled-fish
bash ~/.cursor/skills/pickled-fish/scripts/install-skills.sh
```

按需拉远端大库（例：CC0 心理学摘要）：

```bash
bash ~/.cursor/skills/pickled-fish/scripts/add-pack.sh psych-summaries \
  https://github.com/cognitivetech/Psychology-Summaries
```

---

## 知识域速览

| 域 | Pack |
|:--|:--|
| 课程地图 | `psych-foundations` |
| 依恋 / ECR-R | `attachment-ecr` · `dating-master` |
| 情侣互动 | `lovelab` · `chatrel` · `rel-consult` |
| 沟通 | `nvc` · `howtotalk` |
| 中文实操 | `qingsheng` · `partner` |

完整路由 → [`knowledge/REGISTRY.md`](knowledge/REGISTRY.md)

---

## Stars

实时曲线（随仓库 stars 更新）：

[![Star History Chart](https://api.star-history.com/svg?repos=lnuxe/pickled-fish&type=Date&legend=top-left)](https://www.star-history.com/#lnuxe/pickled-fish&Date)

<p align="center">
  <a href="https://github.com/lnuxe/pickled-fish">
    <img src="https://img.shields.io/github/stars/lnuxe/pickled-fish?label=Star%20this%20repo&style=social" alt="Star" />
  </a>
</p>

---

## 导航

| | |
|:--|:--|
| 总控 | [`SKILL.md`](SKILL.md) |
| RAG | [`skills/kb-rag`](skills/kb-rag/) |
| 导出 | [`skills/wechat-mac-export`](skills/wechat-mac-export/) |
| 致谢 | [`NOTICE`](NOTICE) · [`LICENSE`](LICENSE) |

---

<div align="center">

<sub>Built for curious owners of their own data — not for crossing lines.</sub>

**[English →](README_EN.md)**

</div>
