#!/usr/bin/env python3
"""Export a WeChat 4.x conversation to chat.txt.

Sender attribution: each message row carries real_sender_id, which indexes the
message database's Name2Id table. The row is "me" when the resolved username is
your own wxid and the contact's when it is theirs; ids that resolve to nothing
(system notices) are labelled 系统 instead of being folded into a speaker. The
sender id meanings are NOT stable across databases, so the mapping is read from
the database rather than assumed.

Output format matches the downstream local-chat-pipeline:

    [YYYY-MM-DD HH:MM:SS] 我: ...
    [YYYY-MM-DD HH:MM:SS] <对方>: ...
"""
import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

TYPES = {1: "text", 3: "image", 34: "voice", 43: "video", 47: "sticker",
         49: "app", 50: "call", 10000: "system"}


def dec(x):
    return x.decode("utf-8", "replace") if isinstance(x, bytes) else str(x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True, help="decrypted message database")
    ap.add_argument("--table", required=True, help="Msg_* table for the conversation")
    ap.add_argument("--me-wxid", required=True, help="your own wxid")
    ap.add_argument("--other-wxid", required=True, help="the contact's wxid")
    ap.add_argument("--other-name", default="对方")
    ap.add_argument("--out", default="chat.txt")
    args = ap.parse_args()

    con = sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)
    con.text_factory = bytes
    cur = con.cursor()

    n2i = {}
    for rid, name in cur.execute("SELECT rowid, user_name FROM Name2Id"):
        n2i[rid] = dec(name)

    rows = list(cur.execute(
        f'SELECT local_id, create_time, real_sender_id, local_type, message_content '
        f'FROM "{args.table}" ORDER BY local_id'))
    con.close()

    lines = []
    for _lid, ct, rs, lt, mc in rows:
        when = datetime.fromtimestamp(ct).strftime("%Y-%m-%d %H:%M:%S")
        resolved = n2i.get(rs, "")
        if resolved == args.me_wxid:
            who = "我"
        elif resolved == args.other_wxid:
            who = args.other_name
        elif not resolved:
            who = "系统"
        else:
            who = resolved
        try:
            lt = int(lt)
        except Exception:  # noqa: BLE001
            lt = 0
        if lt != 1:
            body = f"[{TYPES.get(lt, 'type' + str(lt))}]"
        else:
            body = "".join(c if c.isprintable() else " " for c in dec(mc))
        body = " ".join(body.split())
        lines.append(f"[{when}] {who}: {body}")

    out = Path(args.out)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    me = sum(1 for l in lines if "] 我: " in l)
    other = sum(1 for l in lines if f"] {args.other_name}: " in l)
    print(f"wrote {len(lines)} lines -> {out}")
    print(f"  me={me}  other={other}  system/other={len(lines) - me - other}")
    if lines:
        print(f"  span: {lines[0][:19]} -> {lines[-1][:19]}")
        print("  verify this end time against the WeChat window before trusting it")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
