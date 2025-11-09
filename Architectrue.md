# 無標題

# 113 台北市 A1/A2 交通事故視覺化 — 系統架構說明 (Architecture)

> 目標：以 Pandas 進行資料擷取與清理，並使用 Matplotlib（+ Cartopy 做底圖）完成
> 
> 1. 各行政區事故分佈、2) 日/夜分層趨勢、3) 依日期推進的「縮時攝影」式地圖動畫，並以不同車種的 ICON 呈現。

---

## 1) 需求與產出 (Requirements & Deliverables)

- **資料來源**：台北市 113 年 A1/A2 交通事故明細（有經緯度、日期時間、行政區、車種、光線、天候等欄位）。
- **核心技術**：`pandas`、`matplotlib`、`matplotlib.animation.FuncAnimation`、`cartopy`（地圖投影 + 底圖特徵）。
- **必備成果**
    1. 行政區事故**統計圖**（柱狀/條形、可分 A1/A2）。
    2. **時間分布圖**（按日或小時，日/夜分層）。
    3. **地圖散點圖**（全市，車種以不同 marker 或自訂 ICON）。
    4. **縮時動畫**（日期推進，白天 vs 夜晚顏色區分）。
- **加分項**
    - 事故嚴重度（A1/A2）以大小或透明度違例呈現
    - 匯出：PNG（圖）、MP4（動畫）、CSV（中間結果）

---

## 2) 系統總覽 (System Overview)

```mermaid
flowchart LR
    A[API/CSV Source] -->|requests/pandas| B[Ingestion 模組]
    B --> C[Raw Cache (.parquet)]
    C --> D[Clean/ETL 模組<br/>- 欄位正規化<br/>- 時間/日夜標記<br/>- 車種 mapping]
    D --> E[(DataFrame<br/>整潔資料)]
    E --> F1[統計圖表 Matplotlib]
    E --> F2[地圖層 Cartopy+Matplotlib<br/>- 散點<br/>- 車種 ICON<br/>- 日/夜分色]
    E --> F3[縮時動畫 FuncAnimation]
    F1 --> G1[PNG 輸出]
    F2 --> G2[PNG 輸出]
    F3 --> G3[MP4/GIF 輸出]

```

---

## 3) 專案結構 (Repo Layout)

```
taipei-accidents-113/
├─ data/
│  ├─ raw/                 # 原始回應快取（CSV/JSON）
│  ├─ interim/             # 中間處理（parquet）
│  └─ processed/           # 清理後輸出
├─ icons/                  # 車種小圖示（PNG/SVG）
├─ notebooks/              # 探索用 Jupyter（可選）
├─ src/
│  ├─ config.py            # 參數、常數、路徑
│  ├─ ingest.py            # 抓資料 + 分頁 + 快取
│  ├─ etl.py               # 清理、轉型、派生欄位
│  ├─ viz_stats.py         # 統計圖（行政區、時間）
│  ├─ viz_map.py           # 地圖散點與車種 ICON
│  └─ animate.py           # 縮時動畫（FuncAnimation）
├─ outputs/
│  ├─ figures/             # 圖片
│  └─ videos/              # 動畫
├─ requirements.txt / environment.yml
└─ README.md

```

---

## 4) 環境與相依 (Environment & Dependencies)

- **Python 版本**：3.10+
- **套件**
    - `pandas`（資料處理）
    - `matplotlib`（靜態圖與動畫）
    - `cartopy`（地圖投影/底圖；Conda 安裝較穩）
    - `requests`（若經由 API 拉資料）
    - `pyproj`, `shapely`（Cartopy 可能需要）
    - `ffmpeg`（輸出 MP4 動畫）

> 安裝建議（conda-forge）
> 
> 
> `conda create -n tpe113 python=3.11 pandas matplotlib cartopy requests -c conda-forge`
> 
> `sudo apt-get install ffmpeg`（或以其他方式安裝 ffmpeg）
> 

---

## 5) 資料模型與欄位正規化 (Data Model & Normalization)

**必備欄位（示例）**：

