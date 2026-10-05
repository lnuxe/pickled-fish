#!/usr/bin/env python3
"""Decrypt a WeChat 4.1+ SQLCipher database, with self-checks that catch the
parameter mistakes which otherwise look like success.

Verified on WeChat 4.1.15.13 (Windows). The values below are not defaults taken
from documentation; each was confirmed by parsing the result, because several
plausible-looking alternatives produce output that decrypts "cleanly" but is
wrong:

  * reserve is 80, and within it the IV comes FIRST (offset 4016) and the 64-byte
    HMAC tag last. Using the opposite order leaves page 1 looking perfect while
    every later page is random bytes.
  * page 1 ciphertext is only [16:4016]; the plaintext is the SQLite magic plus
    the decrypted body and MUST be padded back to a full page, or every
    subsequent page is shifted and the file is unreadable.

Self-checks are run on every output: page-size alignment, page-1 header fields,
b-tree type bytes on sampled pages, and a real sqlite3 schema read.
"""
import argparse
import hashlib
import sqlite3
import struct
import sys
from pathlib import Path

from Crypto.Cipher import AES

PAGE_SIZE = 4096
RESERVE = 80
IV_OFFSET = PAGE_SIZE - RESERVE              # 4016
CT_END = PAGE_SIZE - RESERVE                 # 4016
SALT_LEN = 16
ITERATIONS = 256000
SQLITE_MAGIC = b"SQLite format 3\x00"
VALID_BTREE_TYPES = {0x02, 0x05, 0x0A, 0x0D}


def derive_key(passphrase: bytes, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha512", passphrase, salt, ITERATIONS, dklen=32)


def derive_mac_key(enc_key: bytes, salt: bytes) -> bytes:
    mac_salt = bytes(b ^ 0x3A for b in salt)
    return hashlib.pbkdf2_hmac("sha512", enc_key, mac_salt, 2, dklen=32)


def decrypt_page(page: bytes, enc_key: bytes, pgno: int) -> bytes:
    """Decrypt one page, always returning exactly PAGE_SIZE bytes."""
    iv = page[IV_OFFSET:IV_OFFSET + 16]
    if pgno == 1:
        body = AES.new(enc_key, AES.MODE_CBC, iv).decrypt(page[SALT_LEN:CT_END])
        return (SQLITE_MAGIC + body).ljust(PAGE_SIZE, b"\x00")
    body = AES.new(enc_key, AES.MODE_CBC, iv).decrypt(page[:CT_END])
    return body.ljust(PAGE_SIZE, b"\x00")


def decrypt_database(blob: bytes, passphrase: bytes) -> bytes:
    enc_key = derive_key(passphrase, blob[:SALT_LEN])
    out = bytearray()
    for i in range(0, len(blob), PAGE_SIZE):
        page = blob[i:i + PAGE_SIZE]
        if len(page) < PAGE_SIZE:
            out.extend(page)                 # trailing partial page: keep as-is
            continue
        out.extend(decrypt_page(page, enc_key, i // PAGE_SIZE + 1))
    return bytes(out)


def verify(data: bytes) -> dict:
    """Cheap structural checks; these are what caught the wrong-IV mistake."""
    report = {"ok": False, "reasons": []}
    if len(data) % PAGE_SIZE:
        report["reasons"].append(f"size {len(data)} not page aligned")
        return report
    if data[:16] != SQLITE_MAGIC:
        report["reasons"].append("missing SQLite magic on page 1")
        return report
    page_size = struct.unpack_from(">H", data, 16)[0]
    if page_size != PAGE_SIZE:
        report["reasons"].append(f"header page_size={page_size}")
        return report
    declared = struct.unpack_from(">I", data, 28)[0]
    actual = len(data) // PAGE_SIZE
    if declared and declared != actual:
        report["reasons"].append(f"header db_size={declared} but file has {actual} pages")

    # sample pages: the first byte of every later page must be a b-tree type
    bad = 0
    sampled = 0
    for pg in range(2, actual + 1, max(1, actual // 200)):
        sampled += 1
        if data[(pg - 1) * PAGE_SIZE] not in VALID_BTREE_TYPES:
            bad += 1
    if sampled and bad > sampled * 0.2:
        report["reasons"].append(f"{bad}/{sampled} sampled pages have invalid b-tree type")
    report["ok"] = not report["reasons"]
    report["pages"] = actual
    report["sampled_bad"] = bad
    return report


def schema_readable(path: Path) -> tuple[bool, str]:
    try:
        con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        n = con.execute("SELECT count(*) FROM sqlite_master").fetchone()[0]
        con.close()
        return True, f"{n} schema objects"
    except Exception as e:  # noqa: BLE001
        return False, str(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True, help="64 hex chars from the capture")
    ap.add_argument("--db", required=True, help="encrypted .db file")
    ap.add_argument("--out", required=True, help="decrypted output path")
    args = ap.parse_args()

    passphrase = bytes.fromhex(args.key)
    src = Path(args.db)
    blob = src.read_bytes()
    print(f"db   : {src}  ({len(blob):,} bytes)")
    print(f"salt : {blob[:16].hex()}")

    data = decrypt_database(blob, passphrase)
    rep = verify(data)
    for r in rep["reasons"]:
        print(f"  [check] {r}")
    print(f"  pages={rep.get('pages')} sampled_bad={rep.get('sampled_bad')}")

    dst = Path(args.out)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)
    ok, detail = schema_readable(dst)
    print(f"schema: {'readable' if ok else 'UNREADABLE'} ({detail})")
    if not ok:
        print("\nHINT: a page 1 that looks right while later pages fail usually means"
              "\n      the IV offset is wrong (must be 4016, not 4032).")
        return 2
    print(f"\nwrote {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
