# Counterfactual Engine — 反事实模拟引擎

## 概述

反事实模拟引擎（Counterfactual Engine）是 partner.skill 的差异化核心能力。它将同一个情境下的多条可能回应路径进行并行模拟，预测每条路径对伴侣情绪状态和关系质量指数（RQI）的影响，并按预期结果排序，帮助用户在行动前看清选择的后果。

> **核心价值**：把 skill 从"解释器"变成"模拟器"。你不再只是被告知"应该怎么做"，而是能够亲眼看到"如果我这样做，会发生什么"。

---

## 模拟框架

### 输入参数

```
SIMULATION_INPUT = {
    "situation": str,           # 当前情境描述
    "partner_state": {
        "emotional_state": str, # 当前情绪状态（angry/sad/anxious/neutral/happy）
        "attachment_type": str, # 依恋类型
        "current_state": str,   # 关系状态 S1-S6
    },
    "candidate_responses": [    # 待模拟的候选回应（2-4条）
        {"id": "A", "text": str, "strategy_type": str},
        {"id": "B", "text": str, "strategy_type": str},
        ...
    ]
}
```

### 输出结构

```
SIMULATION_OUTPUT = {
    "simulations": [
        {
            "response_id": "A",
            "response_text": str,
            "strategy_type": str,
            "partner_reaction": str,          # 预测的伴侣反应描述
            "emotional_outcome": str,         # 情绪结果（positive/neutral/negative）
            "rqi_delta": float,               # RQI 变化量（-2.0 到 +2.0）
            "confidence": float,              # 预测置信度（0-1）
            "risk_factors": [str],            # 潜在风险
            "follow_up_state": str,           # 预测的后续关系状态
        }
    ],
    "recommended_response": "A",              # 推荐的最优回应
    "worst_response": "C",                    # 最差回应（需要避免）
    "reasoning": str,
}
```

---

## RQI 影响评估规则

### 情绪状态 × 策略类型 → 影响系数

```
IMPACT_MATRIX = {
    # (emotional_state, strategy_type) → rqi_multiplier

    ("angry",   "soothing"):       +0.8,
    ("angry",   "defensive"):      -1.2,
    ("angry",   "withdraw"):       -0.3,   # 回避型：+0.4，焦虑型：-0.8
    ("angry",   "problem_solving"): -0.6,  # 情绪未平复时谈问题会加剧冲突

    ("anxious", "soothing"):       +1.0,
    ("anxious", "reassurance"):    +0.9,
    ("anxious", "dismissive"):     -1.5,
    ("anxious", "withdraw"):       -1.2,

    ("avoidant","space_giving"):   +0.8,
    ("avoidant","pressure"):       -1.4,
    ("avoidant","light_reconnect"): +0.5,

    ("sad",     "empathy"):        +1.0,
    ("sad",     "advice_giving"):  -0.4,   # 对方想被理解，不是被解决
    ("sad",     "distraction"):    +0.3,

    ("neutral", "any"):            +0.2,   # 中性情绪下任何合理策略都有小幅正效应
}
```

### 依恋类型修正系数

```
ATTACHMENT_MODIFIER = {
    "secure":   1.0,   # 安全型：策略效果接近预期
    "anxious":  1.3,   # 焦虑型：情绪放大效应，好的更好，坏的更坏
    "avoidant": 0.7,   # 回避型：情绪抑制，效果衰减
    "fearful":  1.5,   # 恐惧-回避型：最不稳定，极端反应概率高
}
```

---

## 标准模拟示例

### 情境：伴侣因你临时取消约会而生气，发来"随便"

**候选回应**：

**回应 A（辩解型）**：
> "我也不想啊，但工作真的没办法，你能不能理解一下？"

**回应 B（安抚型）**：
> "宝宝，对不起，我知道你很失望。你期待了这么久，是我让你失望了。我现在就去想怎么补偿你，好吗？"

**回应 C（问题导向型）**：
> "你说'随便'是什么意思？我们能不能好好说？"

**回应 D（忽视型）**：
> "好的，那就随便吧。"

---

### 模拟结果（伴侣：焦虑型依恋，当前状态 S4）

| 回应 | 策略类型 | 伴侣预期反应 | RQI 变化 | 置信度 | 推荐 |
|------|----------|-------------|----------|--------|------|
| A | 辩解型 | 防御升级，"你就知道找借口" | -1.2 | 85% | ❌ 最差 |
| B | 安抚型 | 情绪软化，可能回复"算了" | +0.8 | 82% | ✅ 最优 |
| C | 追问型 | 情绪激化，"你还问我什么意思？" | -0.8 | 78% | ❌ 避免 |
| D | 忽视型 | 情绪崩溃，触发焦虑型最深恐惧 | -1.8 | 90% | 🚨 危险 |

**推荐回应**：B（安抚型）

**核心理由**：焦虑型依恋在冲突期（S4）的核心需求是"被看见"和"被重视"。回应 B 首先承认了对方的情绪，然后给出了具体的补偿意愿，符合 P1（安抚型）策略的执行逻辑。回应 A 虽然是事实，但在对方情绪激活时，任何解释都会被解读为"你在为自己辩解，不在乎我的感受"。

---

## 高级模拟：长期路径预测

除了单次回应的即时效果，反事实引擎还能模拟**3 步路径**的累积 RQI 影响：

```
PATH_SIMULATION = {
    "path_A": {
        "step_1": "回应 B（安抚型）",
        "step_2": "当天晚上主动发消息关心",
        "step_3": "周末补偿约会",
        "cumulative_rqi_delta": +2.1,
        "predicted_state_after": "S2（稳定期）",
    },
    "path_B": {
        "step_1": "回应 A（辩解型）",
        "step_2": "等对方先联系",
        "step_3": "约会继续推迟",
        "cumulative_rqi_delta": -2.8,
        "predicted_state_after": "S5（冷却期）",
    }
}
```

---

## 与其他引擎的协作

反事实引擎在执行协议的 Step 4 运行，它的输入来自：
- **State Engine**：当前关系状态 S_t 和伴侣情绪状态 E_t
- **Policy Selector**：已选定的最优策略类型
- **Persona Builder**：伴侣的依恋类型和爱的语言

它的输出直接进入 **Action Generator**（话术生成），为用户提供经过模拟验证的最优回应。

```
State Engine → Policy Selector → Counterfactual Engine → Action Generator
     S_t              P_i              模拟排序                最终话术
```
