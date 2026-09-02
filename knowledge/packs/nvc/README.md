<div align="center">

<img src="./cover.png" alt="非暴力沟通 · Nonviolent Communication" width="540">

# ayi-nonviolent-communication

**马歇尔·卢森堡《非暴力沟通》(NVC) 的可执行 AI Skill**

一个为 Cursor / Claude Code / Codex 设计的工具箱，把任何一句话翻译成
「观察—感受—需要—请求」，让沟通回到善意与连结。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

</div>

---

## 这是什么

不是读书笔记，是一个**可被 AI 反复调用的工具箱**。它把《非暴力沟通》一整本书里的
框架、原则、技法、反模式、作者语气，提炼成结构化、可执行的指导。

核心引擎只有一句话：**把任何信息（自己的或他人的）翻译成「观察—感受—需要—请求」四要素，重新与普世「需要」连结。**

覆盖五类用法：

| 用法 | 场景 |
|---|---|
| 🧭 决策 / 自我教练 | 理清自己的需要再行动："我该不该做这件事""理一理我现在的情绪" |
| ✏️ 话术改写 | 把指责/评判式表达改成 NVC 表达："改一下这条消息别那么冲" |
| 👂 同理倾听 | 听见对方话语背后的感受和需要："他这么说我该怎么回应" |
| 🕊️ 冲突调解 / 复盘 | 区分需要 vs 策略，设计满足各方的方案："化解一段冲突""复盘一次难谈话" |
| 🎙️ 以马歇尔语气产出内容 | 用《非暴力沟通》的声音写表达 |

## 它由什么组成

路由型架构 —— 一个入口 + 5 个按需加载的引用文件：

```
SKILL.md                              入口：四要素引擎 + 意图路由表 + 核心区分速查
references/
├── engine-four-components.md         四要素引擎（观察/感受/需要/请求）+ 四组核心区分
├── empathy-and-self.md               同理倾听 · 自我同理 · 爱自己 · 情绪三阶段
├── anger-conflict-force.md           愤怒的转化 · 冲突调解五步 · 保护性 vs 惩罚性强制力
├── anti-patterns.md                  异化沟通（豺狗语言）反模式清单
└── voice-and-gratitude.md            马歇尔的作者语气 · 表达与接受感激
```

保留原书的精确命名：观察 vs 评论 / 感受 vs 想法 / 需要 vs 策略 / 请求 vs 要求 /
刺激 vs 原因 / 保护性 vs 惩罚性强制力 / 哀悼(mourning) / 非暴力呐喊 / 长颈鹿 vs 豺狗。

## 安装

把整个目录放进你的 skills 目录，文件夹名保持为 `ayi-nonviolent-communication`：

**Cursor**

```bash
git clone https://github.com/ayi-ai/ayi-nonviolent-communication.git \
  ~/.cursor/skills/ayi-nonviolent-communication
```

**Claude Code**

```bash
git clone https://github.com/ayi-ai/ayi-nonviolent-communication.git \
  ~/.claude/skills/ayi-nonviolent-communication
```

之后正常对话即可被自动召回，或手动把 `SKILL.md` 喂给 Codex 等工具。

## 怎么用

装好后直接说你的真实场景，它会自动路由到对应的引用文件，例如：

- "帮我想想这话该怎么说 / 这条消息改一下别那么冲"
- "他说『你从来不管这个家』，我该怎么回应？"
- "我好生气 / 好委屈 / 好内疚，怎么办？"
- "帮我复盘一次很难的谈话 / 调解一下这场争吵"
- "帮我表达一次真诚的感谢 / 给同事一个不带评判的反馈"

## 致谢与边界

- 方法论来自马歇尔·卢森堡《非暴力沟通（修订版）》。本仓库是对其方法的**结构化提炼与工具化**，所有引述均忠于原著，不编造框架、数字或案例。
- 想深入，请支持购买正版原书。

## License

[MIT](./LICENSE) © 2026 AYi (@AYi_AInotes)
