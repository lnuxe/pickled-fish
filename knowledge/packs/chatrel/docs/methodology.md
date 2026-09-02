# Methodology

Every numeric output in ChatRel is derived from matching Chinese phrase
lexicons against message text and aggregating the counts with specific
weights. This document lists which lexicon maps to which framework, the
weighting and normalization choices, and the source literature.

## 1. Sternberg Triangular Theory of Love

> **Sternberg, R. J.** (1986). *A triangular theory of love.* Psychological
> Review, 93(2), 119–135.

Love is decomposed into three separable components:

| Component | ChatRel proxy |
|---|---|
| **Intimacy** — bondedness, self-disclosure, emotional support | `disclosure_medium` ∪ `disclosure_deep` ∪ `care_support` |
| **Passion** — romantic, physical arousal | `love_explicit` ∪ `longing` ∪ `heart_flutter` ∪ `physical_affection` |
| **Commitment** — decision to maintain the relationship | `future_together` ∪ `relationship_terms` ∪ `marriage_terms` ∪ `exclusivity` ∪ `devotion` |

Per-week per-role scoring: hit counts are normalized by messages-per-week
(per-1000-message rate), `log1p`-squashed to tame heavy tails, and
min-max scaled to 0–100 across the chat's lifespan. The score is a
**relative indicator within this chat**, not absolute.

**Composite Intimacy Depth Score (IDS)**:

    IDS = 0.35·Intimacy + 0.30·Passion + 0.20·Commitment + 0.15·Ritual

Weights are heuristic — higher on intimacy because empirical literature
(Acker & Davis, 1992; Lemieux & Hale, 1999) consistently finds intimacy
most predictive of relationship quality. Ritual (morning/night/check-in
rate per week) is included because daily availability is a stronger
predictor of long-term satisfaction than peak affection.

## 2. Knapp Relational Development Model

> **Knapp, M. L.** (1978). *Social intercourse: From greeting to goodbye.*
> Boston: Allyn & Bacon.

Ten-stage model (five "coming-together", five "coming-apart"). ChatRel
anchors the first four stages by first-occurrence language markers:

| Stage | Anchor |
|---|---|
| Initiating | start of chat |
| Experimenting | first morning/night greeting |
| Intensifying | first `爱你` (love declaration) |
| Integrating | first `我们以后` / `等我们` (shared-future language) |
| Bonding | first marriage/forever language |

"Coming-apart" stages are represented by lexicons (`decline_*`) but not
used for phase assignment — language alone cannot distinguish a playful
rant from actual differentiation.

## 3. Altman & Taylor Social Penetration Theory

> **Altman, I., & Taylor, D. A.** (1973). *Social penetration: The
> development of interpersonal relationships.* New York: Holt, Rinehart &
> Winston.

Self-disclosure grows in **breadth** (topic variety) and **depth**
(surface → core). ChatRel slices disclosure into three layers:

| Layer | Examples |
|---|---|
| Shallow | 我今天、我刚 (factual, recent) |
| Medium | 我觉得、我想 (opinions, preferences) |
| Deep | 我害怕、我其实、我小时候、只有你知道 (vulnerability, history, secrets) |

Rising deep-layer share over time corresponds to Altman–Taylor's core
penetration and is consistently associated with stronger relationship
quality in empirical work (Laurenceau et al., 1998; Sprecher &
Hendrick, 2004).

## 4. ECR-R Attachment + Bartholomew Four Categories

> **Fraley, R. C., Waller, N. G., & Brennan, K. A.** (2000). *An item
> response theory analysis of self-report measures of adult attachment.*
> Journal of Personality and Social Psychology, 78(2), 350–365.
>
> **Bartholomew, K., & Horowitz, L. M.** (1991). *Attachment styles among
> young adults: A test of a four-category model.* Journal of Personality
> and Social Psychology, 61(2), 226–244.

ECR-R is a two-dimensional self-report scale (Anxiety, Avoidance).
ChatRel translates each dimension into a **behavioral lexicon**:

### Anxiety (fear of abandonment, need for reassurance)

1. Reassurance-seeking (`anx_reassurance`): 你爱我吗, 你在吗
2. Hypervigilance (`anx_hypervig`): 怎么还不回, 为什么不理我
3. Protest (`anx_protest`): 求你, 别走, 不要离开
4. Self-devaluation (`anx_self_dep`): 都怪我, 我是不是很烦
5. Clinginess (`anx_cling`): 好想你, 舍不得, 不想挂

### Avoidance (discomfort with closeness, over-independence)

