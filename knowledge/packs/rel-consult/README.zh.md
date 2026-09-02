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
