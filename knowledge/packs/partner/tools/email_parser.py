#!/usr/bin/env python3
"""
邮件解析器

解析 .eml 或 .mbox 格式的邮件，提取与伴侣的沟通内容。
适用于长距离恋爱、书信往来等场景。

用法：
    python3 email_parser.py --input emails.mbox --output parsed.json
    python3 email_parser.py --input letter.eml --output parsed.json --stats
    python3 email_parser.py --input emails/ --output parsed.json  # 解析目录下所有 .eml
"""

from __future__ import annotations

import json
import email
import mailbox
import argparse
import sys
import re
from pathlib import Path
from email.header import decode_header
from email.utils import parsedate_to_datetime
from typing import Optional


def decode_str(s: Optional[str]) -> str:
    """解码邮件头部字段"""
    if not s:
        return ""
    parts = decode_header(s)
    result = []
    for part, charset in parts:
        if isinstance(part, bytes):
            try:
                result.append(part.decode(charset or "utf-8", errors="replace"))
            except Exception:
                result.append(part.decode("utf-8", errors="replace"))
        else:
            result.append(str(part))
    return "".join(result)


def extract_body(msg: email.message.Message) -> str:
    """提取邮件正文（优先纯文本）"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    body = payload.decode(charset, errors="replace")
                    break
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            body = payload.decode(charset, errors="replace")

    # 清理引用内容（"On ... wrote:"）
    body = re.sub(r"\n>.*", "", body)
    body = re.sub(r"\nOn .+wrote:\n", "", body, flags=re.DOTALL)
    return body.strip()


def parse_eml(file_path: Path) -> Optional[dict]:
    """解析单个 .eml 文件"""
    try:
        with open(file_path, "rb") as f:
            msg = email.message_from_binary_file(f)
    except Exception as e:
        return None

    subject = decode_str(msg.get("Subject", ""))
    sender = decode_str(msg.get("From", ""))
    recipient = decode_str(msg.get("To", ""))
    date_str = msg.get("Date", "")

    timestamp = None
    if date_str:
        try:
            dt = parsedate_to_datetime(date_str)
            timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            timestamp = date_str

    body = extract_body(msg)
    if not body:
        return None

    return {
        "subject": subject,
        "sender": sender,
        "recipient": recipient,
        "timestamp": timestamp,
        "body": body,
        "source": str(file_path),
    }


def parse_mbox(file_path: Path) -> list[dict]:
    """解析 .mbox 文件"""
    emails_list = []
    try:
        mbox = mailbox.mbox(str(file_path))
        for msg in mbox:
            subject = decode_str(msg.get("Subject", ""))
            sender = decode_str(msg.get("From", ""))
            recipient = decode_str(msg.get("To", ""))
            date_str = msg.get("Date", "")

            timestamp = None
            if date_str:
                try:
                    dt = parsedate_to_datetime(date_str)
                    timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    timestamp = date_str

            body = extract_body(msg)
            if not body:
                continue

            emails_list.append({
                "subject": subject,
                "sender": sender,
                "recipient": recipient,
                "timestamp": timestamp,
                "body": body,
                "source": str(file_path),
            })
    except Exception as e:
        print(f"警告：解析 mbox 失败 — {e}", file=sys.stderr)

    return emails_list


def analyze_emails(emails_list: list[dict], my_email: str = "") -> dict:
    """分析邮件内容，提取关系信息"""
    total = len(emails_list)
    if total == 0:
        return {"total_emails": 0}

    sent = [e for e in emails_list if my_email and my_email in e.get("sender", "")]
    received = [e for e in emails_list if my_email and my_email not in e.get("sender", "")]

    # 如果没有 my_email，无法区分
    if not my_email:
        sent = []
        received = emails_list

    # 平均正文长度
    avg_body_len = sum(len(e.get("body", "")) for e in received) / max(len(received), 1)

    # 情感分析（简单关键词）
    positive_keywords = ["爱你", "想你", "喜欢", "开心", "感谢", "love", "miss", "happy", "thank"]
    negative_keywords = ["难过", "伤心", "生气", "失望", "sorry", "sad", "angry", "disappointed"]

    positive_count = 0
    negative_count = 0
    for e in received:
        body = e.get("body", "").lower()
        positive_count += sum(1 for kw in positive_keywords if kw in body)
        negative_count += sum(1 for kw in negative_keywords if kw in body)

    # 主题词提取
    all_subjects = " ".join(e.get("subject", "") for e in emails_list)
    subject_words = re.findall(r"[\u4e00-\u9fff]{2,4}|[a-zA-Z]{4,}", all_subjects)
    subject_freq: dict[str, int] = {}
    for w in subject_words:
        subject_freq[w] = subject_freq.get(w, 0) + 1
    top_subjects = sorted(subject_freq.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "total_emails": total,
        "sent_count": len(sent),
        "received_count": len(received),
        "avg_received_body_length": round(avg_body_len, 0),
        "positive_signal_count": positive_count,
        "negative_signal_count": negative_count,
        "top_subject_words": [w for w, _ in top_subjects],
        "communication_style_hint": (
            "书面表达丰富，情感深度可能通过文字体现" if avg_body_len > 500
            else "邮件较简短，可能是功能性沟通为主"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="邮件解析器")
    parser.add_argument("--input", required=True, help="输入文件或目录路径（.eml / .mbox / 目录）")
    parser.add_argument("--output", help="输出 JSON 文件路径（默认打印到 stdout）")
    parser.add_argument("--my-email", default="", help="用户自己的邮箱地址（用于区分发送方）")
    parser.add_argument("--stats", action="store_true", help="输出统计分析")

    args = parser.parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"错误：路径不存在 {input_path}", file=sys.stderr)
        sys.exit(1)

    emails_list = []

    if input_path.is_dir():
        for eml_file in sorted(input_path.glob("**/*.eml")):
            parsed = parse_eml(eml_file)
            if parsed:
                emails_list.append(parsed)
    elif input_path.suffix.lower() == ".mbox":
        emails_list = parse_mbox(input_path)
    elif input_path.suffix.lower() == ".eml":
        parsed = parse_eml(input_path)
        if parsed:
            emails_list = [parsed]
    else:
        print(f"错误：不支持的文件格式 {input_path.suffix}", file=sys.stderr)
        sys.exit(1)

    result: dict = {"emails": emails_list}

    if args.stats:
        result["stats"] = analyze_emails(emails_list, args.my_email)

    output_str = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output_str, encoding="utf-8")
        print(f"✅ 解析完成：{len(emails_list)} 封邮件 → {args.output}")
        if args.stats and "stats" in result:
            stats = result["stats"]
            print(f"   收到邮件：{stats.get('received_count', 0)} 封")
            print(f"   平均正文长度：{stats.get('avg_received_body_length', 0)} 字")
            print(f"   沟通风格提示：{stats.get('communication_style_hint', '')}")
    else:
        print(output_str)


if __name__ == "__main__":
    main()
