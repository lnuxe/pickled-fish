#!/usr/bin/env python3
"""
policy_selector.py — 策略选择器（Policy Layer）
partner.skill 决策核心：根据依恋类型 × 关系状态 × 冲突类型，输出最优干预策略。

Usage:
    python3 policy_selector.py --interactive
    python3 policy_selector.py --attachment anxious --state S4 --conflict gottman_stonewalling
"""

import json
import sys
import argparse
from dataclasses import dataclass, asdict
from typing import Optional, List


# ─────────────────────────────────────────────
# 策略定义
# ─────────────────────────────────────────────

STRATEGIES = {
    "P1": {
        "name": "安抚型（Soothing）",
        "core": "降低对方情绪激活水平，建立安全感",
        "best_for": "焦虑型依恋 + 冲突后",
        "rqi_impact": +0.8,
        "forbidden": [
            "立即解释和辩解（会被解读为'你不在乎我的感受'）",
            "问'你到底想要什么'（会增加压力）",
            "沉默超过 2 小时（会触发焦虑型的灾难化思维）",
        ],
        "steps": [
            "首先承认对方的情绪（不评判，不解释）",
            "表达你理解 ta 的感受",
            "给出具体的安全信号（行动，而非语言）",
            "在情绪稳定后，才进入问题讨论",
        ],
        "script": "我知道你现在很[情绪词]。这是我的错，我让你感到[核心恐惧]。我不会走的。我们等你准备好了再聊，好吗？",
    },
    "P2": {
        "name": "拉开距离（Withdraw）",
        "core": "主动减少互动频率，降低对方压力",
        "best_for": "回避型依恋 + 追逃模式",
        "rqi_impact": +0.6,
        "forbidden": [
            "连续发消息追问（每条消息都是压力）",
            "要求解释和承诺（触发逃跑反应）",
            "情绪化表达（'你不在乎我'）",
        ],
        "steps": [
            "停止主动联系 24–48 小时",
            "如果对方联系，简短回复，不追问，先结束对话",
            "在中性场景中重新建立轻松互动",
            "等对方主动提起问题，再进入讨论",
        ],
        "script": "好的，我理解。我们都冷静一下。[然后不再发消息，等待对方主动]",
    },
    "P3": {
        "name": "重新吸引（Attraction Rebuild）",
        "core": "重建吸引力和新鲜感，打破稳定期平淡",
        "best_for": "稳定期滑向疏离",
        "rqi_impact": +1.0,
        "forbidden": [
            "重复同样的约会模式",
            "过度依赖对方寻找新鲜感",
        ],
        "steps": [
            "打破常规（换一个从未去过的地方约会）",
            "展示成长（分享你最近的新技能或新想法）",
            "制造适度的神秘感（不要 24 小时随时响应）",
            "回忆热恋期的共同记忆，重新激活情感连接",
        ],
        "script": "我最近发现了一个地方，感觉你会喜欢。这周末要不要一起去？",
    },
    "P4": {
        "name": "边界建立（Boundary Setting）",
        "core": "清晰表达需求和底线，重建平等权力结构",
        "best_for": "权力失衡 + 被动方",
        "rqi_impact": +0.7,
        "forbidden": [
            "使用'你总是'或'你从不'（绝对化指责）",
            "在情绪激动时谈边界（会变成攻击）",
        ],
        "steps": [
            "使用'我'陈述，而非'你'指责",
            "描述具体行为，而非评判人格",
            "表达你的感受和需求",
            "提出具体的改变请求",
        ],
        "script": "当[具体行为]发生时，我感到[情绪]，因为我需要[核心需求]。我希望我们可以[具体请求]。",
    },
    "P5": {
        "name": "主动修复（Active Repair）",
        "core": "主动发起和解，使用 Gottman 修复尝试",
        "best_for": "冲突期 + 安全型依恋",
        "rqi_impact": +1.2,
        "forbidden": [
            "在对方情绪激动时强行修复（会被拒绝）",
            "道歉后立即重提争议点",
        ],
        "steps": [
            "等待情绪降温（至少 20 分钟后）",
            "主动发起修复尝试",
            "承认自己在冲突中的责任",
            "表达对关系的重视",
        ],
        "script": "我很抱歉，我说那句话的方式是错的。我知道这对你来说很重要。我们是一个团队。",
    },
    "P6": {
        "name": "深度连接（Deep Connection）",
        "core": "创造高质量情感共鸣时刻，强化亲密度",
        "best_for": "稳定期维护 + S1 巩固",
        "rqi_impact": +0.5,
        "forbidden": [
            "把深度连接变成例行公事",
            "在对方疲惫时强行深度对话",
        ],
        "steps": [
            "创造无干扰的专属时间（关掉手机）",
            "分享你的内心世界（脆弱性是亲密的催化剂）",
            "认真倾听，不急于给建议",
            "表达感激和欣赏",
        ],
        "script": "我最近一直在想，和你在一起让我感到[具体感受]。我很庆幸有你。",
    },
    "P7": {
        "name": "危机干预（Crisis Intervention）",
        "core": "直接面对核心问题，防止关系破裂",
        "best_for": "S5/S6 + 明确负面信号",
        "rqi_impact": +1.5,  # 如果成功
        "forbidden": [
            "回避核心问题（只会延迟破裂）",
            "在公共场所或对方疲惫时进行",
            "把危机对话变成指责清单",
        ],
        "steps": [
            "选择合适的时机和场所（私密、安静）",
            "直接表达你对这段关系的重视",
            "邀请对方分享 ta 真实的感受和需求",
            "共同讨论是否愿意一起努力改变",
            "如果双方都愿意，制定具体的行动计划",
        ],
        "script": "我想认真跟你聊聊我们的关系。我很在乎你，也很在乎我们。我想知道你现在真实的感受是什么。",
    },
}

