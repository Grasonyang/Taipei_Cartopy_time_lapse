# 快速入門指南

本指南將引導您設定開發環境，並執行此專案的主要功能。

## 1. 環境設定

### 使用 Conda (建議)

我們強烈建議使用 Conda 來管理環境，因為它可以輕鬆處理 `cartopy` 的複雜相依性。

1.  **建立並啟用 Conda 環境**:
    ```bash
    conda create -n tpe-accidents python=3.11 -c conda-forge
    conda activate tpe-accidents
    ```

2.  **安裝相依套件**:
    ```bash
    conda install -c conda-forge --file requirements.txt
    ```

### 使用 Pip

如果您希望使用 `pip`，您必須先手動安裝 `cartopy` 所需的系統函式庫。

1.  **安裝系統相依套件 (以 Ubuntu 為例)**:
    ```bash
    sudo apt-get update
    sudo apt-get install -y libproj-dev proj-data proj-bin
    sudo apt-get install -y libgeos-dev
    ```

2.  **建立並啟用虛擬環境**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **安裝 Python 相依套件**:
    ```bash
    pip install -r requirements.txt
    ```

## 2. 安裝 FFmpeg

為了能夠將動畫儲存為 MP4 檔案，您需要安裝 `ffmpeg`。

**Ubuntu**:
```bash
sudo apt-get install ffmpeg
```

**macOS (使用 Homebrew)**:
```bash
brew install ffmpeg
```

## 3. 執行專案

1.  **下載資料**:
    (此步驟取決於您是從API還是CSV檔案取得資料。請將原始資料檔案，例如 `taipei_113_raw.csv`，放置於 `data/raw/` 目錄下。)

2.  **執行 ETL 與視覺化**:
    專案提供了一個 `Makefile` 來簡化執行流程。

    -   **執行所有步驟 (ETL -> 靜態圖表 -> 動畫)**:
        ```bash
        make all
        ```

    -   **分步執行**:
        ```bash
        make etl      # 執行資料清理與轉換
        make figs     # 產生靜態圖表
        make movie    # 產生縮時攝影動畫
        ```

3.  **查看產出**:
    -   靜態圖表將位於 `outputs/figures/` 目錄。
    -   縮時攝影動畫將位於 `outputs/videos/` 目錄。
