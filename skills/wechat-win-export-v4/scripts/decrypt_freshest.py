#!/usr/bin/env python3
"""Decrypt a WeChat 4.x database and prove the result is the freshest one reachable.

Why this script exists
----------------------
A tempting simplification is "decrypt the main file, then merge the WAL frames".
On the build this was written for that is actively WRONG: the main file already
holds the newest committed state, while the 4 MB WAL next to it can be a stale
generation. Merging it overwrites fresh pages with old ones - measured on a real
account, that silently rolled a conversation back six days and "lost" 749
messages. The two files even share the same mtime, so timestamps cannot tell you
which is current.

The safeguard is therefore based on the data itself, not on metadata:

  1. decrypt the main file alone, and with all WAL frames applied
  2. read the newest message timestamp and the total message row count from each
  3. keep whichever is fresher (timestamp first, row count as the tie-breaker,
     because an unrelated busy thread can make both candidates report the same
     "newest" while one is missing thousands of rows), and say so explicitly

Both candidates are kept on disk so the choice can be re-checked by hand.
"""
import argparse
import hashlib
import sqlite3
import struct
import sys
from datetime import datetime
from pathlib import Path

from Crypto.Cipher import AES

PAGE_SIZE = 4096
RESERVE = 80
IV_OFFSET = PAGE_SIZE - RESERVE              # 4016
CT_END = PAGE_SIZE - RESERVE
SALT_LEN = 16
ITERATIONS = 256000
SQLITE_MAGIC = b"SQLite format 3\x00"
VALID_BTREE_TYPES = {0x02, 0x05, 0x0A, 0x0D}
WAL_MAGIC = (0x377F0682, 0x377F0683)


def decrypt_blob(blob: bytes, passphrase: bytes) -> bytes:
    enc_key = hashlib.pbkdf2_hmac("sha512", passphrase, blob[:SALT_LEN],
                                  ITERATIONS, dklen=32)
    out = bytearray()
    for i in range(0, len(blob), PAGE_SIZE):
        page = blob[i:i + PAGE_SIZE]
        if len(page) < PAGE_SIZE:
            out.extend(page)
            continue
        pgno = i // PAGE_SIZE + 1
        iv = page[IV_OFFSET:IV_OFFSET + 16]
        if pgno == 1:
            body = AES.new(enc_key, AES.MODE_CBC, iv).decrypt(page[SALT_LEN:CT_END])
            out.extend((SQLITE_MAGIC + body).ljust(PAGE_SIZE, b"\x00"))
        else:
            out.extend(AES.new(enc_key, AES.MODE_CBC, iv)
                       .decrypt(page[:CT_END]).ljust(PAGE_SIZE, b"\x00"))
    return bytes(out)


