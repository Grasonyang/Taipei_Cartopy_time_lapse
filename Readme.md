# 台北市交通事故縮時攝影動畫

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一個完整的資料分析專案，使用 Python 處理台北市 113 年（2024）交通事故資料，產生統計圖表、地圖視覺化以及縮時攝影動畫。

## 📋 專案概述

本專案分析台北市 113 年（2024）A1 及 A2 類交通事故資料，透過完整的 ETL 流程將原始資料轉換為可視化內容：

- **統計分析**：事故發生區域與時段分布
- **地圖視覺化**：台北市行政區邊界與事故點位圖
- **縮時動畫**：每日累積事故發生情況的時間序列動畫

## 🎯 主要功能

### 1. ETL 資料處理流程
- **Raw** → **Interim** → **Processed** 三階段處理
- 資料清洗、座標轉換、特徵工程
- 處理 22,367 筆事故記錄

### 2. 統計視覺化
- 各行政區事故發生統計
- 24 小時事故時段分布
- 清晰的圖表設計與中文字型支援

### 3. 地圖視覺化
- 台北市行政區邊界（粉紅色填充）
- A1/A2 事故點位（紅色/橙色標記）
- 正方形畫布設計（1:1 比例）

### 4. 縮時攝影動畫
- 366 天完整年度覆蓋
- 每日累積事故顯示
- MP4 格式輸出，支援影片播放

## 🏗️ 專案架構

```
Taipei_Cartopy_time_lapse/
├── data/                          # 資料目錄
│   ├── raw/                       # 原始資料
│   ├── interim/                   # 中間處理資料
│   └── processed/                 # 最終處理資料
├── outputs/                       # 輸出結果
│   ├── figures/                   # 統計圖表
│   └── videos/                    # 動畫影片
├── src/                           # 原始碼
│   ├── config.py                  # 設定檔案
│   ├── etl.py                     # 資料處理模組
│   ├── viz_stats.py               # 統計視覺化
│   ├── viz_raw_map.py             # 基礎地圖
│   ├── viz_map.py                 # 事故地圖
│   └── animate.py                 # 縮時動畫
├── main.py                        # 主執行腳本
├── requirements.txt               # 依賴套件
└── README.md                      # 專案說明
```

## 🚀 快速開始

### 環境需求

- Python 3.10+
- Ubuntu/Debian 系統（支援中文字型）
- ffmpeg（動畫生成需要）

### 安裝步驟

1. **複製專案**
```bash
git clone <repository-url>
cd Taipei_Cartopy_time_lapse
```

2. **建立虛擬環境**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

3. **安裝依賴套件**
```bash
pip install -r requirements.txt
```

4. **安裝系統依賴**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg
```

### 資料準備

將原始資料檔案放置於 `data/raw/` 目錄：
- `113年-臺北市A1及A2類交通事故明細.csv`
- `G97_A_CAVLGE_P.shp` 及其相關 shapefile 檔案

## 📊 使用說明

### 完整 ETL 流程
```bash
python main.py
```

### 個別功能執行

```bash
# 統計視覺化
python -m src.viz_stats

# 基礎地圖（僅台北市邊界）
python -m src.viz_raw_map

# 事故分布地圖
python -m src.viz_map

# 縮時攝影動畫
python -m src.animate
```

### Makefile 指令（開發中）

```bash
# 資料處理
make etl

# 生成圖表
make figs

# 生成動畫
make movie

# 完整流程
make all
```

## 📈 輸出結果

### 統計圖表
- `outputs/figures/district_distribution.png` - 各區事故統計
- `outputs/figures/hourly_distribution.png` - 時段分布統計

### 地圖視覺化
- `outputs/figures/taipei_raw_map.png` - 台北市邊界地圖
- `outputs/figures/taipei_accident_map.png` - 事故分布地圖

### 縮時動畫
- `outputs/videos/taipei_timelapse.mp4` - 年度事故縮時動畫

## 🛠️ 技術細節

### 資料處理
- **座標系統**：EPSG:3826 (TWD97 TM2) → EPSG:4326 (WGS84)
- **資料格式**：CSV → Parquet（高效能儲存）
- **事故分類**：A1（死亡事故）、A2（重傷事故）

### 視覺化規格
- **畫布尺寸**：14×14 英吋（4200×4200 像素）
- **解析度**：300 DPI
- **色彩方案**：
  - 台北市邊界：粉紅色填充（透明度 30%）
  - A1 事故：紅色圓點
  - A2 事故：橙色圓點
- **字型**：Noto Sans CJK TC（支援繁體中文）

### 動畫參數
- **幀率**：10 FPS
- **總幀數**：366 幀（涵蓋全年）
- **編碼器**：H.264 (MP4)
- **解析度**：2100×2100 像素

## 📋 專案章程

本專案遵循以下核心原則：

1. **語言規範**：所有程式碼、文件與溝通使用繁體中文
2. **依賴管理**：requirements.txt 在最終發行前不指定版本
3. **程式碼結構**：採用 try-catch、函式化與類別化設計

詳細章程請參考：`.specify/memory/constitution.md`

## 🤝 貢獻指南

1. Fork 此專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送至分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📝 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 📞 聯絡資訊

如有問題或建議，請透過以下方式聯絡：

- 建立 Issue
- 發送 Pull Request
- 專案維護者

---

**版本**: 1.0.0 | **最後更新**: 2025-11-09