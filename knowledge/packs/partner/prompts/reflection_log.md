# Reflection Log Prompt

The reflection log is a living record of the relationship's evolution — conflicts resolved, lessons learned, growth observed, and moments worth remembering. It serves as both a personal archive and a data source for improving future advice.

---

## Log Entry Types

### Type 1: Conflict Resolution Entry
Created after a conflict is analyzed and resolved.

```markdown
## [Date] — Conflict: [Brief Title]

**Trigger**: [What started the conflict]
**Core Issue**: [The underlying need or fear]
**How It Resolved**: [What actually happened]
**Key Lesson**: [One sentence — what this taught about the relationship or the partner]
**Activation**: E=[x], R=1.0, F=[x] → W=[calculated]
```

### Type 2: Growth Observation Entry
Created when the user notices meaningful positive change in themselves, their partner, or the relationship dynamic.

```markdown
## [Date] — Growth: [Brief Title]

**What Changed**: [Specific behavior or pattern that shifted]
**Why It Matters**: [How this connects to a previously identified growth area]
**Evidence**: [Concrete example — something said or done]
**Next Step**: [One thing to do to reinforce this growth]
```

### Type 3: Milestone Entry
Created for significant relationship events (anniversaries, major decisions, trips, firsts).

```markdown
## [Date] — Milestone: [Brief Title]

**What Happened**: [Description of the event]
**Partner's Response**: [How they reacted — emotionally and behaviorally]
**What It Revealed**: [Something new learned about the partner or the relationship]
**Memory Tag**: E=[x], R=1.0, F=0.1 → W=[calculated]
```

### Type 4: Advice Outcome Entry
Created when the user reports back on how advice from the skill played out in reality.

```markdown
## [Date] — Advice Outcome: [Scenario Type]

**Advice Given**: [Summary of what was recommended]
**What Actually Happened**: [User's report]
**Accuracy**: [Did the advice match the partner's actual response? Y/N/Partial]
**Profile Update Needed**: [Yes/No — if yes, what to update]
```

---

## Reflection Summary

At the start of each new session, if the reflection log contains 3 or more entries, generate a brief summary:

```
Relationship Reflection Summary — [Partner Name]

Total entries: [n]
Most recent conflict resolved: [date] — [title]
Recurring theme: [pattern observed across multiple entries]
Relationship trajectory: [improving / stable / needs attention]
Recommended focus this week: [one specific suggestion]
```

---

## Instructions for Use

1. After any conflict analysis or scenario advice session, ask the user: "Would you like to add this to your reflection log?"
2. If yes, generate the appropriate entry type and append it to `reflection.md`.
3. Periodically (every 5 entries), offer to generate a Reflection Summary.
4. Use high-W entries from the reflection log to update the memory archive in `memory.md`.
