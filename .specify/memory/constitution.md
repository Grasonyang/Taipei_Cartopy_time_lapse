<!--
Sync Impact Report:
- Version change: 0.0.0 → 1.0.0
- Modified principles:
  - [PRINCIPLE_1_NAME] → 語言與註解
  - [PRINCIPLE_2_NAME] → 依賴管理
  - [PRINCIPLE_3_NAME] → 程式碼結構
- Removed sections:
  - PRINCIPLE_4_NAME
  - PRINCIPLE_5_NAME
  - SECTION_2_NAME
  - SECTION_3_NAME
- Templates requiring updates: None
- Follow-up TODOs: None
-->
# Taipei Cartopy Time Lapse 章程

## 核心原則

### 語言與註解
所有程式碼、文件和溝通一律使用繁體中文，並在程式碼中加入中文註解以利理解。

### 依賴管理
在 `requirement.txt` 中，在最終發行版之前，不應訂定具體版本號，以保持開發彈性。

### 程式碼結構
程式設計應採用 `try-catch` 區塊，並配合函式化與類別化。單一函式內的程式碼不應過於冗長，以提高可讀性與可維護性。

## 治理
本章程高於所有其他實踐。任何修訂都必須有文件記錄、審核批准及遷移計畫。所有提取請求（PR）和審查都必須驗證是否符合本章程。

**版本**: 1.0.0 | **批准日期**: 2025-11-09 | **最後修訂日期**: 2025-11-09
