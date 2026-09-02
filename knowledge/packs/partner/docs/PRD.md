# 现任.skill —— 产品需求文档 v2.0

## 一、产品概述

**现任.skill (partner-skill)** 是一个运行在 OpenClaw 和 Claude Code 上的 meta-skill。

用户通过对话式交互提供原材料（聊天记录、邮件、备忘录、截图或手动描述），系统自动生成一个可独立运行的伴侣 Persona Skill。该 Skill 基于心理学和社会学理论（依恋理论、大五人格、Gottman 四骑士等）构建，旨在帮助用户维护和提升当前的恋爱关系。

生成的 Skill 由两个独立部分组成：

- **Part A — 关系档案 (Relationship Profile)**：基于 RQI（关系质量指数）数学模型量化的关系健康度、核心冲突模式和记忆权重库。
- **Part B — 人格画像 (Persona)**：该伴侣的性格、沟通风格、爱的语言和行为模式。

两部分可以独立使用，也可以组合运行（默认组合）。生成后的 Skill 支持通过追加文件或对话纠正持续进化。

---

## 二、用户流程

```text
用户触发 /create-partner
       ↓
[Step 1] 基础信息录入（全部可跳过）
  - 姓名/代号
  - 基础背景（性别、年龄、职业）
  - 性格快照（MBTI、星座、依恋类型、爱的语言）
       ↓
[Step 2] 原材料导入（支持多选）
  - 微信/短信聊天记录导出（TXT/JSON）
  - 邮件导出（.eml/.mbox）
  - 聊天截图（图片）
  - 备忘录/日记（Markdown/文本）
  - 直接描述（自由文本）
       ↓
[Step 3] 自动化分析与生成
  - 运行 profile_builder.py 构建基础画像
  - 运行 relationship_analyzer.py 计算 RQI、ACS、LLMI
  - 运行 chat_parser.py / email_parser.py 提取沟通模式
  - 生成 persona.md 和 relationship.md
       ↓
[Step 4] 预览与确认
  - 展示关系健康度雷达图和核心指标
  - 确认后写入 partners/{slug}/ 目录
       ↓
[Step 5] 日常调用与进化
  - /{slug} 调用场景顾问（支持 23 个生活场景）
  - /{slug}-conflict 调用冲突解决器
  - /{slug}-gift 调用送礼顾问
  - /{slug}-reflect 记录反思日志
```

---

## 三、输入信息规范

### 3.1 基础信息字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `name` | String | 是 | 伴侣的称呼、代号或全名，用于生成 slug |
| `gender` | String | 否 | 性别，影响部分心理学模型的基线假设 |
| `age` | Number | 否 | 年龄，影响人生阶段和未来规划的建议 |
| `occupation` | String | 否 | 职业，用于分析职业压力和作息规律 |

### 3.2 心理学与性格标签

| 标签维度 | 理论基础 | 示例值 |
|---|---|---|
| **MBTI** | 迈尔斯-布里格斯类型指标 | INTJ, ENFP, ISFJ |
| **依恋类型** | 依恋理论 (Bowlby, 1969) | 安全型, 焦虑型, 回避型, 恐惧-回避型 |
| **爱的语言** | 爱的五种语言 (Chapman, 1992) | 肯定言辞, 精心时刻, 接受礼物, 服务的行动, 身体接触 |
| **大五人格** | OCEAN 模型 | 高开放性, 低尽责性, 高神经质 |
| **冲突模式** | Gottman 四骑士 | 批评, 鄙视, 辩护, 冷战 |

---

## 四、文件输入支持

| 来源 | 格式 | 解析工具 | 备注 |
|---|---|---|---|
| 微信聊天记录 | TXT (WeChatMsg/留痕) | `chat_parser.py` | 自动提取时间戳、发送者、内容 |
| 微信聊天记录 | JSON (PyWxDump) | `chat_parser.py` | 自动提取时间戳、发送者、内容 |
| 短信 / iMessage | TXT | `chat_parser.py` | 支持通用正则匹配 |
| 邮件往来 | .eml / .mbox | `email_parser.py` | 提取正文，过滤引用，支持长文情感分析 |
| 聊天截图 | 图片 (PNG/JPG) | Claude 视觉能力 | 需模型自行提取文本和情绪 |
| 备忘录 / 日记 | Markdown / TXT | 直接读取 | 用于提取核心记忆和重大事件 |

---

## 五、生成内容规范

### 5.1 Part A — 关系档案 (Relationship Profile)

从文件中提取双方的互动模式，量化关系健康度，并建立记忆权重库。