- `acc_date`（事故日期、字串→`datetime.date`）
- `acc_time`（事故時間、字串→`datetime.time`）
- `district`（行政區 → 標準化字典）
- `case_type`（A1/A2）
- `light`（光線：白天、夜晚、昏暗等 → 映射為 `day`/`night` 二分）
- `weather`（天候 → 可保留原值或彙整）
- `vehicle_type`（車種 → 映射到 ICON 類別）
- `longitude`, `latitude`（經緯度 → `float`）
- `acc_dt`（**派生**：`datetime` = `acc_date + acc_time`，時區設為 **Asia/Taipei**）
- `hour`（**派生**：`acc_dt.hour`）
- `is_day`（**派生**：根據 `light` 或以時段規則推論）

**欄位映射建議**：

- `light`: {白天→`day`, 夜間→`night`, 昏暗/隧道→可依規則分配}
- `vehicle_type`: 做一個 mapping 到 5–8 類（小客車、機車、卡車、公車、腳踏車、行人…），方便 ICON 與色系管理。
- `district`: 去除空白/異體字，確保群組鍵一致。

---

## 6) ETL 管線 (ETL Pipeline)

1. **擷取 (Ingest)**
    - 走 API：支援 `limit`/`offset` 分頁，抓到完整年度，序列化到 `data/raw/`。
    - 或直接載 CSV：放入 `data/raw/`。
2. **清理 (Clean)**
    - 去重、去除無效經緯度（`NaN` 或落在台北市外的點）。
    - 標準化行政區、光線、車種。
    - 生成 `acc_dt`、`hour`、`is_day` 等派生欄。
3. **輸出 (Persist)**
    - 存為 `parquet`（高效 I/O）到 `data/interim/`。
    - 最終整潔版 `data/processed/taipei_113_clean.parquet`。

---

## 7) 視覺化規劃 (Visualization Plan)

### 7.1 行政區事故分佈（靜態圖）

- **圖型**：水平條形圖（行政區在 y 軸、事故數在 x 軸），可用 `stacked` 方式區分 `A1/A2`。
- **要點**：排序、標籤顯示、色彩一致性、字型支援（中文）。

### 7.2 時間分佈（日/夜分層）

- **圖型**：折線圖或雙柱圖（x 軸為日期或小時；不同顏色代表 `day/night`）。
- **要點**：平滑化（rolling mean 可選）、標註節假日（可選）。

### 7.3 地圖散點圖（全市）

- **投影**：`ccrs.PlateCarree()`；`ax.set_extent([119.5, 122.0, 23.0, 25.5])`（視情況調整到大台北）。
- **底圖**：`ax.coastlines('10m')` + `cfeature.LAND/OCEAN`；（如需更細行政區邊界，建議額外載 shapefile，但純 Matplotlib/Cartopy 亦可不加）。
- **繪點**：`ax.scatter(lon, lat, transform=ccrs.PlateCarree(), s=..., marker=..., alpha=...)`
- **車種 ICON**：使用 `AnnotationBbox(OffsetImage(img), (lon,lat), ...)` 疊上小 PNG（僅對代表性樣本或彙整點，以免太擁擠）。

### 7.4 縮時動畫（FuncAnimation）

- **單位時間步**：以「日」為一幀（也可用「小時」視資料密度）。
- **分層**：白天 vs 夜晚使用不同顏色或透明度。
- **流程**：
    1. 預先 `groupby(date)` 或 `resample('D')`。
    2. `init_func` 建立地圖底圖、座標系。
    3. `update(frame_date)`：清除上次散點 → 繪製當天資料（分 `day/night`）。
    4. 加上 `title` 顯示日期。
- **輸出**：`ani.save('outputs/videos/tpe113_timelapse.mp4', fps=12, dpi=150)`（需 ffmpeg）。

---

## 8) 設計細節 (Design Details)

- **色彩/樣式**
    - A1（死亡）用較醒目顏色（例如深色或高飽和），A2（受傷）用較淡色或透明度略高。
    - day/night：例如 day 用亮色、night 用深色。
- **ICON 配置**
    - `icons/` 放置小 PNG，縮時動畫僅在「代表樣本」或「聚合點」使用，避免喧賓奪主與效能負擔。
- **標註與說明**
    - 每張圖加上 `title`、`xlabel`/`ylabel`、`legend`，必要時加上 `caption` 描述資料範圍與限制。
