# State Engine — 关系状态机

## 概述

关系状态机（Relationship State Machine）是 partner.skill 的核心推理层。它将当前关系的所有可观测信号映射到一个离散状态空间，并预测在不干预情况下的状态转移路径，从而为策略选择器（Policy Selector）提供输入。

---

## 状态空间定义

| 状态 ID | 状态名称 | 核心特征 | RQI 区间 |
|---------|----------|----------|----------|
| S1 | 热恋期（Honeymoon） | 高亲密 + 高回应 + 主动互动频繁 | 8.0–10.0 |
| S2 | 稳定期（Stable） | 中亲密 + 稳定互动 + 冲突少且可修复 | 6.0–7.9 |
| S3 | 轻度疏离（Mild Drift） | 低主动 + 回复延迟 + 共同活动减少 | 4.5–5.9 |
| S4 | 冲突期（Active Conflict） | 负面情绪主导 + 高频摩擦 + 防御行为增加 | 3.0–5.5 |
| S5 | 冷却期（Emotional Withdrawal） | 低互动 + 情绪撤退 + 单方或双方回避 | 2.0–3.9 |
| S6 | 破裂边缘（Critical） | 极低互动 + 明确负面信号 + 分离讨论出现 | 0.0–2.5 |

---

## Step 1: 状态推断（State Inference）

### 输入信号矩阵

从用户描述和聊天记录中提取以下可观测信号：

```
OBSERVABLE_SIGNALS = {
    "response_latency":    float,   # 平均回复延迟（小时）
    "initiation_ratio":    float,   # 用户主动发起 / 总互动次数（0–1）
    "negative_sentiment":  float,   # 负面情绪词频率（0–1）
    "conflict_frequency":  int,     # 近 7 天冲突次数
    "physical_intimacy":   int,     # 近 7 天肢体亲密行为（0–5 评分）
    "shared_activities":   int,     # 近 7 天共同活动次数
    "withdrawal_signals":  bool,    # 是否出现情绪撤退信号
    "explicit_negative":   bool,    # 是否出现明确分离/分手讨论
}
```

### 状态判定规则

```
IF explicit_negative == True:
    → S6（破裂边缘）

ELIF withdrawal_signals == True AND negative_sentiment > 0.5:
    → S5（冷却期）

ELIF conflict_frequency >= 3 AND negative_sentiment > 0.4:
    → S4（冲突期）

ELIF response_latency > 6 AND initiation_ratio < 0.3:
    → S3（轻度疏离）

ELIF response_latency <= 2 AND initiation_ratio >= 0.4 AND negative_sentiment < 0.2:
    → S1（热恋期）

ELSE:
    → S2（稳定期）
```

---

## Step 2: 状态转移预测（Transition Prediction）

### 转移矩阵（无干预情况下的自然漂移）

```
TRANSITION_MATRIX = {
    "S1": {"S1": 0.60, "S2": 0.35, "S3": 0.05},
    "S2": {"S1": 0.10, "S2": 0.55, "S3": 0.25, "S4": 0.10},
    "S3": {"S2": 0.20, "S3": 0.40, "S4": 0.25, "S5": 0.15},
    "S4": {"S2": 0.15, "S3": 0.20, "S4": 0.30, "S5": 0.25, "S6": 0.10},
    "S5": {"S3": 0.10, "S4": 0.15, "S5": 0.45, "S6": 0.30},
    "S6": {"S5": 0.20, "S6": 0.80},
}
```

### 输出格式

```
STATE_INFERENCE_RESULT = {
    "current_state": "S_t",
    "state_name": "状态名称",
    "confidence": float,          # 判定置信度（0–1）
    "key_signals": [str],         # 触发该判定的主要信号
    "predicted_next_state": "S_t+1",
    "transition_probability": float,
    "rqi_delta_if_no_action": float,  # 不干预时的 RQI 变化量（负数表示恶化）
    "urgency_level": str,         # "LOW" / "MEDIUM" / "HIGH" / "CRITICAL"
}
```

---

## Step 3: 紧急程度评估

| 状态 | 紧急程度 | 推荐响应时间 |
|------|----------|-------------|
| S1 | LOW | 维护即可，无需紧急干预 |
| S2 | LOW | 定期维护，关注趋势 |
| S3 | MEDIUM | 48 小时内主动行动 |
| S4 | HIGH | 24 小时内启动冲突修复协议 |
| S5 | HIGH | 立即启动重新连接协议 |
| S6 | CRITICAL | 立即启动危机干预，同时建议寻求专业帮助 |

---

## 状态机输出示例

```json
{
  "current_state": "S4",
  "state_name": "冲突期（Active Conflict）",
  "confidence": 0.82,
  "key_signals": [
    "近 3 天发生 2 次争吵",
    "回复延迟从 30 分钟增加到 4 小时",
    "对方使用防御性语言（'你总是这样'）"
  ],
  "predicted_next_state": "S5",
  "transition_probability": 0.25,
  "rqi_delta_if_no_action": -1.2,
  "urgency_level": "HIGH"
}
```

---

## 状态机与其他引擎的接口

```
State Engine Output
        ↓
Policy Selector（策略选择器）
        ↓
Counterfactual Engine（反事实模拟）
        ↓
Action Generator（话术生成）
```

State Engine 的输出是所有后续引擎的必要输入。在每次用户调用 `/{slug}` 时，State Engine 必须首先运行，其结果存入当前会话上下文。
