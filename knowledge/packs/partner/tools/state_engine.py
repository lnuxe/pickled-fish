#!/usr/bin/env python3
"""
state_engine.py — 关系状态机（Relationship State Machine）
partner.skill 核心推理层：判定当前关系状态，预测状态转移，评估干预紧急程度。

Usage:
    python3 state_engine.py --interactive
    python3 state_engine.py --signals '{"response_latency": 6, "conflict_frequency": 3, ...}'
"""

import json
import sys
import argparse
from dataclasses import dataclass, asdict
from typing import Optional


# ─────────────────────────────────────────────
# 状态空间定义
# ─────────────────────────────────────────────

STATES = {
    "S1": {
        "name": "热恋期（Honeymoon）",
        "description": "高亲密 + 高回应 + 主动互动频繁",
        "rqi_range": (8.0, 10.0),
        "urgency": "LOW",
        "color": "🟢",
    },
    "S2": {
        "name": "稳定期（Stable）",
        "description": "中亲密 + 稳定互动 + 冲突少且可修复",
        "rqi_range": (6.0, 7.9),
        "urgency": "LOW",
        "color": "🟢",
    },
    "S3": {
        "name": "轻度疏离（Mild Drift）",
        "description": "低主动 + 回复延迟 + 共同活动减少",
        "rqi_range": (4.5, 5.9),
        "urgency": "MEDIUM",
        "color": "🟡",
    },
    "S4": {
        "name": "冲突期（Active Conflict）",
        "description": "负面情绪主导 + 高频摩擦 + 防御行为增加",
        "rqi_range": (3.0, 5.5),
        "urgency": "HIGH",
        "color": "🟠",
    },
    "S5": {
        "name": "冷却期（Emotional Withdrawal）",
        "description": "低互动 + 情绪撤退 + 单方或双方回避",
        "rqi_range": (2.0, 3.9),
        "urgency": "HIGH",
        "color": "🔴",
    },
    "S6": {
        "name": "破裂边缘（Critical）",
        "description": "极低互动 + 明确负面信号 + 分离讨论出现",
        "rqi_range": (0.0, 2.5),
        "urgency": "CRITICAL",
        "color": "🚨",
    },
}

# 无干预情况下的自然状态转移矩阵
TRANSITION_MATRIX = {
    "S1": {"S1": 0.60, "S2": 0.35, "S3": 0.05},
    "S2": {"S1": 0.10, "S2": 0.55, "S3": 0.25, "S4": 0.10},
    "S3": {"S2": 0.20, "S3": 0.40, "S4": 0.25, "S5": 0.15},
    "S4": {"S2": 0.15, "S3": 0.20, "S4": 0.30, "S5": 0.25, "S6": 0.10},
    "S5": {"S3": 0.10, "S4": 0.15, "S5": 0.45, "S6": 0.30},
    "S6": {"S5": 0.20, "S6": 0.80},
}

# 不干预时的 RQI 变化量（每周）
RQI_DELTA_NO_ACTION = {
    "S1": +0.1,   # 热恋期自然维持
    "S2": 0.0,    # 稳定期持平
    "S3": -0.5,   # 疏离期缓慢下滑
    "S4": -1.2,   # 冲突期快速恶化
    "S5": -1.5,   # 冷却期持续恶化
    "S6": -2.0,   # 破裂边缘急速恶化
}

URGENCY_RESPONSE_TIME = {
    "LOW": "无需紧急干预，定期维护即可",
    "MEDIUM": "建议 48 小时内主动行动",
    "HIGH": "建议 24 小时内启动修复协议",
    "CRITICAL": "立即启动危机干预，必要时寻求专业帮助",
}


# ─────────────────────────────────────────────
# 数据结构
# ─────────────────────────────────────────────