- **字型**
    - Matplotlib 預設不一定支援中文，請設定支援中文字型（如 Noto Sans CJK），避免亂碼。

---

## 9) 關鍵程式骨架 (Code Skeletons)

### 9.1 Ingest（API 分頁）

```python
# src/ingest.py
import requests, pandas as pd, time
from pathlib import Path
from .config import RAW_DIR, API_URL

def fetch_all(limit=1000, pause=0.2) -> pd.DataFrame:
    offset, all_rows = 0, []
    while True:
        r = requests.get(API_URL, params={"limit": limit, "offset": offset}, timeout=30)
        r.raise_for_status()
        payload = r.json()["result"]
        rows = payload.get("results", [])
        if not rows: break
        all_rows.extend(rows)
        offset += limit
        time.sleep(pause)
    df = pd.DataFrame(all_rows)
    Path(RAW_DIR).mkdir(parents=True, exist_ok=True)
    df.to_csv(f"{RAW_DIR}/tpe113_raw.csv", index=False)
    return df

```

### 9.2 ETL（清理與派生欄位）

```python
# src/etl.py
import pandas as pd
from zoneinfo import ZoneInfo

LIGHT_MAP = {"白天":"day","日間":"day","夜間":"night","夜晚":"night","昏暗":"night"}

def clean(df: pd.DataFrame) -> pd.DataFrame:
    # 標準化欄位名稱（依實際欄位調整）
    df = df.rename(columns={
        "發生日期":"acc_date","發生時間":"acc_time",
        "行政區":"district","光線":"light","天候":"weather",
        "車種":"vehicle_type","經度":"longitude","緯度":"latitude","事故類別":"case_type"
    })
    # 時間
    tpe = ZoneInfo("Asia/Taipei")
    dt = pd.to_datetime(df["acc_date"] + " " + df["acc_time"], errors="coerce")
    df["acc_dt"] = dt.dt.tz_localize(tpe, nonexistent="shift_forward", ambiguous="NaT")
    df["date"] = df["acc_dt"].dt.date
    df["hour"] = df["acc_dt"].dt.hour
    # 光線
    df["light_bin"] = df["light"].map(LIGHT_MAP).fillna("unknown")
    # 經緯度
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["latitude"]  = pd.to_numeric(df["latitude"], errors="coerce")
    df = df.dropna(subset=["longitude","latitude"])
    # 行政區/車種 文字修整
    df["district"] = df["district"].str.strip()
    df["vehicle_type"] = df["vehicle_type"].str.strip()
    return df.drop_duplicates()

```

### 9.3 行政區分佈（統計圖）

```python
# src/viz_stats.py
import matplotlib.pyplot as plt

def plot_by_district(df, out_path):
    agg = (df.groupby(["district","case_type"])
             .size().unstack(fill_value=0)
             .sort_values(by=df["district"].unique(), ascending=False))
    ax = agg.plot(kind="barh", stacked=True, figsize=(8,10))
    ax.set_title("113 台北市 A1/A2 事故數 — 依行政區")
    ax.set_xlabel("事故數")
    ax.set_ylabel("行政區")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()

```

### 9.4 地圖（Cartopy + Matplotlib）

```python
# src/viz_map.py
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_map(df, out_path):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
    # 台北—可微調
    ax.set_extent([121.3, 121.7, 24.9, 25.2], crs=ccrs.PlateCarree())
    ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.LAND, alpha=0.2)
    ax.add_feature(cfeature.OCEAN, alpha=0.1)

    day = df[df["light_bin"]=="day"]
    night = df[df["light_bin"]=="night"]

    ax.scatter(day["longitude"], day["latitude"], s=8, alpha=0.6,
               transform=ccrs.PlateCarree(), label="Day")
    ax.scatter(night["longitude"], night["latitude"], s=8, alpha=0.6,
               transform=ccrs.PlateCarree(), label="Night", marker="x")

    ax.set_title("113 台北市 A1/A2 事故點（白天 vs 夜間）")
    ax.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=220)
    plt.close()

```

### 9.5 縮時動畫（FuncAnimation）

