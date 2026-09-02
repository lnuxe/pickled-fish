# Lexicon reference

Every numerical score in ChatRel derives from phrase counts against
hand-curated Chinese lexicons. This page is the quick index.

| Module | Key sets |
|---|---|
| [`lexicons/depth.py`](../src/chatrel/lexicons/depth.py) | Sternberg proxies (intimacy/passion/commitment), social-penetration layers, rituals, Knapp decline markers, Pennebaker pronoun/cognition/affect, laugh-intensity helper |
| [`lexicons/attachment.py`](../src/chatrel/lexicons/attachment.py) | ECR-R anxiety & avoidance sub-categories, secure markers, Gottman four horsemen, positive/negative affect |
| [`lexicons/conflict.py`](../src/chatrel/lexicons/conflict.py) | Anger / blame / threat / cry / stonewall / apology / repair / reconcile — with weight per category |
| [`lexicons/external.py`](../src/chatrel/lexicons/external.py) | Ex-partner / suitor / rival / suspicion / jealousy / possessive, and defense side (exclusivity / trust / reassurance / we-ness / boundary), and general stressors |
| [`lexicons/stopwords.py`](../src/chatrel/lexicons/stopwords.py) | Minimal Chinese stopword list |

## Design decisions

A few false-positive traps were found during iterative testing on a
real 136 k-message dataset; the fixes are *baked in* and documented
inline:

| Exclusion | Reason |
|---|---|
| `笑死 / 笑死人` not in CONTEMPT | In contemporary Chinese online speech these are overwhelmingly "LOL", not contempt. |
| `醋` (single char) not in JEALOUSY | Matches food references like `米醋 / 加醋`. Only compound forms (`吃醋` etc.) are retained. |
| `呜呜 / 呜呜呜` not in CRY_DISTRESS | In intimate chat these are usually playful whining, not distress. |
| `是不是 / 有没有` not in SUSPICION | Extremely common general question patterns. Only specific phrases (`是不是还有别人`) are kept. |
| `我的` not in POSSESSIVE | Matches almost every message; too generic. |
| `喜欢我 / 喜欢你` not in SUITOR | Standard romantic chatter between partners, not external threat. |

## Extending the lexicons

Each file uses plain Python `set[str]` constants. To add new phrases,
append to the appropriate set and open a PR. If adding a completely new
category, also:

1. Add it to the `ALL_DIMS` mapping at the bottom of the module.
2. If the category belongs to an aggregate axis (e.g., a new anxiety
   sub-facet), append its key to the appropriate group list
   (e.g., `ANXIETY_GROUPS`).
3. Document the theoretical source in
   [`docs/methodology.md`](methodology.md).

## Localization

English / Japanese / Spanish / etc. lexicons are welcome. The suggested
structure is `lexicons/depth_en.py` (mirroring the same set names) and a
runtime switch in `ALL_DIMS`. An `adapters/` fork for locale-specific
signals (e.g., Japanese 敬語 vs casual forms) would be a valuable
contribution.