# 策略选择矩阵：(依恋类型, 状态) → [主策略, 次策略]
STRATEGY_MATRIX = {
    ("secure",   "S1"): ["P6", "P3"],
    ("secure",   "S2"): ["P6", "P3"],
    ("secure",   "S3"): ["P3", "P6"],
    ("secure",   "S4"): ["P5", "P1"],
    ("secure",   "S5"): ["P5", "P7"],
    ("secure",   "S6"): ["P7", "P5"],

    ("anxious",  "S1"): ["P6", "P1"],
    ("anxious",  "S2"): ["P1", "P6"],
    ("anxious",  "S3"): ["P1", "P3"],
    ("anxious",  "S4"): ["P1", "P4"],
    ("anxious",  "S5"): ["P1", "P7"],
    ("anxious",  "S6"): ["P7", "P1"],

    ("avoidant", "S1"): ["P6", "P2"],
    ("avoidant", "S2"): ["P2", "P6"],
    ("avoidant", "S3"): ["P2", "P3"],
    ("avoidant", "S4"): ["P2", "P4"],
    ("avoidant", "S5"): ["P2", "P7"],
    ("avoidant", "S6"): ["P7", "P2"],

    ("fearful",  "S1"): ["P1", "P6"],
    ("fearful",  "S2"): ["P1", "P2"],
    ("fearful",  "S3"): ["P1", "P3"],
    ("fearful",  "S4"): ["P1", "P4"],
    ("fearful",  "S5"): ["P7", "P1"],
    ("fearful",  "S6"): ["P7", "P1"],
}

# 冲突类型修正规则
CONFLICT_OVERRIDES = {
    "gottman_contempt":    ("P7", "P5"),   # 鄙视模式：最危险，直接危机干预
    "gottman_stonewalling": None,           # 冷战：依赖依恋类型决定
    "gottman_criticism":   ("P5", "P4"),   # 批评模式：主动修复 + 边界建立
    "value_conflict":      ("P4", "P5"),   # 价值观冲突：先建立边界
    "resource_conflict":   ("P5", "P4"),   # 资源冲突：协商修复
    "intimacy_conflict":   None,           # 亲密度冲突：依赖依恋类型
    "external_conflict":   ("P1", "P6"),   # 外部压力：先安抚再深度连接
}


# ─────────────────────────────────────────────
# 核心选择逻辑
# ─────────────────────────────────────────────

@dataclass
class PolicyResult:
    attachment_type: str
    state_id: str
    conflict_type: Optional[str]
    primary_strategy_id: str
    primary_strategy_name: str
    secondary_strategy_id: str
    secondary_strategy_name: str
    forbidden_actions: List[str]
    execution_steps: List[str]
    script_template: str
    estimated_rqi_impact: float
    reasoning: str