```python
# src/animate.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def timelapse(df, out_path):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
    ax.set_extent([121.3, 121.7, 24.9, 25.2], crs=ccrs.PlateCarree())
    ax.coastlines('10m'); ax.add_feature(cfeature.LAND, alpha=0.2)

    dates = sorted(df["date"].dropna().unique().tolist())
    scat_day = ax.scatter([], [], s=8, transform=ccrs.PlateCarree(), label="Day")
    scat_night = ax.scatter([], [], s=8, transform=ccrs.PlateCarree(), label="Night", marker="x")
    title = ax.set_title("")

    def init():
        scat_day.set_offsets([]); scat_night.set_offsets([]); title.set_text("")
        return scat_day, scat_night, title

    def update(i):
        d = dates[i]
        sub = df[df["date"]==d]
        day = sub[sub["light_bin"]=="day"][["longitude","latitude"]].to_numpy()
        night = sub[sub["light_bin"]=="night"][["longitude","latitude"]].to_numpy()
        scat_day.set_offsets(day); scat_night.set_offsets(night)
        title.set_text(f"113 台北市事故 — {d}")
        return scat_day, scat_night, title

    ani = animation.FuncAnimation(fig, update, frames=len(dates),
                                  init_func=init, interval=120, blit=True)
    ani.save(out_path, dpi=160, fps=12)
    plt.close()

```

> 車種 ICON：可在 update() 中以 AnnotationBbox 對「樣本點」或「聚合中心」覆蓋小圖示（避免幀內放太多 ICON 造成效能下降）。
> 

---

## 10) 效能與體驗 (Performance & UX)

- **效能**
    - 預先把資料壓成 `parquet`，圖表前先做 `groupby`/`resample` 減少每幀計算。
    - 動畫每幀只更新需要改變的 Artist（如 `set_offsets`），避免重繪整個底圖。
- **互動體驗（選配）**
    - 動畫上疊加當日統計（右上角小面板：當日 A1/A2 計數）。
    - 重要節日或氣候事件以 `ax.text` 標註。

---

## 11) 驗證與測試 (Validation & Testing)

[https://www.notion.so](https://www.notion.so)

[https://www.notion.so](https://www.notion.so)

- **資料品質**
    - 隨機抽樣地理點是否落在台北市合理範圍。
    - 同日同地點多筆重複的處理策略（保留/合併）。
- **圖表檢查**
    - 中文字型、圖例可讀性、標籤完整性。
    - 輸出尺寸與解析（投影片/論文用 200–300 DPI）。

---

## 12) 自動化與重現性 (Automation & Reproducibility)

- 建議提供 **CLI**：
    - `python -m src.ingest` 下載資料
    - `python -m src.etl`
    - `python -m src.viz_stats`
    - `python -m src.viz_map`
    - `python -m src.animate`
- 或使用 `Makefile`：
    
    ```makefile
    ingest:
    	python -m src.ingest
    etl:
    	python -m src.etl
    figs:
    	python -m src.viz_stats && python -m src.viz_map
    movie:
    	python -m src.animate
    all: ingest etl figs movie
    
    ```
    

---

## 13) 風險與替代方案 (Risks & Alternatives)

- **Cartopy 安裝困難**：可退而求其次，以**純 Matplotlib** 在空白座標系上畫點，或載入一張台北市底圖（圖片）作為背景（需注意授權）。
- **ICON 太多造成混亂**：採用聚合（如先 group 到 500m 方格），只在聚合中心放 ICON。
- **資料欄位與命名差異**：以設定檔（`config.py`）集中欄位映射，便於調整。

---

## 14) 里程碑 (Milestones)

1. **D1–D2**：Ingest + ETL（完整清理輸出 parquet）
2. **D3**：行政區/時間統計圖完成
3. **D4**：地圖散點（day/night）完成
4. **D5**：縮時動畫（無 ICON 版）完成
5. **D6**：車種 ICON 疊加與微調（採樣/聚合）
6. **D7**：文件與輸出打包（PNG/MP4 + README）

---

## 15) 是否符合題目要求？

**是。**

整體流程以 **Pandas** 進行資料處理，**Matplotlib** 負責圖表與動畫；地圖底圖由 **Cartopy** 協助，但最終呈現仍透過 Matplotlib 完成，完全符合「Applying Pandas and Matplotlib to visualize the data set of 113 Taipei Traffic A1 & A2 accident report」的要求。