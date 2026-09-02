> 🌐 [English](README.md) | **中文**

# 🧠 Hermes 依恋类型分析

一个 **Hermes Agent 技能**，基于 ECR-R（亲密关系体验量表修订版）框架，通过对话方式评估成人依恋类型。

## 功能

- **评估**：通过 16 题对话问卷评估你的依恋风格
- **分类**：归入 4 种 Bartholomew 类型：安全型、迷恋型、疏离-回避型、恐惧-回避型
- **推荐**：匹配你依恋类型的书籍
- **提供**：每种类型的成长策略

## 2×2 模型

```
                低回避                      高回避
低焦虑  →  安全型                         疏离-回避型
            (+ 自我, + 他人)               (+ 自我, - 他人)

高焦虑  →  迷恋型（焦虑型）                恐惧-回避型
            (- 自我, + 他人)               (- 自我, - 他人)
```

## 涵盖书籍

| 书籍 | 作者 | 侧重点 |
|------|------|--------|
| *Attached* | Levine & Heller | 3 类型模型，约会建议 |
| *The Power of Attachment* | Diane Poole Heller | 4 类型，躯体疗愈 |
| *Attachment in Psychotherapy* | David Wallin | 临床级，神经科学视角 |
| *Hold Me Tight* | Sue Johnson | 伴侣 EFT 疗法 |
| *Insecure in Love* | Becker-Phelps | 焦虑型自救 |
| *Avoidant* | Jeb Kinnison | 回避型手册 |
| *Polysecure* | Jessica Fern | 依恋 × 多元关系 |
| *Becoming Attached* | Robert Karen | 依恋理论史 |

## 使用方式

在 Hermes Agent 中加载技能后，说"分析我的依恋类型"即可开始 16 题测评。

## 安装

```bash
cp SKILL.md ~/.hermes/skills/attachment-style/
```

## 免责声明

本工具改编自学术量表（Fraley 等, 2000 的 ECR-R），属于自我筛查工具，**不构成临床诊断**。如有临床需求，请寻求持证心理咨询师帮助。

## 参考文献

- Bartholomew & Horowitz (1991). *JPSP, 61*(2), 226-244.
- Fraley, Waller & Brennan (2000). *JPSP, 78*, 350-365.
- Levine & Heller (2010). *Attached*. TarcherPerigee.
- Heller, D. P. (2019). *The Power of Attachment*. Sounds True.

## 许可证

MIT
