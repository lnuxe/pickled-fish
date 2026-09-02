<div align="center">

# pickled-fish · 泡菜鱼

**Local WeChat export · Psychology & relationship KBs · Filesystem RAG**

[English](README_EN.md) · [中文](README.md)

<br/>

[![GitHub stars](https://img.shields.io/github/stars/lnuxe/pickled-fish?style=for-the-badge&logo=github&color=e8a838)](https://github.com/lnuxe/pickled-fish/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-2d6a4f?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/macOS-WeChat%204.x-1d3557?style=for-the-badge)](skills/wechat-mac-export/)
[![Disclaimer](https://img.shields.io/badge/Read-DISCLAIMER-c1121f?style=for-the-badge)](DISCLAIMER.md)

<br/>

<sub>Understand the conversation. Then decide what to do.</sub>

</div>

---

## In one line

> Unofficial toolkit: export chats from **your own** Mac WeChat, then analyze with pluggable knowledge packs.  
> **Not** therapy. **Not** a harassment aid. Read the [DISCLAIMER](DISCLAIMER.md) first.

---

## What it does

| | |
|:--|:--|
| **Export** | macOS WeChat 4.x local DB → `chat.txt` |
| **Orchestrate** | `kb-rag` picks ≤2 packs per question |
| **Theory** | Attachment · Gottman · NVC · Sternberg · negotiation… |
| **Practice** | Chinese dating coach · partner maintenance · full-chat pipeline |
| **Extend** | `custom/` + `add-pack.sh` for your own notes |

```text
  WeChat (local) ──export──► chat.txt
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
              timeline / stats       REGISTRY packs
                    │                     │
                    └────────► insight ◄──┘
                         packs_used: […]
```

---

## Install

```bash
git clone https://github.com/lnuxe/pickled-fish.git ~/.cursor/skills/pickled-fish
bash ~/.cursor/skills/pickled-fish/scripts/install-skills.sh
```

Optional remote packs (e.g. CC0 psychology summaries):

```bash
bash ~/.cursor/skills/pickled-fish/scripts/add-pack.sh psych-summaries \
  https://github.com/cognitivetech/Psychology-Summaries
```

---

## Knowledge at a glance

| Domain | Packs |
|:--|:--|
| Curriculum map | `psych-foundations` |
| Attachment / ECR-R | `attachment-ecr` · `dating-master` |
| Couple dynamics | `lovelab` · `chatrel` · `rel-consult` |
| Communication | `nvc` · `howtotalk` |
| CN practice | `qingsheng` · `partner` |

Full routing → [`knowledge/REGISTRY.md`](knowledge/REGISTRY.md)

---

## Stars

Live star history (updates with the repo):

[![Star History Chart](https://api.star-history.com/svg?repos=lnuxe/pickled-fish&type=Date&legend=top-left)](https://www.star-history.com/#lnuxe/pickled-fish&Date)

<p align="center">
  <a href="https://github.com/lnuxe/pickled-fish">
    <img src="https://img.shields.io/github/stars/lnuxe/pickled-fish?label=Star%20this%20repo&style=social" alt="Star" />
  </a>
</p>

---

## Navigate

| | |
|:--|:--|
| Umbrella | [`SKILL.md`](SKILL.md) |
| RAG | [`skills/kb-rag`](skills/kb-rag/) |
| Export | [`skills/wechat-mac-export`](skills/wechat-mac-export/) |
| Credits | [`NOTICE`](NOTICE) · [`LICENSE`](LICENSE) |

---

<div align="center">

<sub>Built for curious owners of their own data — not for crossing lines.</sub>

**[← 中文](README.md)**

</div>
