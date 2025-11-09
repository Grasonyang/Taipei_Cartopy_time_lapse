# 開發任務：台北市113年A1/A2交通事故視覺化

本文件將 `spec.md` 中定義的使用者故事分解為具體的、可執行的開發任務。

## 第 1 階段：專案設定

-   [X] T001 根據 `Architectrue.md` 建立專案目錄結構 (`data/`, `src/`, `outputs/` 等)。
-   [X] T002 建立 `requirements.txt` 檔案，並填入核心相依套件：`pandas`, `matplotlib`, `cartopy`, `requests`。
-   [X] T003 建立 `src/config.py` 檔案，用於存放路徑、常數與欄位對應等設定。
-   [X] T004 在 `src/` 目錄下建立 `__init__.py` 檔案，使其成為一個可匯入的套件。

## 第 2 階段：[US1] 資料擷取與ETL

**目標**: 建立一個可重複執行的ETL管線，將原始資料轉換為乾淨的 Parquet 檔案。
**獨立測試**: 執行 `make etl` 後，應能在 `data/processed/` 目錄下看到 `taipei_113_clean.parquet` 檔案，且其 schema 符合 `data-model.md` 的定義。

-   [X] T005 [US1] 在 `src/ingest.py` 中，實作 `fetch_all` 函式，用於從 API 或 CSV 讀取原始資料，並將其儲存到 `data/raw/`。
-   [X] T006 [US1] 在 `src/etl.py` 中，實作 `clean` 函式，用於資料清理、欄位標準化及派生欄位的建立。
-   [X] T007 [US1] 在 `src/etl.py` 中，加入處理無效經緯度與日期時間的錯誤處理邏輯（例如，記錄並移除）。
-   [X] T008 [US1] 建立一個主腳本或 `Makefile` 中的 `etl` 目標，串連 `ingest` 與 `clean` 函式，並將最終的 DataFrame 儲存為 `data/processed/taipei_113_clean.parquet`。

## 第 3 階段：[US2] 靜態統計圖表

**目標**: 產生依行政區與時間分佈的靜態圖表。
**獨立測試**: 執行 `make figs` 後，應能在 `outputs/figures/` 目錄下看到至少兩張 PNG 圖檔。

-   [X] T009 [P] [US2] 在 `src/viz_stats.py` 中，實作 `plot_by_district` 函式，用於產生依行政區劃分的堆疊長條圖。
-   [X] T010 [P] [US2] 在 `src/viz_stats.py` 中，實作一個新函式 `plot_by_time`，用於產生依時間（小時或日/夜）分佈的折線圖或柱狀圖。
-   [X] T011 [US2] 確保所有圖表都能正確設定並顯示繁體中文字型。
-   [ ] T012 [US2] 建立 `Makefile` 中的 `figs` 目標，用於執行 `viz_stats.py` 中的所有繪圖函式。

## 第 4 階段：[US3] 地圖散點圖

**目標**: 在 Cartopy 地圖上繪製事故散點圖。
**獨立測試**: 執行 `make map` (或整合進 `figs`) 後，應能在 `outputs/figures/` 目錄下看到地圖散點圖 PNG。

-   [X] T013 [US3] 在 `src/viz_map.py` 中，實作 `plot_map` 函式。
-   [X] T014 [US3] 在 `plot_map` 中，設定 Cartopy 的地圖投影 (`ccrs.PlateCarree()`) 與範圍 (`set_extent`)。
-   [X] T015 [US3] 在 `plot_map` 中，加入海岸線、陸地等底圖特徵。
-   [X] T016 [US3] 在 `plot_map` 中，根據 `light_bin` 欄位，使用不同顏色或標記繪製白天與夜晚的事故散點。

## 第 5 階段：[US4] 縮時攝影動畫

**目標**: 建立一個依日期推進的 MP4 動畫。
**獨立測試**: 執行 `make movie` 後，應能在 `outputs/videos/` 目錄下看到 `tpe113_timelapse.mp4` 影片檔。

-   [X] T017 [US4] 在 `src/animate.py` 中，實作 `timelapse` 函式。
-   [X] T018 [US4] 在 `timelapse` 中，設定 `matplotlib.animation.FuncAnimation`，包含 `init` 和 `update` 函式。
-   [X] T019 [US4] 在 `update` 函式中，實現每一幀的資料篩選與散點更新邏輯。
-   [X] T020 [US4] 在 `timelapse` 中，加入儲存動畫為 MP4 的功能，並在 `ffmpeg` 未安裝時提供清晰的錯誤提示。
-   [ ] T021 [US4] 建立 `Makefile` 中的 `movie` 目標，用於執行 `animate.py`。

## 第 6 階段：潤飾與整合

-   [ ] T022 建立 `Makefile` 中的 `all` 目標，用於依序執行 `etl`, `figs`, `movie`。
-   [ ] T023 撰寫 `README.md`，說明專案目標、如何設定環境及執行。
-   [ ] T024 最終審查所有程式碼，確保註解清晰、風格一致。

## 相依性

-   [US2] 相依於 [US1]
-   [US3] 相依於 [US1]
-   [US4] 相依於 [US1]

## 平行執行範例

-   在 [US2] 中，`T009` 和 `T010` 可以平行開發，因為它們處理不同的圖表，但都依賴相同的輸入資料。

## 實作策略

將遵循 MVP (Minimum Viable Product) 優先的原則，首先完成 [US1] 以確保資料管線的暢通。接著，依序完成 [US2]、[US3] 和 [US4]，逐步交付視覺化成果。
