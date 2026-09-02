#!/usr/bin/env python3
"""
counterfactual_engine.py — 反事实模拟引擎（Counterfactual Engine）
partner.skill 差异化核心：模拟多条回应路径，预测每条路径的 RQI 影响，输出最优选择。

Usage:
    python3 counterfactual_engine.py --interactive
    python3 counterfactual_engine.py --demo
"""

import json
import sys
import argparse
from dataclasses import dataclass, asdict, field
from typing import Optional, List


# ─────────────────────────────────────────────
# 影响系数矩阵
# ─────────────────────────────────────────────

# (情绪状态, 策略类型) → RQI 影响基础值
IMPACT_MATRIX = {
    ("angry",    "soothing"):        +0.8,
    ("angry",    "defensive"):       -1.2,
    ("angry",    "withdraw"):        -0.3,
    ("angry",    "problem_solving"): -0.6,
    ("angry",    "dismissive"):      -1.8,
    ("angry",    "empathy"):         +0.7,
    ("angry",    "humor"):           -0.5,  # 生气时开玩笑通常适得其反

    ("anxious",  "soothing"):        +1.0,
    ("anxious",  "reassurance"):     +0.9,
    ("anxious",  "dismissive"):      -1.5,
    ("anxious",  "withdraw"):        -1.2,
    ("anxious",  "empathy"):         +0.8,
    ("anxious",  "problem_solving"): -0.3,

    ("avoidant", "space_giving"):    +0.8,
    ("avoidant", "pressure"):        -1.4,
    ("avoidant", "light_reconnect"): +0.5,
    ("avoidant", "soothing"):        +0.3,
    ("avoidant", "withdraw"):        +0.6,

    ("sad",      "empathy"):         +1.0,
    ("sad",      "advice_giving"):   -0.4,
    ("sad",      "distraction"):     +0.3,
    ("sad",      "soothing"):        +0.8,
    ("sad",      "dismissive"):      -1.2,

    ("neutral",  "any"):             +0.2,
    ("neutral",  "soothing"):        +0.3,
    ("neutral",  "problem_solving"): +0.4,
    ("neutral",  "deep_connect"):    +0.6,
}

# 依恋类型修正系数
ATTACHMENT_MODIFIER = {
    "secure":   1.0,
    "anxious":  1.3,   # 情绪放大效应
    "avoidant": 0.7,   # 情绪抑制，效果衰减
    "fearful":  1.5,   # 最不稳定，极端反应概率高
}

# 策略类型的中文名称
STRATEGY_TYPE_NAMES = {
    "soothing":        "安抚型",
    "defensive":       "辩解型",
    "withdraw":        "拉开距离型",
    "problem_solving": "问题导向型",
    "dismissive":      "忽视型",
    "empathy":         "共情型",
    "reassurance":     "安全感给予型",
    "pressure":        "施压型",
    "space_giving":    "给予空间型",
    "light_reconnect": "轻度重连型",
    "advice_giving":   "建议给予型",
    "distraction":     "转移注意型",
    "deep_connect":    "深度连接型",
    "humor":           "幽默化解型",
    "any":             "通用型",
}

# 情绪状态的中文名称
EMOTIONAL_STATE_NAMES = {
    "angry":   "愤怒",
    "anxious": "焦虑/不安",
    "sad":     "悲伤",
    "neutral": "平静",
    "happy":   "开心",
}