@dataclass
class ObservableSignals:
    """可观测信号输入"""
    response_latency: float = 1.0       # 平均回复延迟（小时）
    initiation_ratio: float = 0.5       # 用户主动发起比例（0–1）
    negative_sentiment: float = 0.1     # 负面情绪词频率（0–1）
    conflict_frequency: int = 0         # 近 7 天冲突次数
    physical_intimacy: int = 3          # 近 7 天肢体亲密行为（0–5）
    shared_activities: int = 3          # 近 7 天共同活动次数
    withdrawal_signals: bool = False    # 是否出现情绪撤退信号
    explicit_negative: bool = False     # 是否出现明确分离/分手讨论


@dataclass
class StateInferenceResult:
    """状态推断结果"""
    current_state: str
    state_name: str
    state_description: str
    confidence: float
    key_signals: list
    predicted_next_state: str
    transition_probability: float
    rqi_delta_if_no_action: float
    urgency_level: str
    urgency_advice: str
    color: str


# ─────────────────────────────────────────────
# 核心推断逻辑
# ─────────────────────────────────────────────

def infer_state(signals: ObservableSignals) -> StateInferenceResult:
    """
    根据可观测信号推断当前关系状态。
    返回完整的状态推断结果。
    """
    key_signals = []
    state_id = "S2"  # 默认稳定期
    confidence = 0.60

    # ── 规则引擎（优先级从高到低）──

    if signals.explicit_negative:
        state_id = "S6"
        confidence = 0.90
        key_signals.append("出现明确的分离或分手讨论")

    elif signals.withdrawal_signals and signals.negative_sentiment > 0.5:
        state_id = "S5"
        confidence = 0.82
        key_signals.append(f"情绪撤退信号明显，负面情绪频率 {signals.negative_sentiment:.0%}")
        if signals.response_latency > 8:
            key_signals.append(f"回复延迟高达 {signals.response_latency:.0f} 小时")

    elif signals.conflict_frequency >= 3 and signals.negative_sentiment > 0.4:
        state_id = "S4"
        confidence = 0.85
        key_signals.append(f"近 7 天发生 {signals.conflict_frequency} 次冲突")
        key_signals.append(f"负面情绪频率 {signals.negative_sentiment:.0%}")
        if signals.response_latency > 4:
            key_signals.append(f"回复延迟增加至 {signals.response_latency:.0f} 小时")

    elif signals.response_latency > 6 and signals.initiation_ratio < 0.3:
        state_id = "S3"
        confidence = 0.75
        key_signals.append(f"回复延迟 {signals.response_latency:.0f} 小时，明显增加")
        key_signals.append(f"主动发起比例仅 {signals.initiation_ratio:.0%}")
        if signals.shared_activities < 2:
            key_signals.append(f"近 7 天共同活动仅 {signals.shared_activities} 次")

    elif (signals.response_latency <= 2 and
          signals.initiation_ratio >= 0.4 and
          signals.negative_sentiment < 0.2 and
          signals.conflict_frequency == 0):
        state_id = "S1"
        confidence = 0.80
        key_signals.append(f"回复延迟仅 {signals.response_latency:.0f} 小时，互动活跃")
        key_signals.append(f"近 7 天无冲突，情绪积极")

    else:
        state_id = "S2"
        confidence = 0.65
        key_signals.append("互动稳定，无明显异常信号")

    # ── 计算状态转移预测 ──
    transitions = TRANSITION_MATRIX.get(state_id, {})
    predicted_next = max(transitions, key=transitions.get) if transitions else state_id
    transition_prob = transitions.get(predicted_next, 0.0)

    state_info = STATES[state_id]

    return StateInferenceResult(
        current_state=state_id,
        state_name=state_info["name"],
        state_description=state_info["description"],
        confidence=confidence,
        key_signals=key_signals,
        predicted_next_state=predicted_next,
        transition_probability=transition_prob,
        rqi_delta_if_no_action=RQI_DELTA_NO_ACTION[state_id],
        urgency_level=state_info["urgency"],
        urgency_advice=URGENCY_RESPONSE_TIME[state_info["urgency"]],
        color=state_info["color"],
    )


