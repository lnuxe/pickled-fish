# Limitations

Reading this file before making strong claims from ChatRel's output is
non-optional. The tool is designed to surface **patterns**, not
**diagnoses**.

## 1. Validity

* **No gold standard.** Nothing here has been validated against
  self-report measures (ECR-R, RAS, DAS, etc.) or clinical interviews.
* **n = 1 relationships.** Every analysis reflects one dyad's language,
  not a population. Cross-dyad generalization is unjustified.
* **Proxy ceiling.** Lexicon-based scoring is known to under-perform
  ML embedding approaches on emotion/sentiment tasks by 10–30 %.
  Contextual sarcasm, irony, and playful inversion ("I hate you" =
  affection in some couples) will mislead the counts.

## 2. Interpretation risks

* **Labelling a person as "Anxious-Preoccupied"** based on one
  behavioral map is statistically fragile and relationally harmful.
  Attachment is context-sensitive and changes with safety.
* **The couple-dynamic table** (anxious × avoidant → "trap") is a known
  empirical pattern but **not destiny**. Many such couples do fine with
  awareness and repair practices; some secure×secure couples fall
  apart.
* **Forecasts are not predictions.** Damped linear extrapolation with
  mean reversion is a descriptive scenario generator. It does not
  compute probabilities. Nobody should decide a breakup based on it.
* **Rising EWS** (variance + AR(1)) has face validity but its
  specificity in relational time-series is unvalidated. A confirmed
  warning ≠ an imminent break.

## 3. Text-only blind spots

ChatRel only sees what was typed. It does not see:

* Face-to-face time (often *more* important than text for closeness).
* Voice messages' prosody (Gottman's original "contempt" was vocal).
* Physical affection, gift-giving, parallel presence, service acts.
* Private journals, third-party complaints, conversations with friends.

A relationship that looks cool in text can be warm in person, and vice
versa. A low IDS may mean "we see each other every day, we barely text"
rather than "we're distant."

## 4. Lexicon coverage

* **Mandarin online speech only.** Classical / formal / dialect / local
  slang is under-covered.
* **Codeswitched text.** Chinese-English mixed messages partially
  matched.
* **Stickers, emojis, images, voice, video calls** — counted
  categorically but content is not analyzed.
* **Negation windows.** `不要道歉` ("don't apologize") matches
  `道歉` (apology) because the detector is phrase-based, not
  dependency-parsed. Event reconstruction may double-count.

## 5. Sentiment tool limits

Where SnowNLP sentiment is used (the original `analyzers.depth` /
earlier analysis pipelines; not the core of the 0.1 release), remember:

* SnowNLP was trained on e-commerce reviews — a very different
  distribution from intimate chat.
* Short messages ("嗯") return unstable scores.
* Positive / negative binary misses emotional complexity.

## 6. The ethics of analyzing someone

* The partner consented to *sending* the messages. They did not
  consent to having their language statistically modeled.
* Showing a partner their "attachment score" can be interpreted as an
  ambush rather than shared curiosity. Discuss patterns, not numbers.
* Never publish real messages, real user IDs, or identifiable scores.
  ChatRel's `.gitignore` blocks the obvious files; you must be
  responsible for the rest.

## 7. Reproducibility

* Weights (IDS composition, forecast damping, event thresholds) are
  **heuristic**. They have not been tuned against a labeled dataset.
* Random sampling (e.g., memory book "Meeting" chapter) uses fixed
  seeds but changes if you edit the code.
* Time-zone handling assumes timestamps are consistent — if your
  export mixes UTC and local time, weekly buckets will smear across
  days.

## 8. What ChatRel is good for

Within these limits, ChatRel is a reasonable way to:

* Scan a long history for **pattern shifts** you hadn't noticed
  (ritual decline, response-time asymmetry, vocabulary shrinking).
* Generate **conversation starters** with your partner — not as
  "science says…" but as "huh, our late-night chat dropped 40 %
  since March, does that track for you?"
* Create a **keepsake** (the memory book) of the relationship's
  language evolution.
* Serve as a pedagogical tool for relationship frameworks, grounded
  in your own data instead of abstract examples.

Outside these uses, treat every claim as a hypothesis, not a finding.
