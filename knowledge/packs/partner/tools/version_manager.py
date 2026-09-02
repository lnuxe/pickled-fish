"""
version_manager.py — Snapshot and rollback manager for partner profiles.

Saves versioned snapshots of a partner's profile directory and supports
listing history and rolling back to previous states.
"""

import os
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime


def get_versions_dir(slug: str, base_dir: str) -> Path:
    """Return the path to the .versions directory for a given slug."""
    return Path(base_dir) / slug / ".versions"


def save_snapshot(slug: str, message: str, base_dir: str) -> dict:
    """
    Save a snapshot of the current partner profile.

    Args:
        slug: Partner identifier slug.
        message: Commit-style message describing this snapshot.
        base_dir: Base directory containing partner profiles.

    Returns:
        A dict with version_id, timestamp, and message.
    """
    source_dir = Path(base_dir) / slug
    if not source_dir.exists():
        raise FileNotFoundError(f"Partner profile not found: {source_dir}")

    versions_dir = get_versions_dir(slug, base_dir)
    versions_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    version_id = f"v_{timestamp}"
    snapshot_dir = versions_dir / version_id

    # Copy all files except the .versions directory itself
    shutil.copytree(
        source_dir,
        snapshot_dir,
        ignore=shutil.ignore_patterns(".versions"),
    )

    # Write metadata
    meta = {"version_id": version_id, "timestamp": timestamp, "message": message}
    with open(snapshot_dir / "_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"Snapshot saved: {version_id} — {message}")
    return meta


def list_versions(slug: str, base_dir: str) -> list:
    """
    List all saved snapshots for a partner.

    Args:
        slug: Partner identifier slug.
        base_dir: Base directory containing partner profiles.

    Returns:
        A list of version metadata dicts, sorted newest-first.
    """
    versions_dir = get_versions_dir(slug, base_dir)
    if not versions_dir.exists():
        print(f"No version history found for: {slug}")
        return []

    versions = []
    for entry in sorted(versions_dir.iterdir(), reverse=True):
        meta_path = entry / "_meta.json"
        if meta_path.exists():
            with open(meta_path, encoding="utf-8") as f:
                versions.append(json.load(f))

    for v in versions:
        print(f"  {v['version_id']}  {v['timestamp']}  {v['message']}")

    return versions


def rollback(slug: str, version_id: str, base_dir: str) -> None:
    """
    Restore a partner profile to a previous snapshot.

    Args:
        slug: Partner identifier slug.
        version_id: The version identifier to restore.
        base_dir: Base directory containing partner profiles.
    """
    snapshot_dir = get_versions_dir(slug, base_dir) / version_id
    if not snapshot_dir.exists():
        raise FileNotFoundError(f"Version not found: {version_id}")

    target_dir = Path(base_dir) / slug

    # Save current state before overwriting
    save_snapshot(slug, f"Auto-save before rollback to {version_id}", base_dir)

    # Remove current files (preserve .versions)
    for item in target_dir.iterdir():
        if item.name == ".versions":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    # Restore from snapshot
    for item in snapshot_dir.iterdir():
        if item.name == "_meta.json":
            continue
        dest = target_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    print(f"Rolled back {slug} to {version_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Partner profile version manager")
    parser.add_argument(
        "--action",
        required=True,
        choices=["save", "list", "rollback"],
        help="Action to perform",
    )
    parser.add_argument("--slug", required=True, help="Partner slug")
    parser.add_argument("--message", default="Manual snapshot", help="Snapshot message")
    parser.add_argument("--version", help="Version ID for rollback")
    parser.add_argument("--base-dir", default="./partners", help="Base directory")

    args = parser.parse_args()

    if args.action == "save":
        save_snapshot(args.slug, args.message, args.base_dir)
    elif args.action == "list":
        list_versions(args.slug, args.base_dir)
    elif args.action == "rollback":
        if not args.version:
            parser.error("--version is required for rollback action")
        rollback(args.slug, args.version, args.base_dir)