1. Minimization (`avo_minimize`): 随便, 算了, 没事
2. Deflection (`avo_deflect`): 不想说, 懒得说
3. Distance (`avo_distance`): 自己来, 我一个人, 不需要
4. Close-outs (`avo_close_out`): 睡了, 去忙了, 下次吧

Each dimension's 0–100 score is `log1p(hits_per_1k_msgs) × 18`, clamped.
Bartholomew's four-category type is assigned by quadrant using the
couple's **median** as threshold — this compares partners to each other,
not to a population norm.

### Important caveat

No language-based proxy can replace a self-report attachment scale.
Avoidant partners specifically *under-report verbally* — their "silence"
is the signal. ChatRel's short-reply-ratio and slow-response-ratio are
included as behavioral cross-checks.

## 5. Gottman 5:1 Magic Ratio + Four Horsemen

> **Gottman, J. M.** (1994). *Why marriages succeed or fail.* New York:
> Simon & Schuster.
>
> **Gottman, J. M., & Levenson, R. W.** (1992). *Marital processes
> predictive of later dissolution.* Journal of Personality and Social
> Psychology, 63(2), 221–233.

Gottman's research on hundreds of videotaped couple interactions found:

* Stable couples exchange roughly **5 positive interactions per 1
  negative**. Below that, satisfaction drops; below 1:1, dissolution
  risk is very high.
* **Four horsemen** of relational apocalypse (in ascending lethality):
  Criticism → Contempt → Defensiveness → Stonewalling. *Contempt* is
  Gottman's single strongest individual predictor of divorce.

ChatRel counts positive and negative affect tokens per week to compute
P:N ratio, and tracks horseman phrases as separate time series.

**Critical caveat**: Gottman's "contempt" was detected via facial
expressions and vocal tone, not text. ChatRel's text-only proxy
*deliberately excludes* the phrase `笑死` (lmao) from the contempt
lexicon — in modern Chinese online speech it's humor, not contempt.
False-positive rates for all horsemen are likely high; use as
**relative change indicator**, not absolute diagnosis.

## 6. Critical Slowing / Early-Warning Signals

> **Scheffer, M., Bascompte, J., Brock, W. A., et al.** (2009).
> *Early-warning signals for critical transitions.* Nature, 461, 53–59.

Before regime shifts in ecological, epidemiological, and psychological
systems, three statistical signatures often rise:

1. **Variance** — fluctuations amplify
2. **Lag-1 autocorrelation (AR(1))** — the system gets "stuck" in
   states, recovers more slowly from perturbation
3. **Skewness** (not implemented) — asymmetric departures from mean

ChatRel computes 6-week rolling variance and AR(1) of the composite IDS,
and flags a warning if both slopes are positive. Application of EWS to
relational dynamics (vs. ecological/epidemiological) is still
exploratory (van de Leemput et al., 2014, explored this for
depression), so treat it as a hypothesis generator.

## 7. LIWC (Chinese proxy)

> **Pennebaker, J. W., Boyd, R. L., Jordan, K., & Blackburn, K.** (2015).
> *The development and psychometric properties of LIWC2015.*

LIWC isn't a theory — it's a dictionary that slots words into cognitive
/ affective / social / temporal categories, and has decades of empirical
work linking these rates to personality, health, and social outcomes. A
few findings that ChatRel's lexicons build on:

* **First-person singular** (`我`) correlates with depression and
  self-focus; couples' use of `我们` correlates with relationship
  satisfaction (Slatcher et al., 2008; Rentscher et al., 2013).
* **Cognitive process words** (`因为`, `觉得`, `希望`) signal active
  sense-making vs. pure reactive venting.
* **Tentative words** (`好像`, `可能`) signal uncertainty; **certain
  words** (`肯定`, `一定`) signal confidence / rigidity.

The simplified Chinese LIWC (SC-LIWC) developed by Gao, Hao, Li, Gao &
Zhu (2013) was a reference for category curation but ChatRel's lexicons
are hand-written rather than a translation.

---

## Reproducibility & validity notes

* **Sample size.** ChatRel is typically run on a single dyad's messages
  (n=1 relationship). No external validity is claimed.
* **No ground truth.** Participants haven't self-reported attachment
  scale scores, relationship satisfaction, etc. Correlations between
  ChatRel proxies and real scales have not been validated. This is the
  #1 limitation — see [`limitations.md`](limitations.md).
* **Lexicons are coverage-incomplete.** They target Mandarin online
  chat. Regional speech, dialect, and code-switched (Chinese/English)
  patterns may be under-captured.
* **Iterative refinement.** False positives caught during development
  (e.g., `笑死` in contempt; `醋` in jealousy; `呜呜` in cry-distress)
  have been explicitly excluded with in-file rationale comments.
