# LoveLab

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-Open_Standard-green.svg)](https://agentskills.io)
[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code-Plugin-blueviolet.svg)](https://code.claude.com/docs/en/plugins)
[![Platform](https://img.shields.io/badge/Platform-Claude_|_Codex_|_Gemini_|_Cursor-lightgrey.svg)](#cross-platform-support)

Paste a couple's conversation. Get a structured analysis based on Gottman, attachment theory, NVC, and cognitive behavioral frameworks.

Not therapy. A mirror.

## Install

```bash
# Claude Code plugin (recommended)
/plugin marketplace add thc1006/lovelab-skills
/plugin install lovelab@lovelab-marketplace

# Or test locally
git clone https://github.com/thc1006/lovelab-skills.git
claude --plugin-dir ./lovelab-skills
```

Skills-only (no plugin):

```bash
git clone https://github.com/thc1006/lovelab-skills.git
cp -r lovelab-skills/skills/lovelab-* ~/.claude/skills/
```

### Cross-Platform Support

Follows the [Agent Skills open standard](https://agentskills.io).

| Platform | Installation |
|----------|-------------|
| Claude Code | Plugin or `~/.claude/skills/` |
| Codex CLI | `~/.codex/skills/` |
| Gemini CLI | Reference in `GEMINI.md` |
| Cursor | `.cursor/rules/<name>.mdc` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Windsurf | `.windsurfrules.md` |

## Usage

```
> Analyze this couple dialogue: [paste transcript]
> Use lovelab-horsemen to detect the Four Horsemen in this transcript: [paste]
```

See [examples/](examples/) for sample input, output, and the JSON schema for longitudinal tracking.

## Skills

| Skill | Analyzes | Based on |
|-------|----------|----------|
| `lovelab-analyze` | Full analysis orchestrator | All |
| `lovelab-horsemen` | Four Horsemen + repair attempts | Gottman |
| `lovelab-attachment` | Anxiety/avoidance dimensions | ECR-R, EFT |
| `lovelab-nvc` | NVC compliance scoring | Rosenberg |
| `lovelab-cognitive` | 7 cognitive distortion types | CBCT |
| `lovelab-dynamics` | Pursuer-withdrawer, power, pronouns, LSM | Gottman, Pennebaker |
| `lovelab-report` | Report with strengths, growth tracking | All + cultural layer |

### Longitudinal Tracking

Results follow a [standardized JSON schema](examples/analysis-schema.json) so you can compare across sessions:

```
Session 1 (baseline)  -->  Session 2  -->  Session 3
  Anxiety: 6/10            Anxiety: 5/10     Anxiety: 4/10
  Repair rate: 60%         Repair rate: 75%  Repair rate: 80%
```

## Cultural Calibration

Includes a calibration layer for Chinese/Mandarin communication. Examples:

| Pattern | Western default | Calibrated reading |
|---------|----------------|--------------------|
| Low emotional expression | Avoidant | May be culturally adaptive (Song et al. 2024) |
| Indirect communication | Passive-aggressive | May be face-saving with care signals |
| Silence | Stonewalling | May be reflective processing |

Generational differences noted. Post-1995 urban Taiwanese populations often diverge from traditional norms.

## What This Is Not

Not a therapist. Not a divorce predictor. Not a replacement for professional help. Not a judge of who is right.

Crisis resources: Taiwan 1925 / 1995 / 1980. International: https://findahelpline.com

## Methodological Limitations

Every skill discloses its limits. The big ones:

- Gottman's >90% divorce prediction was not cross-validated. Dropped to 29% in Heyman (2001). Four Horsemen are useful for pattern recognition, not prediction.
- The 5:1 ratio is a heuristic from specific samples, not a universal standard.
- NVC has a growing but limited evidence base. No meta-analysis exists yet.
- Zero Gottman studies and only 2 EFT studies have been conducted with Chinese populations.

## References

- Gottman (1994). *What Predicts Divorce?*
- Fraley et al. (2015). Categorical or Dimensional? *JPSP* 109(2).
- Rosenberg (2003). *Nonviolent Communication*.
- Ireland et al. (2011). Language Style Matching. *Psych Science* 22(1).
- Song, Chan & Ryan (2024). Expressive Suppression in East Asian Societies.
- Heyman (2001). Observation of Couple Conflicts. *J Marriage & Family* 63.
- Kim, Capaldi & Crosby (2007). Generalizability of Gottman. *J Marriage & Family* 69.

## Privacy

All analysis runs locally in the LLM context window. These are plain Markdown files. No external servers, no API keys, no telemetry.

## Contributing

Open an issue before submitting a PR. Help wanted:

- Language calibration layers (Korean, Japanese, Spanish, Arabic)
- Validation against trained coder annotations
- Longitudinal tracking tooling

## Project Structure

```
lovelab-skills/
  .claude-plugin/
    plugin.json              Plugin manifest
    marketplace.json         Marketplace definition
  skills/
    lovelab-analyze/         Full analysis orchestrator
    lovelab-horsemen/        Gottman Four Horsemen
    lovelab-attachment/      Attachment dimensions
    lovelab-nvc/             NVC scoring
    lovelab-cognitive/       Cognitive distortions
    lovelab-dynamics/        Communication dynamics
    lovelab-report/          Report generation
  examples/
    sample-transcript.txt    Sample input
    sample-output.md         Sample report
    analysis-schema.json     JSON schema for tracking
```

## License

[MIT](LICENSE)

LoveLab is for self-reflection. It is not a substitute for licensed therapy, mental health treatment, or crisis intervention. If you are in distress, please contact a qualified professional.
