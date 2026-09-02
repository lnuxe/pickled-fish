#!/usr/bin/env python3
"""
Partner Skill 文件写入器

负责将生成的 relationship.md、persona.md 写入到正确的目录结构，
并生成 meta.json 和完整的 SKILL.md。

用法：
    python3 skill_writer.py --action create --slug xiaoyu --meta meta.json \
        --relationship relationship.md --persona persona.md \
        --base-dir ./partners

    python3 skill_writer.py --action update --slug xiaoyu \
        --relationship-patch relationship_patch.md \
        --base-dir ./partners

    python3 skill_writer.py --action list --base-dir ./partners
"""

from __future__ import annotations

import json
import shutil
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


SKILL_MD_TEMPLATE = """\
---
name: partner_{slug}
description: {name}，{identity}
user-invocable: true
---

# {name}

{identity}

---

## PART A：关系档案

{relationship_content}

---

## PART B：人格画像

{persona_content}

---

## 运行规则

接收到任何场景描述或问题时：

1. **先由 PART B 判断**：TA 在这个情境下的情绪状态、需求和反应模式是什么？
2. **再由 PART A 执行**：结合关系健康度和历史记忆，给出最适合这段关系的建议
3. **输出时保持个性化**：建议必须符合 TA 的依恋风格、爱的语言和沟通偏好

**PART B 的 Layer 0 硬规则永远优先，任何情况下不得违背。**
"""


def slugify(name: str) -> str:
    """将姓名转为 slug。优先尝试 pypinyin，否则 fallback 到简单处理。"""
    try:
        from pypinyin import lazy_pinyin
        parts = lazy_pinyin(name)
        slug = "_".join(parts)
    except ImportError:
        import unicodedata
        result = []
        for char in name.lower():
            if char.isascii() and (char.isalnum() or char in ("-", "_")):
                result.append(char)
            elif char == " ":
                result.append("_")
        slug = "".join(result)

    import re
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug if slug else "partner"


def build_identity_string(meta: dict) -> str:
    """从 meta 构建身份描述字符串"""
    profile = meta.get("profile", {})
    parts = []

    gender = profile.get("gender", "")
    age = profile.get("age", "")
    occupation = profile.get("occupation", "")

    if gender:
        parts.append(gender)
    if age:
        parts.append(f"{age}岁")
    if occupation:
        parts.append(occupation)

    identity = " · ".join(parts) if parts else "伴侣"

    mbti = profile.get("mbti", "")
    zodiac = profile.get("zodiac", "")
    attachment = profile.get("attachment_style", "")

    extras = []
    if mbti:
        extras.append(f"MBTI {mbti}")
    if zodiac:
        extras.append(f"{zodiac}座")
    if attachment:
        extras.append(f"{attachment}型依恋")

    if extras:
        identity += "，" + " / ".join(extras)

    return identity


