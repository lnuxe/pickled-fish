---
name: attachment-style
description: Analyze adult attachment style via conversational assessment based on ECR-R + Attached frameworks. Covers the 4 Bartholomew types (Secure, Preoccupied, Dismissive, Fearful), recommends books matched to the user's style, and provides repair strategies. Load when the user wants to understand their attachment style, analyze relationship patterns, or explore attachment theory books.
---

# Attachment Style Assessment & Book Guide

This skill administers a conversational attachment style assessment based on the two-dimensional model (anxiety × avoidance), categorizes the user into one of 4 types, and recommends tailored books and strategies.

## Theoretical Foundation

Attachment theory originated with **John Bowlby** (1969) and **Mary Ainsworth** ("Strange Situation", 1978). Adult attachment was systematized by **Bartholomew & Horowitz** (1991) into a 2×2 model based on:

- **Anxiety dimension**: Fear of rejection, abandonment, preoccupation with partner's availability
- **Avoidance dimension**: Discomfort with closeness, dependence, emotional intimacy

```
                LOW AVOIDANCE              HIGH AVOIDANCE
LOW ANXIETY  →  SECURE                     DISMISSIVE-AVOIDANT
                 (+ self, + others)         (+ self, - others)

HIGH ANXIETY →  PREOCCUPIED (Anxious)      FEARFUL-AVOIDANT
                 (- self, + others)         (- self, - others)
```

## Key Books by School

### 1. Popular Science / Self-Help
- **Attached** (Amir Levine & Rachel Heller, 2010) — The entry point. 3 types: Secure, Anxious, Avoidant. Practical dating/relationship advice. **Best for beginners.**
- **The Power of Attachment** (Diane Poole Heller, 2019) — 4 styles with somatic/body-based healing. Includes the DARe (Dynamic Attachment Re-patterning Experience) approach.
- **Wired for Love** (Stan Tatkin, 2012) — Neurobiological lens; "couple bubble" concept.

### 2. Clinical / Academic
- **Attachment in Psychotherapy** (David Wallin, 2007) — Integrates neuroscience, mentalization, mindfulness. **The clinical gold standard.**
- **Hold Me Tight** (Sue Johnson, 2008) — Emotionally Focused Therapy (EFT) for couples. 7 conversations framework.

### 3. Style-Specific
- **Insecure in Love** (Leslie Becker-Phelps, 2014) — For anxious-preoccupied readers.
- **Avoidant: How to Love (or Leave) a Dismissive Partner** (Jeb Kinnison) — Covers both avoidant types.
- **Polysecure** (Jessica Fern, 2020) — Attachment in non-monogamous structures; also excellent for understanding attachment wounds in any context.

### 4. History / Depth
- **Becoming Attached** (Robert Karen, 1994) — Sweeping history from Bowlby to modern research.

## Assessment Protocol

### Phase 1: Explain the two dimensions

Tell the user:
> "成人依恋由两个维度决定：① **依恋焦虑** — 你有多担心被抛弃/不被回应；② **依恋回避** — 你对亲密和依赖有多不舒服。两个维度交叉形成4种类型。我会各问你6-8个问题，请用1-7打分（1=完全不同意，7=完全同意）。"

### Phase 2: Anxiety dimension questions (8 items)

Ask one at a time or batch. Use these ECR-R adapted items:

1. 我担心伴侣不会像我关心TA那样关心我。
2. 我经常担心伴侣不想和我在一起。
3. 我担心伴侣一旦了解真实的我就会离开。
4. 当伴侣不在身边时，我担心TA可能对别人产生兴趣。
5. 当我对伴侣表达感受时，我害怕TA和我的感觉不一样。
6. 我经常希望伴侣对我的感情和我对TA的感情一样强烈。
7. 我担心被抛弃。
8. *反向题* 我很少担心伴侣会离开我。 (R)

### Phase 3: Avoidance dimension questions (8 items)

1. 我更喜欢不和伴侣表现得太亲近。
2. 当伴侣想和我非常亲近时，我会感到不舒服。
3. 和伴侣分享内心深处的想法和感受让我不自在。
4. 在困难时期向伴侣求助对我来说很困难。
5. 当伴侣开始亲近我时，我发现自己会退缩。
6. *反向题* 向伴侣敞开心扉让我感到舒服。 (R)
7. *反向题* 我会在需要时向伴侣求助。 (R)
8. *反向题* 和伴侣亲密让我感到自在。 (R)

Scale: 1 (strongly disagree) to 7 (strongly agree)

### Phase 4: Compute scores

Reverse-score items marked (R): `reversed = 8 - raw`

**Anxiety score** = mean of all anxiety items (with reverse-scoring applied)
**Avoidance score** = mean of all avoidance items (with reverse-scoring applied)

### Phase 5: Classify

Use the midpoint 3.5 as the cutoff:

| Condition | Type |
|-----------|------|
| Anxiety < 3.5 AND Avoidance < 3.5 | **Secure** (安全型) |
| Anxiety ≥ 3.5 AND Avoidance < 3.5 | **Preoccupied** (迷恋型/焦虑型) |
| Anxiety < 3.5 AND Avoidance ≥ 3.5 | **Dismissive-Avoidant** (疏离-回避型) |
| Anxiety ≥ 3.5 AND Avoidance ≥ 3.5 | **Fearful-Avoidant** (恐惧-回避型) |

If either score is within 0.5 of the cutoff (3.0-4.0), mention the user shows mixed traits and leans toward the classified type.

## Four Type Profiles

### Secure (安全型)
- **Self-view**: + | **Other-view**: +
- **Traits**: Comfortable with intimacy AND independence. Can ask for help. Trusts others. Handles conflict constructively.
- **Childhood**: Caregiver was consistently responsive.
- **Relationships**: Healthy balance. ~50-60% of population.
- **Book**: *Attached* (Levine) — understand others' styles + *Wired for Love* (Tatkin)

### Preoccupied / Anxious (迷恋型)
- **Self-view**: − | **Other-view**: +
- **Traits**: Craves closeness, fears rejection, can be "clingy." Hypervigilant to partner's moods. Needs frequent reassurance. Falls in love easily.
- **Childhood**: Inconsistently responsive caregiver.
- **Relationships**: "Protest behaviors" — calling/texting excessively, jealousy, playing games to get attention.
- **Core wound**: "I'm not enough."
- **Book**: *Insecure in Love* (Becker-Phelps) + *Attached* (Levine)

### Dismissive-Avoidant (疏离-回避型)
- **Self-view**: + | **Other-view**: −
- **Traits**: Highly self-sufficient. Uncomfortable with dependence. May seem cold or distant. Values independence above intimacy.
- **Childhood**: Caregiver was emotionally unavailable; learned to self-soothe.
- **Relationships**: Keeps partners at arm's length. Dismisses the importance of relationships. Uses "deactivating strategies" (finding flaws, fantasizing about the "perfect" ex).
- **Core wound**: "Others can't be relied on."
- **Book**: *Avoidant* (Kinnison) + *The Power of Attachment* (Heller)

### Fearful-Avoidant / Disorganized (恐惧-回避型)
- **Self-view**: − | **Other-view**: −
- **Traits**: Desires closeness but fears it simultaneously. Unpredictable behavior. May have experienced trauma. Deep internal conflict.
- **Childhood**: Often associated with abuse, neglect, or caregiver who was source of both comfort and fear.
- **Relationships**: Hot-cold dynamics. Wants intimacy then pushes away. Hardest to treat, but most rewarding when healed.
- **Core wound**: "I want love but it terrifies me."
- **Book**: *The Power of Attachment* (Heller) + *Attachment in Psychotherapy* (Wallin) + *Polysecure* (Fern)

## Post-Assessment: Provide Results

After classification, deliver:

1. **Type result** with anxiety/avoidance scores
2. **Personalized profile** — how this manifests in relationships
3. **Book recommendation** — top 2 books matched to type (include Chinese translations where available)
4. **Growth direction** — specific strategies:
   - Anxious → Build self-soothing, stop protest behaviors, date secure partners
   - Avoidant → Practice vulnerability in small steps, recognize deactivating strategies
   - Fearful → Therapy recommended, somatic work, gradual trust-building
   - Secure → Maintain awareness, help partners feel secure
5. **Offer** to do a deeper dive into any aspect

## Important Disclaimers

- This is a self-report screening tool, NOT a clinical diagnosis
- Attachment styles are dimensional, not categorical — most people are blends
- Attachment style can change over time with relationships and therapy
- For clinical concerns, recommend professional evaluation (AAI — Adult Attachment Interview)
- The conversational version is adapted from ECR-R; full 36-item version available at https://labs.psychology.illinois.edu/~rcfraley/measures/ecrr.htm

## References

- Bartholomew, K., & Horowitz, L. M. (1991). Attachment styles among young adults: A test of a four-category model. *JPSP, 61*(2), 226-244.
- Brennan, K. A., Clark, C. L., & Shaver, P. R. (1998). Self-report measurement of adult attachment. In J. A. Simpson & W. S. Rholes (Eds.), *Attachment theory and close relationships* (pp. 46-76).
- Fraley, R. C., Waller, N. G., & Brennan, K. A. (2000). An item-response theory analysis of self-report measures of adult attachment. *JPSP, 78*, 350-365.
- Levine, A., & Heller, R. (2010). *Attached: The new science of adult attachment*. TarcherPerigee.
- Heller, D. P. (2019). *The Power of Attachment*. Sounds True.
- Johnson, S. (2008). *Hold Me Tight*. Little, Brown Spark.