def select_policy(
    attachment_type: str,
    state_id: str,
    conflict_type: Optional[str] = None,
) -> PolicyResult:
    """
    根据依恋类型、关系状态和冲突类型选择最优策略。
    """
    attachment_type = attachment_type.lower()
    state_id = state_id.upper()

    # 从矩阵获取基础策略
    key = (attachment_type, state_id)
    base_strategies = STRATEGY_MATRIX.get(key, ["P5", "P1"])
    primary_id, secondary_id = base_strategies[0], base_strategies[1]
    reasoning = f"基于依恋类型（{attachment_type}）× 关系状态（{state_id}）矩阵推断"

    # 冲突类型修正
    if conflict_type and conflict_type in CONFLICT_OVERRIDES:
        override = CONFLICT_OVERRIDES[conflict_type]
        if override is not None:
            primary_id, secondary_id = override
            reasoning += f"，并根据冲突类型（{conflict_type}）进行策略修正"

    primary = STRATEGIES.get(primary_id, STRATEGIES["P5"])
    secondary = STRATEGIES.get(secondary_id, STRATEGIES["P1"])

    return PolicyResult(
        attachment_type=attachment_type,
        state_id=state_id,
        conflict_type=conflict_type,
        primary_strategy_id=primary_id,
        primary_strategy_name=primary["name"],
        secondary_strategy_id=secondary_id,
        secondary_strategy_name=secondary["name"],
        forbidden_actions=primary["forbidden"],
        execution_steps=primary["steps"],
        script_template=primary["script"],
        estimated_rqi_impact=primary["rqi_impact"],
        reasoning=reasoning,
    )


def print_policy_report(result: PolicyResult):
    """打印格式化的策略报告"""
    print("\n" + "═" * 60)
    print("  策略选择器报告  Policy Selector Report")
    print("═" * 60)

    print(f"\n🧠 推断依据：{result.reasoning}")

    print(f"\n✅ 主策略：{result.primary_strategy_id} — {result.primary_strategy_name}")
    print(f"   预期 RQI 影响：+{result.estimated_rqi_impact:.1f}")

    print(f"\n🔄 备选策略：{result.secondary_strategy_id} — {result.secondary_strategy_name}")

    print(f"\n🚫 禁止行为：")
    for action in result.forbidden_actions:
        print(f"   ✗ {action}")

    print(f"\n📋 执行步骤：")
    for i, step in enumerate(result.execution_steps, 1):
        print(f"   {i}. {step}")

    print(f"\n💬 话术模板：")
    print(f'   "{result.script_template}"')
    print("═" * 60 + "\n")


ATTACHMENT_NAMES = {
    "secure": "安全型",
    "anxious": "焦虑型",
    "avoidant": "回避型",
    "fearful": "恐惧-回避型",
}

CONFLICT_NAMES = {
    "gottman_contempt": "鄙视模式（Gottman 四骑士）",
    "gottman_stonewalling": "冷战/冷暴力",
    "gottman_criticism": "批评模式",
    "value_conflict": "价值观冲突",
    "resource_conflict": "资源冲突",
    "intimacy_conflict": "亲密度冲突",
    "external_conflict": "外部压力引发",
}


def interactive_mode():
    """交互式策略选择模式"""
    print("\n═══════════════════════════════════════")
    print("  partner.skill — 策略选择器")
    print("═══════════════════════════════════════\n")

    print("依恋类型选项：")
    for k, v in ATTACHMENT_NAMES.items():
        print(f"  {k} = {v}")
    attachment = input("\n请输入伴侣的依恋类型 [默认: anxious]: ").strip() or "anxious"

    print("\n关系状态选项：S1（热恋）S2（稳定）S3（疏离）S4（冲突）S5（冷却）S6（破裂边缘）")
    state = input("请输入当前关系状态 [默认: S4]: ").strip() or "S4"

    print("\n冲突类型选项（可选）：")
    for k, v in CONFLICT_NAMES.items():
        print(f"  {k} = {v}")
    conflict = input("\n请输入冲突类型（直接回车跳过）: ").strip() or None

    result = select_policy(attachment, state, conflict)
    print_policy_report(result)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="partner.skill 策略选择器 — 输出最优干预策略"
    )
    parser.add_argument("--interactive", action="store_true", help="交互式模式")
    parser.add_argument("--attachment", type=str, help="依恋类型: secure/anxious/avoidant/fearful")
    parser.add_argument("--state", type=str, help="关系状态: S1-S6")
    parser.add_argument("--conflict", type=str, help="冲突类型（可选）")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.attachment and args.state:
        result = select_policy(args.attachment, args.state, args.conflict)
        if args.json:
            print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        else:
            print_policy_report(result)
    else:
        # 默认示例：回避型 + 冷战
        print("[示例模式] 回避型依恋 + 冷战（S5）...")
        result = select_policy("avoidant", "S5", "gottman_stonewalling")
        print_policy_report(result)


if __name__ == "__main__":
    main()