# 预测的伴侣反应模板
REACTION_TEMPLATES = {
    ("angry",    "soothing"):        "情绪开始软化，可能沉默或简短回应，防御性降低",
    ("angry",    "defensive"):       "防御升级，反击更激烈，可能引发更大冲突",
    ("angry",    "dismissive"):      "情绪崩溃，感到被忽视，可能触发最深层的恐惧",
    ("angry",    "problem_solving"): "感到不被理解，'你只关心解决问题，不关心我的感受'",
    ("angry",    "empathy"):         "感到被看见，情绪逐渐平复，愿意继续对话",
    ("anxious",  "soothing"):        "焦虑水平下降，安全感提升，可能主动靠近",
    ("anxious",  "reassurance"):     "核心恐惧得到回应，情绪稳定，关系信任增强",
    ("anxious",  "dismissive"):      "触发被抛弃恐惧，可能出现极端情绪反应",
    ("anxious",  "withdraw"):        "焦虑加剧，灾难化思维启动，'ta 不在乎我了'",
    ("avoidant", "space_giving"):    "压力降低，可能在 24-48 小时后主动联系",
    ("avoidant", "pressure"):        "触发逃跑反应，进一步退缩，互动频率降低",
    ("sad",      "empathy"):         "感到被理解，情绪得到释放，愿意分享更多",
    ("sad",      "advice_giving"):   "感到不被理解，'我只是想被听见，不是要你解决问题'",
    ("neutral",  "deep_connect"):    "情感连接加深，亲密度提升，关系质量改善",
}


# ─────────────────────────────────────────────
# 数据结构
# ─────────────────────────────────────────────

@dataclass
class CandidateResponse:
    """候选回应"""
    id: str
    text: str
    strategy_type: str


@dataclass
class SimulationResult:
    """单条回应的模拟结果"""
    response_id: str
    response_text: str
    strategy_type: str
    strategy_name: str
    partner_reaction: str
    emotional_outcome: str    # positive / neutral / negative
    rqi_delta: float
    confidence: float
    risk_factors: List[str]
    follow_up_state: str
    rank: int = 0


@dataclass
class CounterfactualReport:
    """完整的反事实模拟报告"""
    situation: str
    partner_attachment: str
    partner_emotional_state: str
    current_relationship_state: str
    simulations: List[SimulationResult]
    recommended_response_id: str
    worst_response_id: str
    reasoning: str


# ─────────────────────────────────────────────
# 核心模拟逻辑
# ─────────────────────────────────────────────

def simulate_response(
    candidate: CandidateResponse,
    emotional_state: str,
    attachment_type: str,
    current_state: str,
) -> SimulationResult:
    """模拟单条回应的影响"""

    # 获取基础影响值
    impact_key = (emotional_state, candidate.strategy_type)
    base_impact = IMPACT_MATRIX.get(
        impact_key,
        IMPACT_MATRIX.get(("neutral", "any"), +0.2)
    )

    # 依恋类型修正
    modifier = ATTACHMENT_MODIFIER.get(attachment_type, 1.0)
    rqi_delta = round(base_impact * modifier, 2)

    # 情绪结果判定
    if rqi_delta > 0.3:
        emotional_outcome = "positive"
    elif rqi_delta < -0.3:
        emotional_outcome = "negative"
    else:
        emotional_outcome = "neutral"

    # 伴侣反应预测
    reaction_key = (emotional_state, candidate.strategy_type)
    partner_reaction = REACTION_TEMPLATES.get(
        reaction_key,
        "反应不确定，取决于当前具体情境和双方互动历史"
    )

    # 置信度计算（基于数据充分性）
    confidence = 0.75 if impact_key in IMPACT_MATRIX else 0.55
    if attachment_type == "fearful":
        confidence -= 0.10  # 恐惧-回避型最不可预测

    # 风险因素识别
    risk_factors = []
    if rqi_delta < -0.8:
        risk_factors.append("高风险：可能触发对方的核心防御机制")
    if candidate.strategy_type == "defensive":
        risk_factors.append("辩解型策略在情绪激活时几乎总是适得其反")
    if candidate.strategy_type == "problem_solving" and emotional_state in ["angry", "anxious"]:
        risk_factors.append("情绪未平复时谈问题，对方会感到不被理解")
    if candidate.strategy_type == "withdraw" and attachment_type == "anxious":
        risk_factors.append("对焦虑型依恋使用拉开距离策略会加剧其焦虑")
    if candidate.strategy_type == "pressure" and attachment_type == "avoidant":
        risk_factors.append("对回避型依恋施压会触发逃跑反应，适得其反")

    # 预测后续关系状态
    state_num = int(current_state[1]) if current_state and len(current_state) > 1 else 2
    if rqi_delta > 0.5:
        next_num = max(1, state_num - 1)
    elif rqi_delta < -0.5:
        next_num = min(6, state_num + 1)
    else:
        next_num = state_num
    follow_up_state = f"S{next_num}"

    return SimulationResult(
        response_id=candidate.id,
        response_text=candidate.text,
        strategy_type=candidate.strategy_type,
        strategy_name=STRATEGY_TYPE_NAMES.get(candidate.strategy_type, candidate.strategy_type),
        partner_reaction=partner_reaction,
        emotional_outcome=emotional_outcome,
        rqi_delta=rqi_delta,
        confidence=confidence,
        risk_factors=risk_factors,
        follow_up_state=follow_up_state,
    )


