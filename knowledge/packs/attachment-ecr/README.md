> 🌐 [中文文档](README.zh-CN.md) | **English**

# 🧠 Hermes Attachment Style

A **Hermes Agent skill** that administers a conversational adult attachment style assessment based on the ECR-R (Experiences in Close Relationships-Revised) framework.

## What it does

- **Assesses** your attachment style through a 16-item conversational questionnaire
- **Classifies** you into one of 4 Bartholomew types: Secure, Preoccupied, Dismissive-Avoidant, or Fearful-Avoidant
- **Recommends** books matched to your attachment style
- **Provides** growth strategies for each type

## The 2×2 Model

```
                LOW AVOIDANCE              HIGH AVOIDANCE
LOW ANXIETY  →  SECURE                     DISMISSIVE-AVOIDANT
                 (+ self, + others)         (+ self, - others)

HIGH ANXIETY →  PREOCCUPIED (Anxious)      FEARFUL-AVOIDANT
                 (- self, + others)         (- self, - others)
```

## Books Covered

| Book | Author | Focus |
|------|--------|-------|
| *Attached* | Levine & Heller | 3-type model, dating advice |
| *The Power of Attachment* | Diane Poole Heller | 4 styles, somatic healing |
| *Attachment in Psychotherapy* | David Wallin | Clinical, neuroscience-backed |
| *Hold Me Tight* | Sue Johnson | EFT for couples |
| *Insecure in Love* | Becker-Phelps | Anxious attachment self-help |
| *Avoidant* | Jeb Kinnison | Dismissive partner handbook |
| *Polysecure* | Jessica Fern | Attachment + non-monogamy |
| *Becoming Attached* | Robert Karen | History of attachment theory |

## Usage

Load the skill in Hermes Agent, then say "analyze my attachment style":

```
> analyze my attachment style
```

The agent will walk you through 16 questions (1-7 scale), compute your anxiety and avoidance scores, and deliver your type profile with personalized recommendations.

## Installation

Copy `SKILL.md` into your Hermes Agent skills directory:

```bash
cp SKILL.md ~/.hermes/skills/attachment-style/
```

## Disclaimer

This is a self-report screening tool adapted from academic instruments (ECR-R by Fraley, Waller & Brennan, 2000). It is **not a clinical diagnosis**. For clinical concerns, seek a licensed therapist.

## References

- Bartholomew, K., & Horowitz, L. M. (1991). Attachment styles among young adults. *JPSP, 61*(2), 226-244.
- Fraley, R. C., Waller, N. G., & Brennan, K. A. (2000). An item-response theory analysis of self-report measures of adult attachment. *JPSP, 78*, 350-365.
- Levine, A., & Heller, R. (2010). *Attached*. TarcherPerigee.
- Heller, D. P. (2019). *The Power of Attachment*. Sounds True.

## License

MIT