def wal_frames(wal: Path):
    """All frames in file order. Salt rotates inside one WAL, so never stop early."""
    if not wal.exists():
        return []
    blob = wal.read_bytes()
    if len(blob) < 32 or struct.unpack(">I", blob[:4])[0] not in WAL_MAGIC:
        return []
    if struct.unpack(">I", blob[8:12])[0] != PAGE_SIZE:
        return []
    sz = 24 + PAGE_SIZE
    frames = []
    for i in range((len(blob) - 32) // sz):
        off = 32 + i * sz
        pgno = struct.unpack(">I", blob[off:off + 4])[0]
        if pgno:
            frames.append((pgno, blob[off + 24:off + sz]))
    return frames


def merge_wal(blob: bytes, frames) -> bytes:
    buf = bytearray(blob)
    for pgno, page in frames:
        off = (pgno - 1) * PAGE_SIZE
        if off + PAGE_SIZE > len(buf):
            buf.extend(b"\x00" * (off + PAGE_SIZE - len(buf)))
        buf[off:off + PAGE_SIZE] = page
    return bytes(buf)


def structural_ok(data: bytes) -> bool:
    if len(data) % PAGE_SIZE or data[:16] != SQLITE_MAGIC:
        return False
    if struct.unpack_from(">H", data, 16)[0] != PAGE_SIZE:
        return False
    pages = len(data) // PAGE_SIZE
    bad = sum(1 for pg in range(2, pages + 1, max(1, pages // 200))
              if data[(pg - 1) * PAGE_SIZE] not in VALID_BTREE_TYPES)
    return bad <= max(1, pages // 1000)


def newest_message(path: Path):
    """Newest create_time across every Msg_* table, plus the row count."""
    try:
        con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        con.text_factory = bytes
    except Exception:  # noqa: BLE001
        return None, None, "cannot open"
    newest, table, rows_total = None, None, 0
    try:
        tabs = [r[0].decode("utf-8", "replace") if isinstance(r[0], bytes) else r[0]
                for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
        for t in tabs:
            if not str(t).startswith("Msg_"):
                continue
            try:
                r = con.execute(f'SELECT count(*), max(create_time) FROM "{t}"').fetchone()
            except Exception:  # noqa: BLE001
                continue
            rows_total += r[0] or 0
            if r[1] and (newest is None or r[1] > newest):
                newest, table = r[1], t
    finally:
        con.close()
    return (datetime.fromtimestamp(newest) if newest else None), table, rows_total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True)
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    passphrase = bytes.fromhex(args.key)
    src = Path(args.db)
    blob = src.read_bytes()
    frames = wal_frames(src.with_name(src.name + "-wal"))

    candidates = [("main-only", decrypt_blob(blob, passphrase))]
    if frames:
        candidates.append(
            (f"wal-merged({len(frames)}f)", decrypt_blob(merge_wal(blob, frames), passphrase)))

    results = []
    for label, data in candidates:
        p = Path(args.out).with_name(Path(args.out).stem + f".{label.split('(')[0]}.dec")
        p.write_bytes(data)
        ok = structural_ok(data)
        newest, table, rows = newest_message(p)
        results.append({"label": label, "path": p, "ok": ok,
                        "newest": newest, "table": table, "rows": rows,
                        "wal_frames": len(frames) if "wal" in label else 0})
        stamp = newest.strftime("%Y-%m-%d %H:%M:%S") if newest else "n/a"
        print(f"  [{label:<16}] structural={'ok' if ok else 'FAIL'} "
              f"newest={stamp} rows={rows}")

    usable = [r for r in results if r["ok"] and r["newest"]]
    if not usable:
        print("\nNo candidate decrypted into a usable database.")
        return 2

    # Newest timestamp decides first; when two candidates report the same newest
    # message (common, because one unrelated busy thread can dominate the max),
    # the total row count breaks the tie - a stale WAL merge loses messages
    # wholesale, which shows up as thousands of missing rows.
    best = max(usable, key=lambda r: (r["newest"], r["rows"] or 0))
    final = Path(args.out)
    final.write_bytes(best["path"].read_bytes())
    print(f"\nchosen: {best['label']}  "
          f"(newest {best['newest'].strftime('%Y-%m-%d %H:%M:%S')}, rows {best['rows']})")
    print(f"wrote : {final}")

    rejected = [r for r in results if r is not best]
    for r in rejected:
        if r["newest"] and r["rows"] is not None:
            if r["newest"] < best["newest"] or (r["rows"] or 0) < (best["rows"] or 0):
                print(f"\nNOTE: '{r['label']}' was rejected: newest="
                      f"{r['newest'].strftime('%Y-%m-%d %H:%M:%S')} rows={r['rows']} "
                      f"(vs {best['newest'].strftime('%Y-%m-%d %H:%M:%S')} / {best['rows']})")
    if any(r["label"].startswith("wal-merged") and r is not best for r in results):
        print("      Merging the WAL produced STALER data here. The sidecar can be a"
              "\n      stale generation sharing the main file's mtime - do not re-add"
              "\n      unconditional WAL merging.")
    print("\nVERIFY: compare that timestamp with the newest message shown in WeChat.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