def run_counterfactual(
    situation: str,
    candidates: List[CandidateResponse],
    attachment_type: str,
    emotional_state: str,
    current_state: str,
) -> CounterfactualReport:
    """运行完整的反事实模拟"""

    simulations = []
    for candidate in candidates:
        result = simulate_response(candidate, emotional_state, attachment_type, current_state)
        simulations.append(result)

    # 按 RQI 影响排序
    simulations.sort(key=lambda x: x.rqi_delta, reverse=True)
    for i, sim in enumerate(simulations):
        sim.rank = i + 1

    recommended_id = simulations[0].response_id if simulations else ""
    worst_id = simulations[-1].response_id if simulations else ""

    best = simulations[0] if simulations else None
    worst = simulations[-1] if simulations else None

    reasoning = (
        f"基于伴侣的{ATTACHMENT_MODIFIER.get(attachment_type, 1.0):.1f}x 依恋修正系数"
        f"（{attachment_type}型）和当前情绪状态（{EMOTIONAL_STATE_NAMES.get(emotional_state, emotional_state)}），"
    )
    if best:
        reasoning += f"回应 {best.response_id}（{best.strategy_name}）预期 RQI 变化最高（{best.rqi_delta:+.2f}）"
    if worst:
        reasoning += f"，回应 {worst.response_id}（{worst.strategy_name}）预期 RQI 变化最低（{worst.rqi_delta:+.2f}），应当避免。"

    return CounterfactualReport(
        situation=situation,
        partner_attachment=attachment_type,
        partner_emotional_state=emotional_state,
        current_relationship_state=current_state,
        simulations=simulations,
        recommended_response_id=recommended_id,
        worst_response_id=worst_id,
        reasoning=reasoning,
    )


def print_counterfactual_report(report: CounterfactualReport):
    """打印格式化的反事实模拟报告"""
    print("\n" + "═" * 65)
    print("  反事实模拟引擎报告  Counterfactual Engine Report")
    print("═" * 65)

    print(f"\n📍 情境：{report.situation}")
    att_name = {"secure": "安全型", "anxious": "焦虑型", "avoidant": "回避型", "fearful": "恐惧-回避型"}.get(
        report.partner_attachment, report.partner_attachment
    )
    emo_name = EMOTIONAL_STATE_NAMES.get(report.partner_emotional_state, report.partner_emotional_state)
    print(f"🧠 伴侣画像：{att_name}依恋 | 当前情绪：{emo_name} | 关系状态：{report.current_relationship_state}")

    print(f"\n{'─' * 65}")
    print("  多路径模拟结果")
    print(f"{'─' * 65}")

    outcome_icons = {"positive": "✅", "neutral": "➡️", "negative": "❌"}
    rank_icons = {1: "🥇", 2: "🥈", 3: "🥉"}

    for sim in report.simulations:
        rank_icon = rank_icons.get(sim.rank, f"#{sim.rank}")
        outcome_icon = outcome_icons.get(sim.emotional_outcome, "❓")
        delta_str = f"{sim.rqi_delta:+.2f}"

        print(f"\n{rank_icon} 回应 {sim.response_id}：{sim.strategy_name}  {outcome_icon}")
        print(f'   "{sim.response_text}"')
        print(f"   预测伴侣反应：{sim.partner_reaction}")
        print(f"   RQI 变化：{delta_str}  |  置信度：{sim.confidence:.0%}  |  预测后续状态：{sim.follow_up_state}")
        if sim.risk_factors:
            for risk in sim.risk_factors:
                print(f"   ⚠️  {risk}")

    print(f"\n{'─' * 65}")
    print(f"✅ 推荐回应：回应 {report.recommended_response_id}")
    print(f"🚫 最差回应：回应 {report.worst_response_id}（请避免）")
    print(f"\n💡 推断依据：{report.reasoning}")
    print("═" * 65 + "\n")


