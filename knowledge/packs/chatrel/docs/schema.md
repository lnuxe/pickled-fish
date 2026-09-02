# Chat schema

ChatRel reads a single JSON file describing a two-person chat. The
format is deliberately minimal so adapters from arbitrary platforms
are easy to write.

## Canonical format

```json
{
  "me_name": "Alex",
  "partner_name": "Sam",
  "messages": [
    {"ts": 1700000000, "role": "me",      "text": "hi",     "type": "text"},
    {"ts": 1700000010, "role": "partner", "text": "hey!",   "type": "text"},
    {"ts": 1700000020, "role": "me",      "text": "",       "type": "sticker"}
  ]
}
```

### Top-level

| Key | Type | Required | Description |
|---|---|---|---|
| `me_name` | string | optional (default `"Me"`) | Display name of the "me" side of the conversation. |
| `partner_name` | string | optional (default `"Partner"`) | Display name of the other side. |
| `messages` | array | **required** | List of messages, chronological (loader re-sorts by `ts`). |

### Message

| Key | Type | Required | Description |
|---|---|---|---|
| `ts` | number | **required** | Unix timestamp in seconds (int or float). |
| `role` | `"me"` \| `"partner"` | **required** | Who sent it. |
| `text` | string | optional (default `""`) | Message text. Empty allowed for non-text types. |
| `type` | string | optional (default `"text"`) | One of `"text"`, `"image"`, `"voice"`, `"sticker"`, `"video"`, `"voice_call"`, `"app_link_file"`, `"system"`, `"contact_card"`. |

## Notes

* All text analysis currently operates only on messages with
  `type == "text"` and non-empty `text`. Other types are counted
  categorically for volume metrics.
* Timestamps **must** be in seconds. Milliseconds will produce nonsensical
  weekly buckets. (If your source is ms, divide by 1000 before writing.)
* `role` must be exactly `"me"` or `"partner"`. Group chats are out of
  scope — this tool models dyadic relationships.
* `text` can contain any Unicode, including emoji, URLs, and mixed
  Chinese/English. Line breaks are preserved.

## Validation

```python
from chatrel import load_chat
chat = load_chat("chat.json")  # raises ValueError on malformed input
print(len(chat), "messages", len(chat.text_messages()), "text")
```

The loader:

1. Parses JSON.
2. Validates each message (raises `ValueError` with the offending index).
3. Sorts by `ts` ascending.
4. Returns a `chatrel.schema.Chat` dataclass.

## Minimum useful dataset

Most analyzers expect **at least a few weeks** of data — weekly rolling
statistics degenerate on short chats. Synthetic demo data ships at 90
days / ~2 000 messages; the full pipeline runs fine on anything above
~1 000 text messages spanning 30+ days.
