# Pack specification

## Layout

```
knowledge/custom/<id>/
  PACK.md           # required
  SKILL.md          # or index.md
  LICENSE           # recommended
  references/       # optional long-form
  index.md          # optional directory summary
```

## PACK.md frontmatter (YAML in HTML comment or leading --- block)

Required fields: `id`, `name`, `license`, `entry`, `triggers` (list).

Optional: `source` (upstream URL), `copyright`, `priority` (number, higher wins on tie).

## Writing good triggers

Use concrete Chinese/English phrases users would say, not vague “relationship help”.

## Privacy

Do not put real chat logs, phone numbers, or passphrases inside packs committed publicly.
