<div align="center">

# Partner Skill (现任.skill)

**Distill your partner into a living AI Skill. A 3-layer expert system for relationship maintenance.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-7B61FF.svg)](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
[![AgentSkills Standard](https://img.shields.io/badge/AgentSkills-Standard-00C853.svg)](https://github.com/AgentSkills-Org/AgentSkills)

[Installation](#installation) · [Core Technology](#core-technology-the-3-layer-expert-system) · [Usage](#usage) · [Examples](#user-examples) · [File Structure](#file-structure) · [中文](./README.md)

> ⚠️ **Disclaimer**: This project is for personal relationship analysis and improvement only. It does not replace genuine communication and should never be used to manipulate or deceive your partner.

</div>

---

## Why Partner Skill?

In intimate relationships, we often find ourselves thinking: **"I know I love them, but I don't know what to do right now."**

While ordinary AI gives generic "communication advice," **Partner Skill** is a **3-layer expert system** custom-built for your partner. It doesn't just understand their attachment style and personality—it accurately infers your current relationship state, and before you say something that might escalate a conflict, it **simulates the consequences of multiple responses for you**.

From consolidating the honeymoon phase to keeping the stable phase fresh; from negotiating chores to breaking the ice after a cold war. It's not just an analytical tool; it's a **strategy execution engine**.

---

## Core Technology: The 3-Layer Expert System

Partner Skill completely abandons the traditional "Prompt Q&A" model, restructuring into a **5-step execution protocol** compliant with the Claude Code Skill standard. Its core consists of three hardcore engines:

### 1. State Engine
**"What phase are we actually in right now?"**
- **State Space**: Defines 6 discrete states from S1 (Honeymoon) to S6 (Brink of Breakup).
- **Signal Extraction**: Extracts 6 observable signals from your description (e.g., response latency, initiation ratio, negative sentiment frequency).
- **Trajectory Prediction**: Automatically infers the current state $S_t$ and predicts which state $S_{t+1}$ the relationship will drift toward in 1 week without intervention, along with the RQI (Relationship Quality Index) decay.

### 2. Policy Selector
**"The same problem requires completely different strategies for different people."**
- **Policy Space**: Built-in 7 intervention strategies from P1 (Soothing) to P7 (Crisis Intervention).
- **Decision Matrix**: Outputs the optimal strategy from 24 combinations based on the partner's **Attachment Style** (Secure/Anxious/Avoidant/Fearful) × **Current State** (S1-S6) × **Conflict Type** (Gottman's Four Horsemen).
- **Execution Directives**: Each strategy provides not only verbatim scripts but also explicit **"Forbidden Actions"** (e.g., never double-text an avoidant partner; never use the silent treatment on an anxious partner).

### 3. Counterfactual Engine
**"If I reply like this, what will they think?"**
- **Multi-path Simulation**: Before giving final advice, the engine simulates 2-4 candidate responses in parallel.
- **RQI Impact Quantification**: Predicts the specific impact of each sentence on the relationship using the formula `RQI_delta = base_impact × attachment_modifier`.
- **Pitfall Avoidance**: Visually displays the optimal response (✅) and the worst response (❌), letting you see the consequences before you act.

---

## Theoretical Foundation & Mathematical Models

Beyond the 3-layer engine, Partner Skill is supported by rigorous psychological and mathematical models:

- **RQI (Relationship Quality Index)**: An 8-dimension weighted model to quantify relationship health.
- **ACS (Attachment Compatibility Score)**: A 16-combination matrix of attachment styles, acting as a baseline multiplier for RQI.
- **LLMI (Love Language Mismatch Index)**: A 5×5 compatibility matrix quantifying communication gaps.
- **5-Layer Persona**: Integrates Big Five (OCEAN), MBTI, Gottman's Four Horsemen detection, emotion regulation styles, and decision-making styles.
- **Memory Activation Model**: $W = E \times R \times (1 + F)$, ensuring the AI remembers the milestones that matter most to you.

---

## Covers 23 Real-Life Scenarios

Partner Skill doesn't just handle conflicts; it covers all aspects of daily life:

| Category | Supported Scenarios |
|----------|---------------------|
| **Emotion & Conflict** | Partner is angry, needs comfort, how to apologize, handling jealousy & insecurity |
| **Celebration & Gifting** | Anniversary planning, birthday surprises, holiday gifts, celebrating partner's achievements |
| **Experience & Daily Life** | Date planning, travel arrangements, daily warmth, supporting personal growth |
| **Reality & Development** | Chores negotiation, financial discussions, cohabitation, digital boundaries (phone usage), meeting the parents, social circle integration, career stress support, health care, future planning |

---

## Installation

### Method 1: Claude Code (Recommended)
No installation required. Just enter the project directory in your terminal and start Claude Code:
```bash
git clone https://github.com/NatalieCao323/partner-skill.git
cd partner-skill
claude
```

### Method 2: OpenClaw
If you use the OpenClaw desktop app, install via:
```bash
openclaw install https://github.com/NatalieCao323/partner-skill.git
```

---

## Usage

### Step 1: Create Partner Profile
In Claude Code or OpenClaw, type:
> `/create-partner`

The AI will guide you through 3 simple questions and prompt you to upload chat logs (supports WeChat/SMS TXT, screenshots, emails, etc.). The system will then automatically generate `profile.json`, `persona.md`, and `health_report.md`.

### Step 2: Daily Invocation (Advisor Mode)
Whenever you encounter an issue, simply describe the situation to trigger the 5-step execution protocol:
> `/partner I canceled our date yesterday because of overtime, and they just replied "whatever". How should I respond?`

### Step 3: Generate Health Report
Get a regular check-up with an RQI radar chart and a 30-day improvement plan:
> `/partner-report`

### Step 4: Record Reflections & Milestones
Log important moments or review conflicts:
> `/partner-reflect Log this: Today we cooked together for the first time. We burned the pan, but we laughed so hard.`

---

## User Examples

### Example 1: Counterfactual Simulation (Conflict Scenario)

**User**: I canceled our date yesterday because of overtime, and they just replied "whatever". How should I respond?

**AI**:
```text
📍 Situation Diagnosis
Current State: S4 — Conflict Phase (Confidence 82%)
Trend: Without intervention, will drift to S5 (Withdrawal) in 1 week, RQI Δ -1.2
Urgency: HIGH

🧠 Strategy Selection
Primary Strategy: P1 — Soothing
Core Logic: Partner has an Anxious attachment style; their core fear is abandonment. Any explanation right now will be seen as defensiveness. You must lower emotional activation and establish safety first.

⚖️ Counterfactual Simulation
🥇 Response B: Soothing ✅ (RQI +1.04)
   "Baby, I'm so sorry. I know you're disappointed. You've been looking forward to this, and I let you down. Let me figure out how to make it up to you right now, okay?"
   Predicted Reaction: Emotions soften, defensiveness lowers.

🥈 Response C: Problem-Solving ⚠️ (RQI -0.78)
   "What do you mean 'whatever'? Can we talk about this properly?"
   Predicted Reaction: Feels unheard, "You only care about solving the problem, not my feelings."

🥉 Response A: Defensive ❌ (RQI -1.56)
   "I didn't want to either, but I had no choice with work. Can't you be a little understanding?"
   Predicted Reaction: Defenses escalate, counter-attack intensifies.

#4 Response D: Dismissive 🚨 (RQI -2.34)
   "Fine, whatever then."
   Predicted Reaction: Emotional breakdown, triggers deepest fears.

💬 Recommended Action
Please use the approach in [Response B].
❌ NEVER say:
- "I didn't want to either" (shifting blame)
- "Stop being mad" (invalidating emotions)
```

### Example 2: Reality & Development (Chores Negotiation)

**User**: We recently moved in together, but they always leave dirty clothes on the couch. I've mentioned it a few times but it hasn't worked. How should I communicate this?

**AI**:
```text
📍 Situation Diagnosis
Current State: S2 — Stable Phase
Urgency: MEDIUM (Lifestyle friction, need to prevent it from turning into a power struggle)

🧠 Strategy Selection
Primary Strategy: P4 — Boundary Setting
Core Logic: Partner is an ISTP (logic-driven). They are immune to emotional accusations but highly receptive to clear rules and systems.

💬 Recommended Script (Non-Violent Communication Framework):
"Recently, I've noticed dirty clothes on the couch often (Observation). It makes me feel a bit tired because I need our home to be tidy (Feeling & Need). Could we buy a specific laundry basket to put next to the couch, so we can just throw clothes in there when we change? (Specific Request)"

❌ NEVER say:
- "You ALWAYS leave your clothes everywhere!" (Absolute accusation, triggers defense)
- "Can't you just be considerate of me?" (Emotional expression, hard for ISTP to process)
```

---

## File Structure

This project follows the [AgentSkills](https://agentskills.io) open standard:

```text
partner-skill/
├── SKILL.md                    # Core execution protocol (5-step workflow)
├── prompts/                    # Prompt templates
│   ├── state_engine.md         # State machine rules
│   ├── policy_selector.md      # Strategy selection matrix
│   ├── counterfactual_engine.md# Counterfactual simulation framework
│   ├── persona_builder.md      # 5-layer persona construction
│   ├── relationship_health.md  # RQI mathematical model
│   └── scenario_advisor.md     # 23 scenario templates
├── tools/                      # Python tools
│   ├── state_engine.py         # State inference engine
│   ├── policy_selector.py      # Strategy selection engine
│   ├── counterfactual_engine.py# Simulation engine
│   ├── chat_parser.py          # WeChat/SMS parser
│   ├── email_parser.py         # Email parser
│   └── version_manager.py      # Version control
├── partners/                   # Partner profiles (gitignored)
│   ├── example_xiaoyu/         # Example 1
│   └── example_mingming/       # Example 2
└── docs/                       # Documentation
    ├── PRD.md                  # Product Requirements Document
    └── partner_skill.pdf       # Technical Paper
```

---

## Data Privacy

1. **100% Local Processing**: All chat log parsing, persona building, and state inference are done locally in your sandbox or on your device.
2. **No External Storage**: The project contains no telemetry, analytics, or cloud sync code.
3. **Data Isolation**: Each partner's profile is stored independently in the `partners/{slug}/` directory.

---

## The Relationship Trilogy

This project is the final chapter of the "Relationship Trilogy":
1. **The Past**: [ex-skill](https://github.com/therealXiaomanChu/ex-skill) — Cyber-closure, reflection, and growth.
2. **The Ambiguous Phase**: [crush-skill](https://github.com/NatalieCao323/crush-skill) — Intent recognition, breaking the ice.
3. **The Present**: [partner-skill](https://github.com/NatalieCao323/partner-skill) — State inference, relationship maintenance.

---

📄 **Technical Paper**: [partner_skill.pdf](./docs/partner_skill.pdf)

*Inspired by [ex-skill](https://github.com/therealXiaomanChu/ex-skill) and [colleague-skill](https://github.com/titanwings/colleague-skill)*
