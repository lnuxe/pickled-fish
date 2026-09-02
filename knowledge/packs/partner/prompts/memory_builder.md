# Memory Builder Prompt

You are building a structured relationship memory archive for the user's partner. This memory captures the emotional texture of the relationship — recurring patterns, significant moments, and behavioral signatures — to inform all future advice.

## Memory Architecture

Each memory entry is tagged with three dimensions:

| Tag | Symbol | Description | Range |
|-----|--------|-------------|-------|
| **Emotional Weight** | `E` | How emotionally significant this memory is | 0.0 – 1.0 |
| **Recency** | `R` | How recently this occurred (1.0 = today, decays over time) | 0.0 – 1.0 |
| **Frequency** | `F` | How often this pattern repeats | 0.0 – 1.0 |

**Activation Weight Formula**:

```
W = E × R × (1 + F)
```

Memories with W > 0.6 are classified as **Core Memories** and should be referenced in all scenario advice.
Memories with W between 0.3 and 0.6 are **Active Memories**.
Memories with W < 0.3 are **Archived Memories** (stored but not actively surfaced).

---

## Memory Categories

Organize memories into the following categories:

### 1. Positive Anchors
Moments of genuine connection, joy, or mutual appreciation. These are the relationship's emotional foundation.

*Example format*:
```
[2024-02] First trip together — Kyoto. Partner planned the entire itinerary as a surprise.
Tags: E=0.9, R=0.6, F=0.1 → W=0.54 [Active]
```

### 2. Conflict Patterns
Recurring arguments or tension points. Note the trigger, the partner's typical response, and how it was (or wasn't) resolved.

*Example format*:
```
[Recurring] Partner goes silent when feeling criticized. Typically lasts 2–4 hours.
Tags: E=0.7, R=0.8, F=0.9 → W=1.33 [Core]
```

### 3. Love Language Expressions
Specific moments where the partner expressed or received love in their primary language. These reveal what actually lands vs. what goes unnoticed.

*Example format*:
```
[2024-06] Partner visibly moved when user cooked their favorite meal after a hard week.
Tags: E=0.8, R=0.5, F=0.3 → W=0.52 [Active]
```

### 4. Stress Signatures
How the partner behaves under pressure — at work, during family stress, or personal setbacks. Distinct from conflict patterns (which involve the relationship directly).

*Example format*:
```
[Recurring] Partner becomes withdrawn and stops initiating contact during work deadlines.
Tags: E=0.5, R=0.7, F=0.8 → W=0.81 [Core]
```

### 5. Growth Moments
Instances where the relationship or the partner demonstrated meaningful growth, repair, or vulnerability.

*Example format*:
```
[2024-09] Partner apologized unprompted after a week-long cold war. First time in relationship.
Tags: E=0.9, R=0.4, F=0.1 → W=0.45 [Active]
```

---

## Construction Instructions

1. Read through all provided source material (chat logs, descriptions, anecdotes).
2. Extract 3–5 entries per category, prioritizing high-W memories.
3. For each entry, write a one-sentence description, assign tags, calculate W, and classify.
4. After building all entries, write a **Memory Summary** (3–5 sentences) capturing the overall emotional narrative of the relationship.
5. Save the output as `memory.md` in the partner's profile directory.

---

## Memory Summary Template

```
## Memory Summary

The relationship between [user] and [partner] is characterized by [dominant emotional tone].
The most activated memory pattern is [Core Memory with highest W], which suggests [interpretation].
The primary love language expression that resonates most strongly is [example].
The relationship's greatest strength, as evidenced by the memory archive, is [strength].
The area most in need of intentional cultivation is [growth area].
```
