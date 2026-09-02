#!/usr/bin/env python3
"""
聊天记录解析器

支持解析多种格式的聊天记录，提取关键情感信息用于伴侣画像构建。

支持格式：
  - 微信导出 TXT（WeChatMsg / 留痕 格式）
  - 微信导出 JSON（PyWxDump 格式）
  - iMessage / SMS 导出 TXT
  - 通用对话截图（图片路径，需 Claude 视觉分析）
  - 直接粘贴文本

用法：
    python3 chat_parser.py --input chat.txt --format wechat-txt --output parsed.json
    python3 chat_parser.py --input chat.json --format wechat-json --output parsed.json
    python3 chat_parser.py --input messages.txt --format generic --output parsed.json
    python3 chat_parser.py --input chat.txt --format auto --output parsed.json --stats
"""

from __future__ import annotations

import json
import re
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


# ─── 消息数据结构 ─────────────────────────────────────────────────────────────

def make_message(
    sender: str,
    content: str,
    timestamp: Optional[str] = None,
    msg_type: str = "text",
    is_partner: Optional[bool] = None,
) -> dict:
    return {
        "sender": sender,
        "content": content,
        "timestamp": timestamp,
        "type": msg_type,
        "is_partner": is_partner,
    }


# ─── 微信 TXT 解析（WeChatMsg / 留痕 格式）────────────────────────────────────

WECHAT_TXT_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+?)\s*\n([\s\S]*?)(?=\n\d{4}-\d{2}-\d{2}|\Z)",
    re.MULTILINE,
)

def parse_wechat_txt(text: str, my_name: str = "我") -> list[dict]:
    messages = []
    for match in WECHAT_TXT_PATTERN.finditer(text):
        timestamp = match.group(1)
        sender = match.group(2).strip()
        content = match.group(3).strip()
        if not content:
            continue
        is_partner = sender != my_name
        messages.append(make_message(sender, content, timestamp, is_partner=is_partner))
    return messages


# ─── 微信 JSON 解析（PyWxDump 格式）──────────────────────────────────────────

def parse_wechat_json(data: list | dict, my_name: str = "我") -> list[dict]:
    messages = []
    if isinstance(data, dict):
        data = data.get("messages", data.get("data", []))

    for item in data:
        sender = item.get("sender", item.get("from", item.get("nickname", "未知")))
        content = item.get("content", item.get("msg", item.get("text", "")))
        timestamp = item.get("timestamp", item.get("create_time", item.get("time", None)))
        msg_type = item.get("type", "text")

        if isinstance(timestamp, (int, float)):
            try:
                timestamp = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                timestamp = str(timestamp)

        if not content:
            continue

        is_partner = sender != my_name
        messages.append(make_message(sender, content, timestamp, msg_type, is_partner))

    return messages


# ─── 通用 TXT 解析（iMessage / SMS / 粘贴文本）────────────────────────────────

GENERIC_PATTERNS = [
    # "[时间] 发送者: 内容"
    re.compile(r"^\[(\d{4}[-/]\d{2}[-/]\d{2}[T\s]\d{2}:\d{2}(?::\d{2})?)\]\s+(.+?):\s+(.+)$"),
    # "发送者 时间\n内容" (iMessage)
    re.compile(r"^(.+?)\s+(\d{4}[-/]\d{2}[-/]\d{2}\s+\d{2}:\d{2}(?::\d{2})?)\n(.+)$", re.MULTILINE),
    # "发送者: 内容" (无时间)
    re.compile(r"^(.+?):\s+(.+)$"),
]

def parse_generic_txt(text: str, my_name: str = "我") -> list[dict]:
    messages = []
    lines = text.strip().split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        matched = False
        for pattern in GENERIC_PATTERNS[:2]:
            m = pattern.match(line)
            if m:
                groups = m.groups()
                if len(groups) == 3:
                    timestamp, sender, content = groups[0], groups[1], groups[2]
                    is_partner = sender.strip() != my_name
                    messages.append(make_message(sender.strip(), content.strip(), timestamp, is_partner=is_partner))
                    matched = True
                    break

        if not matched:
            m = GENERIC_PATTERNS[2].match(line)
            if m:
                sender, content = m.group(1).strip(), m.group(2).strip()
                is_partner = sender != my_name
                messages.append(make_message(sender, content, is_partner=is_partner))

    return messages


# ─── 自动检测格式 ─────────────────────────────────────────────────────────────