**提取与计算维度：**

1. **RQI (Relationship Quality Index)**：关系质量指数，满分 10 分。
   - 沟通模式 (30%)
   - 情感亲密度 (25%)
   - 爱的语言契合度 (20%)
   - 冲突修复能力 (15%)
   - 共同成长轨迹 (10%)
2. **ACS (Attachment Compatibility Score)**：依恋兼容性得分，作为 RQI 的乘数（0.30 - 0.95）。
3. **LLMI (Love Language Mismatch Index)**：爱的语言错配指数。
4. **核心记忆库**：基于 `W = E × R × (1 + F)` 公式计算记忆激活权重，W > 0.6 的记忆将被标记为核心记忆。

**生成结果：** `relationship.md`

### 5.2 Part B — 人格画像 (Persona)

从文件和手动标签共同构建该伴侣的行为模式和沟通风格。

**分层结构（优先级从高到低）：**

- **Layer 0 — 硬覆盖层**：手动标签直接翻译，最高优先级（例如："TA 绝对不会主动道歉"）。
- **Layer 1 — 身份与心理学基线**：MBTI、依恋类型、大五人格的理论推演。
- **Layer 2 — 表达风格层**：用词习惯、句式长短、emoji 使用习惯（从聊天记录提取）。
- **Layer 3 — 情绪调节与决策层**：遇到压力时的反应（压抑/重评/失调），决策风格（分析型/直觉型）。
- **Layer 4 — 亲密行为层**：在私密空间 vs 公共空间的表现，对肢体接触的接受度。
- **Layer 5 — Correction 层**：对话纠正追加，滚动更新。

**生成结果：** `persona.md`

### 5.3 完整组合 SKILL.md

将 `relationship.md` + `persona.md` 合并，生成可直接运行的完整 Skill。

**运行逻辑：**

1. 接收到场景描述（如："TA 生气了"）。
2. **Persona 判断**：TA 在这个情境下的情绪状态和防御机制是什么？
3. **Relationship 执行**：结合 RQI 诊断和历史核心记忆，给出最适合这段关系的修复策略。
4. **个性化输出**：建议必须符合 TA 的爱的语言和沟通偏好。

---

## 六、核心功能模块

### 6.1 场景顾问 (Scenario Advisor)

支持 23 个生活场景的个性化建议生成：

- **情绪与冲突**：伴侣生气/冷战、需要安慰、真诚道歉、嫉妒与不安全感。
- **庆祝与送礼**：纪念日、生日、节日、庆祝伴侣成就。
- **体验与日常**：约会策划、旅行安排、日常升温、深化亲密感、支持个人成长。
- **现实与发展**：家务分配、财务讨论、同居磨合、数字边界、异地恋、见家长、社交圈、职业压力、健康照料、未来规划。

### 6.2 冲突解决器 (Conflict Resolver)

基于 Gottman 理论的冲突修复路径：

1. 识别表面问题 vs 核心需求。
2. 检测四骑士（批评、鄙视、辩护、冷战）。
3. 生成五步修复话术（破冰、共情、担责、提议、安抚）。

### 6.3 反思日志 (Reflection Log)

记录关系里程碑和冲突复盘，生成 RMM（关系动量模型）轨迹，判断关系处于上升期、稳定期还是下滑期。

---

## 七、进化机制

1. **追加文件进化**：用户上传新的聊天记录，系统自动提取增量信息，更新记忆库和 RQI 评分。
2. **对话纠正进化**：用户指出 "TA 不会这样说"，系统将规则写入 Persona 的 Layer 5 (Correction 层)，立即生效。
3. **版本管理**：每次更新自动存档，支持 `/rollback {slug} {version}` 回滚到任意历史版本。

---

## 八、项目结构

```text
partner-skill/
├── SKILL.md                    # 主入口
├── docs/
│   ├── PRD.md                  # 产品需求文档
│   └── partner_skill.pdf       # 技术论文
├── tools/
│   ├── profile_builder.py      # 基础画像构建
│   ├── relationship_analyzer.py# RQI/ACS 数学模型计算
│   ├── scenario_advisor.py     # 23 场景顾问
│   ├── gift_advisor.py         # 送礼推荐
│   ├── conflict_resolver.py    # 冲突解决器
│   ├── chat_parser.py          # 聊天记录解析
│   ├── email_parser.py         # 邮件解析
│   ├── skill_writer.py         # Skill 文件生成与更新
│   └── version_manager.py      # 版本控制
├── prompts/                    # 提示词模板
└── partners/                   # 生成的伴侣 Skill 目录 (gitignored)
```