def create_partner(
    base_dir: Path,
    slug: str,
    meta: dict,
    relationship_content: str,
    persona_content: str,
) -> Path:
    """创建新的伴侣 Skill 目录结构"""

    partner_dir = base_dir / slug
    partner_dir.mkdir(parents=True, exist_ok=True)

    # 创建子目录
    (partner_dir / "versions").mkdir(exist_ok=True)
    (partner_dir / "memories" / "chats").mkdir(parents=True, exist_ok=True)
    (partner_dir / "memories" / "notes").mkdir(parents=True, exist_ok=True)
    (partner_dir / "memories" / "emails").mkdir(parents=True, exist_ok=True)

    # 写入 relationship.md
    (partner_dir / "relationship.md").write_text(relationship_content, encoding="utf-8")

    # 写入 persona.md
    (partner_dir / "persona.md").write_text(persona_content, encoding="utf-8")

    # 生成并写入 SKILL.md
    name = meta.get("name", slug)
    identity = build_identity_string(meta)

    skill_md = SKILL_MD_TEMPLATE.format(
        slug=slug,
        name=name,
        identity=identity,
        relationship_content=relationship_content,
        persona_content=persona_content,
    )
    (partner_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    # 写入 persona-only skill
    persona_only = (
        f"---\nname: partner_{slug}_persona\n"
        f"description: {name} 的人格画像（仅 Persona）\n"
        f"user-invocable: true\n---\n\n{persona_content}\n"
    )
    (partner_dir / "persona_skill.md").write_text(persona_only, encoding="utf-8")

    # 写入 relationship-only skill
    relationship_only = (
        f"---\nname: partner_{slug}_relationship\n"
        f"description: {name} 的关系档案（仅关系健康度）\n"
        f"user-invocable: true\n---\n\n{relationship_content}\n"
    )
    (partner_dir / "relationship_skill.md").write_text(relationship_only, encoding="utf-8")

    # 写入 meta.json
    now = datetime.now(timezone.utc).isoformat()
    meta["slug"] = slug
    meta.setdefault("created_at", now)
    meta["updated_at"] = now
    meta["version"] = "v1"
    meta.setdefault("corrections_count", 0)
    meta.setdefault("rqi_score", None)
    meta.setdefault("relationship_stage", "unknown")

    (partner_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return partner_dir


def update_partner(
    partner_dir: Path,
    relationship_patch: Optional[str] = None,
    persona_patch: Optional[str] = None,
    correction: Optional[dict] = None,
) -> str:
    """更新现有伴侣 Skill，先存档当前版本，再写入更新"""

    meta_path = partner_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    current_version = meta.get("version", "v1")
    try:
        version_num = int(current_version.lstrip("v").split("_")[0]) + 1
    except ValueError:
        version_num = 2
    new_version = f"v{version_num}"

    # 存档当前版本
    version_dir = partner_dir / "versions" / current_version
    version_dir.mkdir(parents=True, exist_ok=True)
    for fname in ("SKILL.md", "relationship.md", "persona.md"):
        src = partner_dir / fname
        if src.exists():
            shutil.copy2(src, version_dir / fname)

    # 应用 relationship patch
    if relationship_patch:
        current_rel = (partner_dir / "relationship.md").read_text(encoding="utf-8")
        new_rel = current_rel + "\n\n" + relationship_patch
        (partner_dir / "relationship.md").write_text(new_rel, encoding="utf-8")

    # 应用 persona patch 或 correction
    if persona_patch or correction:
        current_persona = (partner_dir / "persona.md").read_text(encoding="utf-8")

        if correction:
            correction_line = (
                f"\n- [{correction.get('scene', '通用')}] "
                f"不应该 {correction['wrong']}，应该 {correction['correct']}"
            )
            target = "## Correction 记录"
            if target in current_persona:
                insert_pos = current_persona.index(target) + len(target)
                rest = current_persona[insert_pos:]
                skip = "\n\n（暂无记录）"
                if rest.startswith(skip):
                    rest = rest[len(skip):]
                new_persona = current_persona[:insert_pos] + correction_line + rest
            else:
                new_persona = (
                    current_persona
                    + f"\n\n## Correction 记录\n{correction_line}\n"
                )
            meta["corrections_count"] = meta.get("corrections_count", 0) + 1
        else:
            new_persona = current_persona + "\n\n" + persona_patch

        (partner_dir / "persona.md").write_text(new_persona, encoding="utf-8")

    # 重新生成 SKILL.md
    relationship_content = (partner_dir / "relationship.md").read_text(encoding="utf-8")
    persona_content = (partner_dir / "persona.md").read_text(encoding="utf-8")
    name = meta.get("name", partner_dir.name)
    identity = build_identity_string(meta)

    skill_md = SKILL_MD_TEMPLATE.format(
        slug=partner_dir.name,
        name=name,
        identity=identity,
        relationship_content=relationship_content,
        persona_content=persona_content,
    )
    (partner_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    # 更新 meta
    meta["version"] = new_version
    meta["updated_at"] = datetime.now(timezone.utc).isoformat()
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return new_version


def list_partners(base_dir: Path) -> list:
    """列出所有已创建的伴侣 Skill"""
    partners = []

    if not base_dir.exists():
        return partners

    for partner_dir in sorted(base_dir.iterdir()):
        if not partner_dir.is_dir():
            continue
        meta_path = partner_dir / "meta.json"
        if not meta_path.exists():
            continue

        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        partners.append({
            "slug": meta.get("slug", partner_dir.name),
            "name": meta.get("name", partner_dir.name),
            "identity": build_identity_string(meta),
            "version": meta.get("version", "v1"),
            "updated_at": meta.get("updated_at", ""),
            "corrections_count": meta.get("corrections_count", 0),
            "rqi_score": meta.get("rqi_score"),
            "relationship_stage": meta.get("relationship_stage", "unknown"),
        })

    return partners


def main() -> None:
    parser = argparse.ArgumentParser(description="Partner Skill 文件写入器")
    parser.add_argument("--action", required=True, choices=["create", "update", "list"])
    parser.add_argument("--slug", help="伴侣 slug（用于目录名）")
    parser.add_argument("--name", help="伴侣姓名/昵称")
    parser.add_argument("--meta", help="meta.json 文件路径")
    parser.add_argument("--relationship", help="relationship.md 内容文件路径")
    parser.add_argument("--persona", help="persona.md 内容文件路径")
    parser.add_argument("--relationship-patch", help="relationship.md 增量更新内容文件路径")
    parser.add_argument("--persona-patch", help="persona.md 增量更新内容文件路径")
    parser.add_argument(
        "--base-dir",
        default="./partners",
        help="伴侣 Skill 根目录（默认：./partners）",
    )

    args = parser.parse_args()
    base_dir = Path(args.base_dir).expanduser()

    if args.action == "list":
        partners = list_partners(base_dir)
        if not partners:
            print("暂无已创建的伴侣 Skill")
        else:
            print(f"已创建 {len(partners)} 个伴侣 Skill：\n")
            for p in partners:
                updated = p["updated_at"][:10] if p["updated_at"] else "未知"
                rqi = f"RQI {p['rqi_score']:.1f}" if p["rqi_score"] else "RQI 未评估"
                print(f"  [{p['slug']}]  {p['name']} — {p['identity']}")
                print(f"    版本: {p['version']}  {rqi}  纠正次数: {p['corrections_count']}  更新: {updated}")
                print()

    elif args.action == "create":
        if not args.slug and not args.name:
            print("错误：create 操作需要 --slug 或 --name", file=sys.stderr)
            sys.exit(1)

        meta: dict = {}
        if args.meta:
            meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
        if args.name:
            meta["name"] = args.name

        slug = args.slug or slugify(meta.get("name", "partner"))

        relationship_content = ""
        if args.relationship:
            relationship_content = Path(args.relationship).read_text(encoding="utf-8")

        persona_content = ""
        if args.persona:
            persona_content = Path(args.persona).read_text(encoding="utf-8")

        partner_dir = create_partner(base_dir, slug, meta, relationship_content, persona_content)
        print(f"✅ 伴侣 Skill 已创建：{partner_dir}")
        print(f"   触发词：/{slug}")

    elif args.action == "update":
        if not args.slug:
            print("错误：update 操作需要 --slug", file=sys.stderr)
            sys.exit(1)

        partner_dir = base_dir / args.slug
        if not partner_dir.exists():
            print(f"错误：找不到 Skill 目录 {partner_dir}", file=sys.stderr)
            sys.exit(1)

        relationship_patch = (
            Path(args.relationship_patch).read_text(encoding="utf-8")
            if args.relationship_patch else None
        )
        persona_patch = (
            Path(args.persona_patch).read_text(encoding="utf-8")
            if args.persona_patch else None
        )

        new_version = update_partner(partner_dir, relationship_patch, persona_patch)
        print(f"✅ 伴侣 Skill 已更新到 {new_version}：{partner_dir}")


if __name__ == "__main__":
    main()