def print_state_report(result: StateInferenceResult):
    """打印格式化的状态推断报告"""
    print("\n" + "═" * 60)
    print("  关系状态机诊断报告  State Engine Report")
    print("═" * 60)

    print(f"\n{result.color} 当前状态：{result.current_state} — {result.state_name}")
    print(f"   {result.state_description}")
    print(f"   判定置信度：{result.confidence:.0%}")

    print(f"\n📡 关键信号：")
    for sig in result.key_signals:
        print(f"   • {sig}")

    print(f"\n🔮 预测（不干预）：")
    next_state_info = STATES.get(result.predicted_next_state, {})
    next_name = next_state_info.get("name", result.predicted_next_state)
    print(f"   下一状态：{result.predicted_next_state} — {next_name}")
    print(f"   转移概率：{result.transition_probability:.0%}")
    delta = result.rqi_delta_if_no_action
    delta_str = f"+{delta:.1f}" if delta >= 0 else f"{delta:.1f}"
    print(f"   RQI 变化：{delta_str}（每周，不干预情况下）")

    print(f"\n⚡ 紧急程度：{result.urgency_level}")
    print(f"   {result.urgency_advice}")
    print("═" * 60 + "\n")


def interactive_mode():
    """交互式信号录入模式"""
    print("\n═══════════════════════════════════════")
    print("  partner.skill — 关系状态机")
    print("  请回答以下问题（直接回车使用默认值）")
    print("═══════════════════════════════════════\n")

    def ask_float(prompt, default):
        val = input(f"{prompt} [默认: {default}]: ").strip()
        return float(val) if val else default

    def ask_int(prompt, default):
        val = input(f"{prompt} [默认: {default}]: ").strip()
        return int(val) if val else default

    def ask_bool(prompt, default):
        val = input(f"{prompt} (y/n) [默认: {'y' if default else 'n'}]: ").strip().lower()
        if val == 'y':
            return True
        elif val == 'n':
            return False
        return default

    signals = ObservableSignals(
        response_latency=ask_float("对方平均回复延迟（小时）", 1.0),
        initiation_ratio=ask_float("你主动发起对话的比例（0.0–1.0）", 0.5),
        negative_sentiment=ask_float("对话中负面情绪词的频率（0.0–1.0）", 0.1),
        conflict_frequency=ask_int("近 7 天发生冲突次数", 0),
        physical_intimacy=ask_int("近 7 天肢体亲密行为评分（0–5）", 3),
        shared_activities=ask_int("近 7 天共同活动次数", 3),
        withdrawal_signals=ask_bool("是否出现情绪撤退信号（冷战、已读不回）", False),
        explicit_negative=ask_bool("是否出现明确的分离或分手讨论", False),
    )

    result = infer_state(signals)
    print_state_report(result)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="partner.skill 关系状态机 — 判定当前关系状态并预测转移"
    )
    parser.add_argument("--interactive", action="store_true", help="交互式模式")
    parser.add_argument("--signals", type=str, help="JSON 格式的信号输入")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出结果")
    args = parser.parse_args()

    if args.interactive:
        result = interactive_mode()
    elif args.signals:
        try:
            signals_dict = json.loads(args.signals)
            signals = ObservableSignals(**signals_dict)
            result = infer_state(signals)
            if args.json:
                print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
            else:
                print_state_report(result)
        except (json.JSONDecodeError, TypeError) as e:
            print(f"错误：无效的信号输入 — {e}")
            sys.exit(1)
    else:
        # 默认：运行示例
        print("\n[示例模式] 模拟冲突期信号...")
        signals = ObservableSignals(
            response_latency=5.0,
            initiation_ratio=0.25,
            negative_sentiment=0.55,
            conflict_frequency=3,
            physical_intimacy=1,
            shared_activities=1,
            withdrawal_signals=True,
            explicit_negative=False,
        )
        result = infer_state(signals)
        print_state_report(result)


if __name__ == "__main__":
    main()
