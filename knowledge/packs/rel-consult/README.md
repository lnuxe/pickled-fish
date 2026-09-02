# 關係諮詢系統

[中文](README.md) | [English](README.en.md)

這是一套給 AI agent 使用的關係諮詢 skills 組合包，以多個心理學模型為核心，用來產生可修正、可迭代的互動假設與建議。

## 快速使用

1. 先請你的 agent 閱讀 `CLAUDE.md`（這是主要操作規範）。
2. 開始描述你的關係情境，並提供目標（例如：想修復信任、想改善溝通）。
3. 如需持續追蹤，使用 `memory-templates/` 建立個體與關係檔案到 `memory/`。

## 專案簡介

本專案提供一套結構化的關係諮詢流程，重點在於：

- 不做診斷，只提供可驗證與可修正的假設
- 兼顧倫理邊界與安全溝通
- 透過多模型交叉解讀關係中的溝通、信任、壓力、需求與互動模式

## 核心文件

- `docs/consultation-protocol.md`：諮詢流程、溝通原則與倫理界線
- `docs/integration-guide.md`：模型整合方式、訊號路由與衝突處理
- `docs/model-bibliography.md`：模型來源與參考資料

## 技能模組

`skills/` 目錄提供可組合的分析模組，包含：

- 依附動力（Attachment Dynamics）
- 衝突模式（Conflict Patterns）
- 信任架構（Trust Architecture）
- 壓力評估（Stress Appraisal）
- 需求滿足（Need Satisfaction）
- 互動風格（Interaction Style）
- 歸因偏誤稽核（Attribution Bias Audit）
- 界線與請求（Boundaries and Requests）
- 不確定性下的決策支持（Decision Support Under Uncertainty）

## 記憶模板

- `memory-templates/subject-profile.md`
- `memory-templates/relationship-dyad.md`

可搭配 `memory/` 目錄，持續維護個體與關係動態的可追蹤紀錄。

## 重要提醒

- 本系統不是醫療、精神或法律診斷工具。
- 所有輸出都應保留暫時性與可修正性。
- 若出現嚴重痛苦、創傷或疑似虐待訊號，應建議尋求專業協助。

## 參考理論文獻（精簡）

完整文獻清單請見：`docs/model-bibliography.md`

- 依附理論（成人親密關係）
  - Hazan, C., & Shaver, P. (1987). Romantic love conceptualized as an attachment process. *Journal of Personality and Social Psychology, 52*(3), 511-524. https://doi.org/10.1037/0022-3514.52.3.511
- 衝突模式（Four Horsemen 脈絡）
  - Gottman, J. M. (1994). *Why Marriages Succeed or Fail*. Simon & Schuster.
- 信任架構（ABI）
  - Mayer, R. C., Davis, J. H., & Schoorman, F. D. (1995). An integrative model of organizational trust. *Academy of Management Review, 20*(3), 709-734. https://doi.org/10.5465/amr.1995.9508080335
- 壓力評估（Cognitive Appraisal）
  - Lazarus, R. S., & Folkman, S. (1984). *Stress, Appraisal, and Coping*. Springer.
- 需求滿足（Self-Determination Theory）
  - Deci, E. L., & Ryan, R. M. (2000). The "what" and "why" of goal pursuits: Human needs and the self-determination of behavior. *Psychological Inquiry, 11*(4), 227-268. https://doi.org/10.1207/S15327965PLI1104_01
- 互動風格（Interpersonal Circumplex）
  - Alden, L. E., Wiggins, J. S., & Pincus, A. L. (1990). Construction of circumplex scales for the Inventory of Interpersonal Problems. *Journal of Personality Assessment, 55*(3-4), 521-536. https://doi.org/10.1080/00223891.1990.9674088
- 動機校準（Regulatory Focus）
  - Higgins, E. T. (1997). Beyond pleasure and pain. *American Psychologist, 52*(12), 1280-1300. https://doi.org/10.1037/0003-066X.52.12.1280
- 歸因與偏誤（Attribution & Bias）
  - Ross, L. (1977). The intuitive psychologist and his shortcomings: Distortions in the attribution process. In L. Berkowitz (Ed.), *Advances in Experimental Social Psychology* (Vol. 10, pp. 173-220). Academic Press. https://doi.org/10.1016/S0065-2601(08)60357-3
  - Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science, 185*(4157), 1124-1131. https://doi.org/10.1126/science.185.4157.1124
- 不確定下的決策
  - Tversky, A., & Kahneman, D. (1979). Prospect theory: An analysis of decision under risk. *Econometrica, 47*(2), 263-292.
  - Gollwitzer, P. M. (1999). Implementation intentions: Strong effects of simple plans. *American Psychologist, 54*(7), 493-503. https://doi.org/10.1037/0003-066X.54.7.493
