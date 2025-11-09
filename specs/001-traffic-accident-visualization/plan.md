# 實作計畫：台北市113年A1/A2交通事故視覺化

**功能分支**：`001-traffic-accident-visualization`
**規格文件**：[spec.md](./spec.md)
**狀態**：規劃中

## 技術上下文

-   **語言**: Python 3.10+
-   **核心函式庫**:
    -   `pandas`: 用於資料處理與ETL。
    -   `matplotlib`: 用於靜態圖表與動畫基礎。
    -   `cartopy`: 用於地圖投影與底圖繪製。
    -   `requests`: (可選) 用於從API擷取資料。
-   **環境管理**: 將使用 `requirements.txt` 管理相依套件。
-   **動畫輸出**: 需要 `ffmpeg` 支援以輸出MP4檔案。
-   **專案結構**: 將遵循 `Architectrue.md` 中定義的結構，將邏輯分離到不同的模組 (`ingest`, `etl`, `viz_stats`, `viz_map`, `animate`)。

## 章程檢查

-   **語言與註解**: (符合) 所有程式碼將使用繁體中文註解。
-   **依賴管理**: (符合) `requirements.txt` 在初期將不鎖定版本。
-   **程式碼結構**: (符合) 程式碼將模組化，並在適當時機使用 `try-catch` 處理錯誤。

## 第 0 階段：大綱與研究

### 研究任務

-   **任務 1**: 確認 `matplotlib` 中支援繁體中文的最佳字型設定方法，以避免亂碼問題。
-   **任務 2**: 研究 `cartopy` 在 Ubuntu 24.04 上的建議安裝方式（`pip` vs `conda`），以及可能遇到的相依性問題。
-   **任務 3**: 探索 `matplotlib.animation.FuncAnimation` 的 `blit=True` 選項在效能上的優化效果，以及在不同後端（如 Agg, TkAgg）下的行為差異。

### 研究成果

將在 `research.md` 中記錄上述任務的發現與決策。

## 第 1 階段：設計與合約

### 資料模型

將在 `data-model.md` 中詳細定義 `Accident` 實體的欄位、資料類型及驗證規則。

### API 合約

此功能不涉及外部API的定義，因此 `contracts/` 目錄將保持空白。

### 快速入門

將在 `quickstart.md` 中提供設定開發環境、安裝相依套件及執行主要腳本的步驟。

### 代理程式上下文更新

將執行 `.specify/scripts/bash/update-agent-context.sh copilot` 以更新AI代理程式的上下文。

## 第 2 階段：實作

此階段將根據 `Architectrue.md` 中的程式碼骨架，逐步完成各個模組的開發。詳細任務將在 `/speckit.tasks` 中定義。