def detect_format(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix == ".json":
        return "wechat-json"
    if suffix in (".txt", ".md"):
        content = file_path.read_text(encoding="utf-8", errors="replace")[:2000]
        if re.search(r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s+\S", content):
            return "wechat-txt"
        return "generic"
    return "generic"


# ─── 统计分析 ─────────────────────────────────────────────────────────────────

EMOTION_KEYWORDS = {
    "positive": ["爱你", "喜欢", "开心", "高兴", "谢谢", "感谢", "好的", "棒", "太好了", "哈哈", "嘻嘻", "❤", "😊", "😍"],
    "negative": ["生气", "难过", "伤心", "烦", "讨厌", "不想", "算了", "随便", "无所谓", "😢", "😡", "😤"],
    "conflict": ["为什么", "凭什么", "你总是", "你从来", "你根本", "不理我", "冷战", "分手"],
    "affection": ["想你", "想见你", "抱抱", "亲亲", "宝贝", "宝宝", "老婆", "老公", "亲爱的"],
}

def analyze_messages(messages: list[dict]) -> dict:
    total = len(messages)
    if total == 0:
        return {"total_messages": 0}

    partner_msgs = [m for m in messages if m.get("is_partner")]
    my_msgs = [m for m in messages if not m.get("is_partner")]

    # 情感词统计
    emotion_counts = {k: 0 for k in EMOTION_KEYWORDS}
    partner_emotion_counts = {k: 0 for k in EMOTION_KEYWORDS}

    for msg in messages:
        content = msg.get("content", "")
        is_partner = msg.get("is_partner", False)
        for emotion, keywords in EMOTION_KEYWORDS.items():
            if any(kw in content for kw in keywords):
                emotion_counts[emotion] += 1
                if is_partner:
                    partner_emotion_counts[emotion] += 1

    # 消息长度分析
    partner_avg_len = (
        sum(len(m.get("content", "")) for m in partner_msgs) / len(partner_msgs)
        if partner_msgs else 0
    )
    my_avg_len = (
        sum(len(m.get("content", "")) for m in my_msgs) / len(my_msgs)
        if my_msgs else 0
    )

    # 发起对话比例（以第一条消息为准）
    initiations = {"partner": 0, "me": 0}
    prev_sender_is_partner = None
    for msg in messages:
        is_partner = msg.get("is_partner", False)
        if prev_sender_is_partner is None or prev_sender_is_partner != is_partner:
            if is_partner:
                initiations["partner"] += 1
            else:
                initiations["me"] += 1
        prev_sender_is_partner = is_partner

    # 高频词提取（简单版）
    all_partner_text = " ".join(m.get("content", "") for m in partner_msgs)
    words = re.findall(r"[\u4e00-\u9fff]{2,4}", all_partner_text)
    word_freq: dict[str, int] = {}
    for w in words:
        word_freq[w] = word_freq.get(w, 0) + 1
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    return {
        "total_messages": total,
        "partner_message_count": len(partner_msgs),
        "my_message_count": len(my_msgs),
        "partner_avg_message_length": round(partner_avg_len, 1),
        "my_avg_message_length": round(my_avg_len, 1),
        "emotion_counts": emotion_counts,
        "partner_emotion_counts": partner_emotion_counts,
        "conversation_initiations": initiations,
        "partner_top_words": [w for w, _ in top_words],
        "analysis_hints": _generate_hints(
            partner_msgs, my_msgs, emotion_counts, partner_emotion_counts, initiations
        ),
    }


def _generate_hints(partner_msgs, my_msgs, emotion_counts, partner_emotion_counts, initiations) -> list[str]:
    hints = []
    total = len(partner_msgs) + len(my_msgs)
    if total == 0:
        return hints

    # 消息比例
    partner_ratio = len(partner_msgs) / total
    if partner_ratio < 0.3:
        hints.append("TA 的消息比例较低（< 30%），可能是话少型或回避型依恋")
    elif partner_ratio > 0.7:
        hints.append("TA 的消息比例较高（> 70%），可能是焦虑型依恋或主动表达型")

    # 冲突信号
    conflict_rate = emotion_counts.get("conflict", 0) / max(total, 1)
    if conflict_rate > 0.05:
        hints.append(f"检测到较高频率的冲突性语言（{emotion_counts['conflict']} 次），建议重点分析冲突模式")

    # 亲密信号
    affection_count = partner_emotion_counts.get("affection", 0)
    if affection_count > 10:
        hints.append(f"TA 使用了 {affection_count} 次亲密称呼/表达，爱的语言可能偏向语言肯定")

    # 发起对话
    total_init = initiations["partner"] + initiations["me"]
    if total_init > 0:
        partner_init_ratio = initiations["partner"] / total_init
        if partner_init_ratio < 0.3:
            hints.append("TA 较少主动发起对话，可能需要更多安全感建立")
        elif partner_init_ratio > 0.7:
            hints.append("TA 经常主动发起对话，对这段关系投入较高")

    return hints


# ─── 主函数 ───────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="聊天记录解析器")
    parser.add_argument("--input", required=True, help="输入文件路径")
    parser.add_argument(
        "--format",
        default="auto",
        choices=["auto", "wechat-txt", "wechat-json", "generic"],
        help="输入格式（默认自动检测）",
    )
    parser.add_argument("--output", help="输出 JSON 文件路径（默认打印到 stdout）")
    parser.add_argument("--my-name", default="我", help="用户自己的名称（用于区分发送方）")
    parser.add_argument("--stats", action="store_true", help="输出统计分析")

    args = parser.parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"错误：文件不存在 {input_path}", file=sys.stderr)
        sys.exit(1)

    # 检测格式
    fmt = args.format
    if fmt == "auto":
        fmt = detect_format(input_path)

    # 解析
    if fmt == "wechat-json":
        data = json.loads(input_path.read_text(encoding="utf-8", errors="replace"))
        messages = parse_wechat_json(data, args.my_name)
    elif fmt == "wechat-txt":
        text = input_path.read_text(encoding="utf-8", errors="replace")
        messages = parse_wechat_txt(text, args.my_name)
    else:
        text = input_path.read_text(encoding="utf-8", errors="replace")
        messages = parse_generic_txt(text, args.my_name)

    result: dict = {"format": fmt, "messages": messages}

    if args.stats:
        result["stats"] = analyze_messages(messages)

    output_str = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output_str, encoding="utf-8")
        print(f"✅ 解析完成：{len(messages)} 条消息 → {args.output}")
        if args.stats and "stats" in result:
            stats = result["stats"]
            print(f"   伴侣消息：{stats.get('partner_message_count', 0)} 条")
            print(f"   平均消息长度：{stats.get('partner_avg_message_length', 0)} 字")
            hints = stats.get("analysis_hints", [])
            if hints:
                print("   分析提示：")
                for h in hints:
                    print(f"     • {h}")
    else:
        print(output_str)


if __name__ == "__main__":
    main()
