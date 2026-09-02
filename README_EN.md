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

<sub>Can you hear it? Understand first. Speak later.</sub>

</div>

---

## What it is

pickled-fish is a **Cursor Agent skill pack**: export chats from **your own** macOS WeChat into readable `chat.txt`, then route each question through local knowledge packs so the agent can recommend what to send — or not to send.

It is not a hosted chatbot. The product is three concrete modules already in this repo:

1. **Export pipeline** — [`skills/wechat-mac-export`](skills/wechat-mac-export/)  
   For WeChat 4.1.10+: `wcdb-key-tool` (LLDB passphrase → PBKDF2) decrypts `db_storage/*.db`, then `wxecho export "nickname"` writes `~/Downloads/wxecho/<contact>/chat.txt`.
2. **Full-chat analysis** — [`skills/qingsheng/references/local-chat-pipeline.md`](skills/qingsheng/references/local-chat-pipeline.md)  
   Timeline, turn-taking, cold spots and turning points over multi-thousand-line exports — not screenshot fragments.
3. **Knowledge orchestration** — [`skills/kb-rag`](skills/kb-rag/) + [`knowledge/REGISTRY.md`](knowledge/REGISTRY.md)  
   Index-first filesystem RAG: `REGISTRY → PACK.md → rg keywords → Read passages`; at most **2** packs per turn; always cite `packs_used`.

Umbrella entry: [`SKILL.md`](SKILL.md).  
Read [`DISCLAIMER.md`](DISCLAIMER.md) first (own data only · not therapy · no harassment).

---

## End-to-end flow

```text
Mac WeChat 4.x
  db_storage/message_*.db
        │  wechat-mac-export
        │  (wcdb-key-tool → plaintext → wxecho)
        ▼
  chat.txt / json / csv
        │  local-chat-pipeline
        │  (timeline · turns · pivots)
        ▼
  kb-rag reads REGISTRY.md
        │  pick ≤2 packs
        ▼
  psych-foundations / attachment-ecr / nvc /
  lovelab / howtotalk / qingsheng / partner / …
        │
        ▼
  1–2 key points + draft reply or “don’t send yet”
  packs_used: [...]
```

How questions map to code:

| You ask | Agent opens |
|:--|:--|
| Export someone’s chat | `skills/wechat-mac-export/SKILL.md` → `wxecho export` |
| What does this huge `chat.txt` mean? | `local-chat-pipeline.md` → then theory/practice packs |
| What does she mean / how to reply / recovery | default `skills/qingsheng/` |
| Attachment / Gottman / NVC lens | `knowledge/packs/attachment-ecr` · `lovelab` · `nvc` |
| Negotiation / hard conversations | `knowledge/packs/howtotalk/` (13 sub-skills) |
| Long-term relationship maintenance | `knowledge/packs/partner/` |
| Use my own notes | `scripts/add-pack.sh` → `knowledge/custom/<id>` |

---

## Repo layout (mapped to features)

```text
pickled-fish/
├── SKILL.md                 # umbrella: export → select → analyze
├── knowledge/
│   ├── REGISTRY.md          # intent → pack routing table
│   ├── index.md             # taxonomy index
│   ├── packs/               # bundled MIT knowledge packs
│   └── custom/              # private packs (keep out of public git)
├── skills/
│   ├── wechat-mac-export/   # macOS WeChat decrypt + export
│   ├── kb-rag/              # pack selection + progressive disclosure
│   └── qingsheng/           # CN dating practice + local-chat pipeline
└── scripts/
    ├── install-skills.sh    # symlink into ~/.cursor/skills/
    └── add-pack.sh          # install git/local packs into custom/
```

### Bundled packs

| Pack | Path | What it does |
|:--|:--|:--|
| `psych-foundations` | `knowledge/packs/psych-foundations/` | Curriculum map → jump table |
| `attachment-ecr` | `knowledge/packs/attachment-ecr/` | ECR-R attachment dialogue assessment |
| `dating-master` | `knowledge/packs/dating-master/` | Pragmatics · attachment · signaling |
| `lovelab` | `knowledge/packs/lovelab/` | Gottman / NVC / cognitive distortions / dynamics |
| `chatrel` | `knowledge/packs/chatrel/docs/` | Sternberg · Knapp · social penetration · EWS docs |
| `rel-consult` | `knowledge/packs/rel-consult/` | Consultation protocol + ethics |
| `nvc` | `knowledge/packs/nvc/` | Four-step NVC rewrites |
| `howtotalk` | `knowledge/packs/howtotalk/` | 13 communication / negotiation skills |
| `partner` | `knowledge/packs/partner/` | Partner persona, scenarios, health metrics |
| `qingsheng` | `skills/qingsheng/` | Reply craft, recovery, profile audit, autopilot |

Optional remotes (not vendored by default): [REGISTRY § D](knowledge/REGISTRY.md).

---

## Install

```bash
git clone https://github.com/lnuxe/pickled-fish.git ~/.cursor/skills/pickled-fish
bash ~/.cursor/skills/pickled-fish/scripts/install-skills.sh
```

`install-skills.sh` symlinks four entries under `~/.cursor/skills/`: `pickled-fish`, `wechat-mac-export`, `qingsheng`, `kb-rag`.

Optional remote pack:

```bash
bash ~/.cursor/skills/pickled-fish/scripts/add-pack.sh psych-summaries \
  https://github.com/cognitivetech/Psychology-Summaries
```

Export deps (local): `@walkerch/wxecho`, [wcdb-key-tool](https://github.com/TANGandXUE/wcdb-key-tool), Python 3. Details in [`skills/wechat-mac-export/SKILL.md`](skills/wechat-mac-export/SKILL.md).

---

## Stars

[![Star History Chart](https://api.star-history.com/svg?repos=lnuxe/pickled-fish&type=Date&legend=top-left)](https://www.star-history.com/#lnuxe/pickled-fish&Date)

<p align="center">
  <a href="https://github.com/lnuxe/pickled-fish">
    <img src="https://img.shields.io/github/stars/lnuxe/pickled-fish?label=Star%20this%20repo&style=social" alt="Star" />
  </a>
</p>

---

## License & boundaries

[LICENSE](LICENSE) · [NOTICE](NOTICE) · [DISCLAIMER](DISCLAIMER.md)

Clear refusal / police involvement → **stop contact** before any pack scripts. Never commit passphrases, `chat.txt`, or private custom packs to public git.

---

<div align="center">

**[← 中文](README.md)**

</div>
