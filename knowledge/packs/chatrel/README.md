<div align="center">

# ChatRel

**Apply 7 empirically-grounded psychology frameworks to your chat history with a partner.**
**100% local · privacy-preserving · Chinese + English.**

[![Tests](https://github.com/ruanflux/chatrel/actions/workflows/test.yml/badge.svg)](https://github.com/ruanflux/chatrel/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-ruanflux.github.io%2Fchatrel-7d5fff)](https://ruanflux.github.io/chatrel/)

### **[🚀 Try the live demo →](https://ruanflux.github.io/chatrel/)**

[中文 README](README.zh.md) · [Methodology](docs/methodology.md) · [Limitations](docs/limitations.md) · [Schema](docs/schema.md) · [Changelog](CHANGELOG.md)

<a href="https://ruanflux.github.io/chatrel/"><img src="docs/screenshots/portal.png" alt="ChatRel portal" width="720"></a>

</div>

---

Most chat analyzers give you a word cloud, a sentiment line, and a heatmap. ChatRel does the opposite: it takes the dyadic interaction signals you already generated — seven months of messages with your partner — and maps them onto the frameworks relationship scientists have actually studied for 40+ years:

| Framework | What it measures | Anchor citation |
|---|---|---|
| **Sternberg Triangular** | Intimacy × Passion × Commitment as three separable axes | Sternberg (1986) |
| **Knapp Stages** | 10-stage model of relational development (Initiating → Bonding, then Differentiating → Terminating) | Knapp (1978) |
| **ECR-R Attachment** | Anxiety × Avoidance dimensions, mapped to Bartholomew 4-category types | Fraley, Waller & Brennan (2000); Bartholomew & Horowitz (1991) |
| **Gottman 5:1 + Four Horsemen** | Positive-to-negative interaction ratio; criticism/contempt/defensiveness/stonewalling density | Gottman (1994) |
| **Social Penetration** | Self-disclosure depth layered from shallow → core | Altman & Taylor (1973) |
| **Critical Slowing (EWS)** | Rising variance + AR(1) as early-warning for regime shifts | Scheffer et al. (2009) |
| **LIWC (Chinese proxy)** | Function-word / cognitive / affective markers | Pennebaker et al. |

**Output** is seven linked interactive HTML reports (Plotly-based), one per framework plus a curated memory book and a portal index. Everything runs on your machine. No data is ever sent anywhere.

## Screenshots

All images below are generated from the **synthetic demo dataset** (`sample_data/synthetic_couple.json`) that ships with the repo — no real chat data.

<div align="center">

| Depth / Sternberg / Knapp | Attachment & 12-week forecast |
|:---:|:---:|
| <img src="docs/screenshots/depth.png" width="420"> | <img src="docs/screenshots/attachment.png" width="420"> |
| **Conflict-repair events** | **External-threat resilience** |
| <img src="docs/screenshots/conflict.png" width="420"> | <img src="docs/screenshots/resilience.png" width="420"> |
| **Auto-curated memory book** | **Portal** |
| <img src="docs/screenshots/memory.png" width="420"> | <img src="docs/screenshots/portal.png" width="420"> |

</div>

## Install

```bash
git clone https://github.com/ruanflux/chatrel.git
cd chatrel
pip install -e .
```

Requires Python 3.10+. Dependencies: `jieba`, `snownlp`, `pandas`, `numpy`, `plotly`.

## Demo (no data required)

```bash
chatrel sample --out sample_data/synthetic_couple.json
chatrel analyze sample_data/synthetic_couple.json --out ./output
open ./output/index.html   # or start on Windows
```

This generates a ~2 000-message fictional 90-day couple chat containing every signal the analyzers look for, then runs the full pipeline. Everything in `output/` is derived from fake data you can freely screenshot.

## Real data

ChatRel reads a canonical chat JSON (see [docs/schema.md](docs/schema.md)):

```json
{
  "me_name": "Alex",
  "partner_name": "Sam",
  "messages": [
    {"ts": 1700000000, "role": "me", "text": "hi", "type": "text"},
    {"ts": 1700000010, "role": "partner", "text": "hey!"}
  ]
}
```

### Adapters

* **Telegram**: export from Telegram Desktop → Settings → Advanced → Export Telegram data → JSON, then
  ```bash
  python -m chatrel.adapters.telegram result.json --out chat.json
  ```
* **WeChat**: ChatRel does **not** bundle WeChat decryption. See [`src/chatrel/adapters/wechat.py`](src/chatrel/adapters/wechat.py) — it points you to external tools and provides a helper to consume their output.
* **Generic CSV / JSON**: `python -m chatrel.adapters.generic path.csv --out chat.json` — works for any `ts,role,text` dump.

Write your own adapter: it only needs to return a `chatrel.schema.Chat`.

## CLI

```bash
chatrel sample                      # Generate synthetic demo chat
chatrel analyze chat.json --out ./output
                                    # Run everything + portal index.html
chatrel depth      chat.json        # Sternberg + Knapp + IDS only
chatrel attachment chat.json        # ECR-R + Gottman + 12-week forecast
chatrel conflict   chat.json        # Conflict-repair events
chatrel external   chat.json        # Poaching / resilience analysis
chatrel memory     chat.json        # Auto-curated memory book
chatrel portal --out ./output       # Rebuild index from existing metrics
```

All subcommands accept `--out` (defaults to `./output`) and `--no-html` (metrics only).

## What you get

Each analyzer writes a `metrics_*.json` under the output directory; a corresponding HTML renderer turns that JSON into an interactive report. The seven outputs are:

| File | Content |
|---|---|
| `depth_metrics.json` + `depth_report.html` | Weekly signal time series · Sternberg triad scores · Knapp phase anchors · composite Intimacy Depth Score (IDS) · milestones · private lexicon |
| `attachment_forecast.json` + `attachment_forecast_report.html` | ECR-R scores · Bartholomew classification · couple-dynamic type · 12-week 3-scenario forecast · Gottman weekly P:N · four horsemen · critical slowing EWS |
| `conflict_events.json` + `conflict_report.html` | Detected conflict windows with initiator/peak/first-apology/recovery · monthly trend · repair-pattern stats |
| `resilience_metrics.json` + `resilience_report.html` | External-threat exposure · exclusivity/trust/we-ness density · 2 h response style · composite Resilience Index · joint stress coping |
| `memory_book_data.json` + `memory_book.html` | 10 chapters of auto-curated moments: firsts / sweetest / deepest / private lexicon / top days / role-specific best, with client-side search |
| `index.html` | Portal linking all of the above |

## Privacy

**ChatRel processes everything locally and makes zero network calls.**

* Your chat JSON never leaves the machine.
* The generated reports are standalone HTML; Plotly is loaded from a CDN at view time (you can swap to local by editing `renderers/common.py`).
* `.gitignore` blocks accidental commits of chat data and generated reports. Review it before pushing.
* The synthetic sample is the only bundled demo dataset — never commit real data.

## Ethics

You're analyzing a real person who hasn't read your lexicon. A few constraints that ChatRel bakes in but cannot enforce:

* The tool produces **proxy signals**, not diagnoses. Do not tell someone they "are" Anxious-Preoccupied.
* Attachment "types" are dimensional, contextual, and change with safety. The 2D scatter is a starting point, not a label.
* Forecasts are damped linear extrapolation with mean reversion, **not** probabilistic predictions. Do not tell someone "we'll break up in six weeks."
* If you decide to discuss findings with your partner, discuss the **patterns** (who apologizes more, when rituals dip), not the scores.

## Contributing

* New lexicons (English, Japanese, Spanish, …) are very welcome — open an issue or PR.
* New adapters (WhatsApp, iMessage, Discord, …) likewise.
* Eval data with expert-annotated ground truth would substantially improve validation — we'd love to collaborate.

## License

MIT © ChatRel contributors.

## Acknowledgements

Built on top of: [jieba](https://github.com/fxsjy/jieba), [SnowNLP](https://github.com/isnowfy/snownlp), [Plotly](https://plotly.com/python/). The psychology frameworks are cited inline and in [`docs/methodology.md`](docs/methodology.md).
