#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_chat.py — 把 PyWxDump 导出的聊天 CSV 规范化成 pickled-fish 下游可读的 chat.txt。

输出行格式（与 wechat-mac-export / local-chat-pipeline 一致）:
    [YYYY-MM-DD HH:MM:SS] 我: 内容
    [YYYY-MM-DD HH:MM:SS] <对方昵称>: 内容

用法:
    python export_chat.py --csv a.csv [b.csv ...] [--out chat.txt]

说明:
    - 按表头读取（列名/顺序随 PyWxDump 版本变化均可，缺关键列会报错提示）。
    - IsSender=1 -> "我"；否则取 Remark > NickName > Sender > TalkerId。
    - 非文本消息（图片/语音/视频/文件/链接等）写成人读占位符，避免把整段 XML 塞进 chat.txt。
    - 多条 CSV 会按时间全局排序合并。
"""

import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

# 消息类型（微信常用枚举，不同版本可能略有出入）
TYPE_TEXT = 1
TYPE_IMAGE = 3
TYPE_VOICE = 34
TYPE_VIDEO = 43
TYPE_EMOJI = 47
TYPE_APP = 49
TYPE_SYSTEM = 10000

# 表头别名：统一小写、去空白、去 BOM 后匹配
ALIASES = {
    "create_time": ["createtime", "create_time", "createtime", "time", "timestamp"],
    "str_time": ["strtime", "str_time", "time_str", "formattime"],
    "content": ["strcontent", "str_content", "content", "msg", "message"],
    "is_sender": ["issender", "is_sender", "is_send", "sender_flag", "self"],
    "msg_type": ["type", "msgtype", "msg_type"],
    "remark": ["remark", "remarkname"],
    "nick": ["nickname", "nick_name", "nickname_", "name"],
    "sender": ["sender", "sender_id", "sender_wxid"],
    "talker": ["talkerid", "talker_id", "talker", "username"],
}


def normalize(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (key or "").strip().lstrip("\ufeff").lower())


def resolve_columns(fieldnames):
    """把 CSV 表头映射到规范字段名；找不到时返回 None。"""
    norm_to_field = {}
    for field, aliases in ALIASES.items():
        for a in aliases:
            norm_to_field.setdefault(normalize(a), field)

    mapping = {}
    for col in fieldnames:
        field = norm_to_field.get(normalize(col))
        if field:
            mapping[field] = col
    return mapping


def parse_time(raw) -> datetime | None:
    """解析 CreateTime（Unix 秒/毫秒）或 StrTime（已格式化字符串）。"""
    s = (raw or "").strip()
    if not s or s in ("0", "0.0"):
        return None
    # 数字时间戳
    try:
        n = float(s)
        if n > 1e12:  # 毫秒
            n /= 1000.0
        return datetime.fromtimestamp(n)
    except ValueError:
        pass
    # 已格式化的字符串
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def xml_text(xml: str, tag: str) -> str:
    m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", xml or "", flags=re.S)
    if not m:
        return ""
    txt = re.sub(r"<[^>]+>", "", m.group(1))
    return txt.strip()


def strip_tags(s: str) -> str:
    """仅在确实含 XML/HTML 标签时去掉标签，避免误删 "a < b" 这类文本。"""
    if re.search(r"</?[a-zA-Z][^>]*>", s):
        return re.sub(r"<[^>]+>", "", s)
    return s


def decode_content(raw: str, msg_type) -> str:
    """把一条消息渲染成一行文本。"""
    raw = (raw or "").strip()
    if msg_type == TYPE_TEXT:
        # 纯文本消息；个别版本内容仍含简单标签，这里仅去最外层尖括号包裹的标签
        return strip_tags(raw).strip()
    if msg_type == TYPE_IMAGE:
        return "[图片]"
    if msg_type == TYPE_VOICE:
        return "[语音]"
    if msg_type == TYPE_VIDEO:
        return "[视频]"
    if msg_type == TYPE_EMOJI:
        return "[表情]"
    if msg_type == TYPE_APP:
        title = xml_text(raw, "title")
        fname = xml_text(raw, "filename") or xml_text(raw, "fileext")
        appname = xml_text(raw, "appname")
        if fname:
            return f"[文件: {fname}]"
        if title and appname and "小" in appname:
            return f"[小程序: {title}]"
        if title:
            return f"[链接: {title}]"
        if appname:
            return f"[应用消息: {appname}]"
        return "[应用消息]"
    if msg_type == TYPE_SYSTEM:
        plain = strip_tags(raw).strip()
        return plain if plain else "[系统消息]"
    # 未知类型：有可读文本就保留，否则给占位
    if raw and not raw.startswith("<"):
        return raw
    return "[消息]"


def sender_label(row, is_sender) -> str:
    if is_sender:
        return "我"
    for key in ("remark", "nick", "sender", "talker"):
        v = (row.get(key) or "").strip()
        if v and v not in ("0", "null", "None"):
            return v
    return "对方"


def read_csv(path: Path, encoding: str):
    rows = []
    with path.open("r", encoding=encoding, newline="", errors="replace") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return rows
        colmap = resolve_columns(reader.fieldnames)
        if "content" not in colmap:
            raise SystemExit(
                f"[错误] {path}: 找不到内容列（表头: {reader.fieldnames}）。"
                " 请确认是 PyWxDump 导出的 CSV。"
            )
        for row in reader:
            # 把原始表头映射成规范字段名，避免大小写/别名差异
            norm = {field: (row.get(col) or "").strip() for field, col in colmap.items()}

            dt = None
            if "create_time" in norm:
                dt = parse_time(norm["create_time"])
            if dt is None and "str_time" in norm:
                dt = parse_time(norm["str_time"])

            raw_type = norm.get("msg_type", "")
            try:
                msg_type = int(float(raw_type))
            except (ValueError, TypeError):
                msg_type = TYPE_TEXT if not raw_type else -1

            is_sender = False
            if "is_sender" in norm:
                is_sender = norm["is_sender"] in ("1", "true", "True", "yes", "1.0")

            content = decode_content(norm.get("content", ""), msg_type)
            if not content:
                continue
            rows.append((dt, sender_label(norm, is_sender), content))
    return rows


def main():
    ap = argparse.ArgumentParser(description="PyWxDump CSV -> chat.txt 规范化")
    ap.add_argument("--csv", nargs="+", required=True, help="PyWxDump 导出的 CSV（可多个，按时间合并）")
    ap.add_argument("--out", help="输出 chat.txt 路径（默认：第一个 CSV 同目录下 chat.txt）")
    ap.add_argument("--encoding", default="utf-8-sig", help="CSV 编码（默认 utf-8-sig；GBK 用 gbk）")
    args = ap.parse_args()

    paths = [Path(p) for p in args.csv]
    for p in paths:
        if not p.is_file():
            raise SystemExit(f"[错误] 文件不存在: {p}")

    records = []
    for p in paths:
        records.extend(read_csv(p, args.encoding))

    if not records:
        raise SystemExit("[提示] 未解析出任何消息，请检查 CSV 内容与列名。")

    # 稳定排序：时间升序，无时间戳的排最后，同时间保持原相对顺序
    epoch = datetime(1970, 1, 1)
    records.sort(key=lambda r: (r[0] or epoch,))

    out = Path(args.out) if args.out else (paths[0].with_name("chat.txt"))
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as f:
        for dt, who, content in records:
            ts = dt.strftime("%Y-%m-%d %H:%M:%S") if dt else "????-??-?? ??:??:??"
            line = f"[{ts}] {who}: {content}"
            f.write(line + "\n")

    print(f"已写入 {len(records)} 条消息 -> {out}")


if __name__ == "__main__":
    main()
