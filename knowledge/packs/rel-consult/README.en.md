# Relationship Consultation System

[中文](README.md) | [English](README.en.md)

A skills bundle for AI agents, providing a practical relationship consultation framework powered by multiple psychology-informed models.

## Quick Start

1. Ask your agent to read `CLAUDE.md` first (primary operating instructions).
2. Describe your relationship scenario and state your goal (for example: rebuild trust, improve communication).
3. For ongoing tracking, use `memory-templates/` to create profile and dyad files under `memory/`.

## Overview

This project provides a structured consultation workflow for relationship scenarios.
It focuses on:

- Non-diagnostic, hypothesis-based analysis
- Safer and more ethical guidance boundaries
- Multi-model interpretation for communication, trust, stress, needs, and behavior patterns

## Core Documents

- `docs/consultation-protocol.md`: session flow, communication principles, and guardrails
- `docs/integration-guide.md`: model integration, signal routing, and conflict handling
- `docs/model-bibliography.md`: model references and background

## Skills

The `skills/` directory contains modular skill files for specific dimensions such as:

- Attachment dynamics
- Conflict patterns
- Trust architecture
- Stress appraisal
- Need satisfaction
- Interaction style
- Attribution bias audit
- Boundaries and requests
- Decision support under uncertainty

## Memory Templates

- `memory-templates/subject-profile.md`
- `memory-templates/relationship-dyad.md`

Use these templates to maintain consistent, revisable records in the `memory/` directory.

## Notes

- This system is not a medical, psychiatric, or legal diagnostic tool.
- Outputs should remain tentative and revisable.
- Professional support should be recommended when severe distress, abuse, or trauma signals are present.

## Theory References (Concise)

For the full bibliography, see: `docs/model-bibliography.md`

- Attachment theory (adult romantic context)
  - Hazan, C., & Shaver, P. (1987). Romantic love conceptualized as an attachment process. *Journal of Personality and Social Psychology, 52*(3), 511-524. https://doi.org/10.1037/0022-3514.52.3.511
- Conflict patterns (Four Horsemen context)
  - Gottman, J. M. (1994). *Why Marriages Succeed or Fail*. Simon & Schuster.
- Trust architecture (ABI)
  - Mayer, R. C., Davis, J. H., & Schoorman, F. D. (1995). An integrative model of organizational trust. *Academy of Management Review, 20*(3), 709-734. https://doi.org/10.5465/amr.1995.9508080335
- Stress appraisal (cognitive appraisal)
  - Lazarus, R. S., & Folkman, S. (1984). *Stress, Appraisal, and Coping*. Springer.
- Need satisfaction (self-determination theory)
  - Deci, E. L., & Ryan, R. M. (2000). The "what" and "why" of goal pursuits: Human needs and the self-determination of behavior. *Psychological Inquiry, 11*(4), 227-268. https://doi.org/10.1207/S15327965PLI1104_01
- Interaction style (interpersonal circumplex)
  - Alden, L. E., Wiggins, J. S., & Pincus, A. L. (1990). Construction of circumplex scales for the Inventory of Interpersonal Problems. *Journal of Personality Assessment, 55*(3-4), 521-536. https://doi.org/10.1080/00223891.1990.9674088
- Motivational framing (regulatory focus)
  - Higgins, E. T. (1997). Beyond pleasure and pain. *American Psychologist, 52*(12), 1280-1300. https://doi.org/10.1037/0003-066X.52.12.1280
- Attribution and bias
  - Ross, L. (1977). The intuitive psychologist and his shortcomings: Distortions in the attribution process. In L. Berkowitz (Ed.), *Advances in Experimental Social Psychology* (Vol. 10, pp. 173-220). Academic Press. https://doi.org/10.1016/S0065-2601(08)60357-3
  - Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science, 185*(4157), 1124-1131. https://doi.org/10.1126/science.185.4157.1124
- Decision-making under uncertainty
  - Tversky, A., & Kahneman, D. (1979). Prospect theory: An analysis of decision under risk. *Econometrica, 47*(2), 263-292.
  - Gollwitzer, P. M. (1999). Implementation intentions: Strong effects of simple plans. *American Psychologist, 54*(7), 493-503. https://doi.org/10.1037/0003-066X.54.7.493