def run_demo():
    """运行内置演示：伴侣因取消约会而生气"""
    situation = "伴侣因你临时取消约会而生气，发来'随便'"
    candidates = [
        CandidateResponse("A", "我也不想啊，但工作真的没办法，你能不能理解一下？", "defensive"),
        CandidateResponse("B", "宝宝，对不起，我知道你很失望。你期待了这么久，是我让你失望了。我现在就去想怎么补偿你，好吗？", "soothing"),
        CandidateResponse("C", "你说'随便'是什么意思？我们能不能好好说？", "problem_solving"),
        CandidateResponse("D", "好的，那就随便吧。", "dismissive"),
    ]

    print("\n[演示模式] 情境：伴侣因取消约会而生气（焦虑型依恋，冲突期 S4）")
    report = run_counterfactual(
        situation=situation,
        candidates=candidates,
        attachment_type="anxious",
        emotional_state="angry",
        current_state="S4",
    )
    print_counterfactual_report(report)


def interactive_mode():
    """交互式模拟模式"""
    print("\n═══════════════════════════════════════")
    print("  partner.skill — 反事实模拟引擎")
    print("═══════════════════════════════════════\n")

    situation = input("请描述当前情境：").strip() or "伴侣生气了"

    print("\n依恋类型：secure / anxious / avoidant / fearful")
    attachment = input("伴侣的依恋类型 [默认: anxious]: ").strip() or "anxious"

    print("\n情绪状态：angry / anxious / sad / neutral / happy")
    emotional = input("伴侣当前情绪状态 [默认: angry]: ").strip() or "angry"

    state = input("当前关系状态 S1-S6 [默认: S4]: ").strip() or "S4"

    print("\n请输入 2-4 条候选回应（输入空行结束）：")
    print("格式：[回应文本] | [策略类型]")
    print("策略类型：soothing / defensive / empathy / problem_solving / dismissive / space_giving / reassurance")

    candidates = []
    ids = "ABCDE"
    for i, rid in enumerate(ids):
        line = input(f"回应 {rid}（直接回车结束）: ").strip()
        if not line:
            break
        parts = line.split("|")
        text = parts[0].strip()
        strategy = parts[1].strip() if len(parts) > 1 else "soothing"
        candidates.append(CandidateResponse(rid, text, strategy))

    if not candidates:
        print("未输入候选回应，使用演示数据。")
        run_demo()
        return

    report = run_counterfactual(situation, candidates, attachment, emotional, state)
    print_counterfactual_report(report)


def main():
    parser = argparse.ArgumentParser(
        description="partner.skill 反事实模拟引擎 — 模拟多条回应路径的 RQI 影响"
    )
    parser.add_argument("--interactive", action="store_true", help="交互式模式")
    parser.add_argument("--demo", action="store_true", help="运行内置演示")
    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.demo:
        run_demo()
    else:
        run_demo()


if __name__ == "__main__":
    main()
