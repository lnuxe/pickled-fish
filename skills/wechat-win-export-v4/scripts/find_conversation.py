#!/usr/bin/env python3
"""Locate the message table that holds a given contact's conversation.

Do not assume the table is named Msg_<MD5(wxid)>: on the build this was written
for that hash does not correspond to any simple digest of the wxid, so guessing it
yields "no messages" rather than an error.

Reliable route, used here:
  1. resolve the contact in contact.db (username / remark / nick_name)
  2. read Name2Id inside the message database to find the row id for that username
  3. pick the Msg_* table whose real_sender_id values include that id

Also reports the target table's newest timestamp, which is the check that proves
the decryption is current rather than stale.
"""
import argparse
import json
import sqlite3
from datetime import datetime
from pathlib import Path


def dec(x):
    return x.decode("utf-8", "replace") if isinstance(x, bytes) else str(x)


def find_contact(contact_db: Path, needle: str):
    con = sqlite3.connect(f"file:{contact_db}?mode=ro", uri=True)
    con.text_factory = bytes
    cur = con.cursor()
    cols = [dec(c[1]) for c in cur.execute("PRAGMA table_info(contact)")]
    hits = []
    it = cur.execute("SELECT * FROM contact")
    while True:
        try:
            row = next(it)
        except StopIteration:
            break
        except Exception:  # noqa: BLE001
            break                       # corrupt cell: stop rather than crash
        vals = [dec(v) for v in row]
        if any(needle in v for v in vals):
            hits.append(dict(zip(cols, vals)))
            if len(hits) >= 5:
                break
    con.close()
    return hits


def tables(con):
    return [dec(r[0]) for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contact-db", required=True)
    ap.add_argument("--message-db", required=True)
    ap.add_argument("--name", required=True, help="remark / nickname / alias to find")
    ap.add_argument("--out", default="conversation.json")
    args = ap.parse_args()

    found = find_contact(Path(args.contact_db), args.name)
    print(f"contact matches: {len(found)}")
    for f in found[:3]:
        print(f"  username={f.get('username')} remark={f.get('remark')} "
              f"nick={f.get('nick_name')} alias={f.get('alias')}")
    if not found:
        return 2

    targets = {f.get("username") for f in found if f.get("username")}
    con = sqlite3.connect(f"file:{args.message_db}?mode=ro", uri=True)
    con.text_factory = bytes
    cur = con.cursor()

    id_of = {}
    try:
        for rid, name in cur.execute("SELECT rowid, user_name FROM Name2Id"):
            n = dec(name)
            if n in targets:
                id_of[rid] = n
    except Exception as e:  # noqa: BLE001
        print(f"Name2Id unreadable: {e}")
    print(f"message-db ids for target: {id_of}")

    best = None
    for t in tables(con):
        if not str(t).startswith("Msg_"):
            continue
        try:
            senders = {r[0] for r in cur.execute(
                f'SELECT DISTINCT real_sender_id FROM "{t}"')}
        except Exception:  # noqa: BLE001
            continue
        if id_of and set(id_of) & senders and len(senders) <= 3:
            row = cur.execute(
                f'SELECT count(*), min(create_time), max(create_time) FROM "{t}"').fetchone()
            best = {"table": t, "rows": row[0],
                    "senders": {k: id_of.get(k, k) for k in senders},
                    "oldest": datetime.fromtimestamp(row[1]).strftime("%Y-%m-%d %H:%M:%S") if row[1] else None,
                    "newest": datetime.fromtimestamp(row[2]).strftime("%Y-%m-%d %H:%M:%S") if row[2] else None}
            break
    con.close()

    Path(args.out).write_text(json.dumps(best, ensure_ascii=False, indent=1),
                              encoding="utf-8") if best else None
    print(f"\nconversation table: {best}")
    if best:
        print("\nIMPORTANT: compare 'newest' with the latest message visible in the"
              "\nWeChat window. If they disagree, the decryption is stale - most often"
              "\nbecause stale WAL frames were merged over a newer main file.")
    return 0 if best else 1


if __name__ == "__main__":
    raise SystemExit(main())
