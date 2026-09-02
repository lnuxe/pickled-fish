# LoveLab — Skills Architecture Design

**Version:** 1.0.0
**Date:** 2026-02-17
**Compatibility:** Claude Code, Codex CLI, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Aider

---

## Overview

LoveLab is a collection of 7 cross-platform AI Skills that analyze couple dialogue transcripts through evidence-based psychological frameworks. Each skill is a standalone `SKILL.md` file following the [Agent Skills Open Standard](https://agentskills.io).

**Core Principle:** LoveLab is a mirror, not a therapist. It helps couples *see* their communication patterns without prescribing what to do.

## Skills Map

```
lovelab-analyze (orchestrator)
├── lovelab-horsemen    → Gottman Four Horsemen detection
├── lovelab-attachment  → Attachment style dimensional analysis
├── lovelab-nvc         → NVC compliance scoring
├── lovelab-cognitive   → Cognitive distortion classification
├── lovelab-dynamics    → Communication dynamics & power analysis
└── lovelab-report      → Comprehensive report generation
```

## Skill Descriptions

| # | Skill | Input | Output | Theory Base |
|---|-------|-------|--------|-------------|
| 1 | **analyze** | Raw transcript | Summary dashboard | All frameworks |
| 2 | **horsemen** | Transcript | Four Horsemen scores + repair attempts | Gottman |
| 3 | **attachment** | Transcript | Anxiety/Avoidance dimensions per speaker | Bowlby, ECR-R |
| 4 | **nvc** | Transcript | Per-utterance NVC scores + giraffe/jackal ratio | Rosenberg |
| 5 | **cognitive** | Transcript | Cognitive distortion inventory | CBCT (Baucom & Epstein) |
| 6 | **dynamics** | Transcript | Pursuer-withdrawer, power index, LSM, We-ratio | Gottman, Pennebaker |
| 7 | **report** | Transcript or prior analysis outputs | Full Markdown report with cultural calibration | All + cultural layer |

## Cross-Platform Installation

### Claude Code
```bash
# Personal (all projects)
cp -r skills/lovelab-* ~/.claude/skills/

# Project-specific
cp -r skills/lovelab-* .claude/skills/
```

### Codex CLI
Append skill content to `AGENTS.md` (32 KiB limit).

### GitHub Copilot
Append skill content to `.github/copilot-instructions.md` (1000 lines limit).

### Cursor
Copy each SKILL.md as `.cursor/rules/<name>.mdc`.

### Gemini CLI
Reference skills in `GEMINI.md` or `system.md`.

### Auto-distribution
Use [Ruler](https://github.com/intellectronica/ruler) to auto-distribute from a single `.ruler/` directory to 12+ AI assistants.

## Design Principles

1. **Evidence-Based with Honest Caveats** — Every analytical dimension cites research. Disputed claims (e.g., Gottman's >90% prediction, 5:1 ratio) are presented with methodological context.
2. **Dimensional over Categorical** — Attachment uses anxiety/avoidance dimensions (ECR-R), not rigid types.
3. **Non-Judgmental** — Presents patterns, never verdicts.
4. **Privacy-First** — All analysis happens locally in the LLM context. No data is sent externally.
5. **Culturally Adaptive** — Built-in calibration for Chinese/Taiwanese communication norms, with generational and urban/rural qualifiers.
6. **Under 500 Lines Each** — Per Claude Code recommendations for optimal skill loading.

## Ethical Guardrails (All Skills)

- Mandatory disclaimer: "This is not therapy or professional counseling."
- Crisis detection: If self-harm, suicidal ideation, or violence indicators appear, immediately surface crisis resources (Taiwan: 1925/1995/1980).
- Never predict breakup/divorce probability.
- Never assign blame or declare one partner "right."
- Flag when professional help is recommended.

## Cultural Calibration Layer

Applies to all skills when analyzing Chinese/Mandarin transcripts:

| Domain | Western Default | Calibrated for Chinese/Taiwanese Context |
|--------|----------------|------------------------------------------|
| Emotional expression | Low expression = avoidance | Low expression may be **culturally adaptive** (Song et al. 2024); not pathological |
| Indirectness | Passive-aggressive | May be face-saving; check for embedded care signals |
| "Should" statements | Cognitive distortion | May reflect relational obligation norms; distinguish prescriptive from caring |
| Silence/pauses | Stonewalling | May be reflective processing; check post-silence behavior |
| Sex communication | Open discussion expected | Significant generational variation; urban youth increasingly open (Taiwan legalized same-sex marriage 2019) |

**Generational qualifier:** Always note that younger urban populations (born after ~1995) often diverge significantly from traditional norms.

## Research Gaps Disclosed

- **Gottman Method:** Zero effectiveness studies with Chinese couples specifically.
- **EFT in Chinese populations:** Only 2 studies; Tseng et al. (2024) found reduced depression but no significant improvement in relationship distress.
- **NVC:** No comprehensive meta-analysis exists; evidence base is "growing but limited."
- **5:1 ratio:** Not independently replicated (Kim et al. 2007); treat as heuristic, not diagnostic standard.

## File Format Specification

Each SKILL.md follows:
```yaml
---
name: lowercase-with-hyphens (max 64 chars)
description: Purpose description (max 1024 chars)
# Optional fields:
# allowed-tools: [Read, Write, Bash, Glob, Grep]
# model: sonnet (default) | opus | haiku
# context: fork (for subagent isolation)
---

# Skill Title

[Markdown body with instructions, examples, output templates]
```
