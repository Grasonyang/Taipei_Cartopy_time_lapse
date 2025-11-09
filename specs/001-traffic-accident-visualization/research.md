# 研究日誌：台北市交通事故視覺化

## 任務 1：Matplotlib 中文支援

-   **決策**: 使用 `matplotlib.font_manager` 來動態載入系統中支援中文的字型（如 `Noto Sans CJK TC` 或 `Microsoft JhengHei`），並在繪圖時透過 `plt.rcParams['font.sans-serif']` 進行全域設定。
-   **理由**: 這種方法避免了修改 `matplotlib` 的設定檔，具有較好的可攜性，且易於在程式碼中管理。
-   **替代方案**:
    -   手動修改 `matplotlibrc` 檔案：設定繁瑣，且在不同環境中不易部署。
    -   在每個繪圖函式中單獨指定 `fontproperties`：程式碼重複性高，不易維護。

## 任務 2：Cartopy 安裝

-   **決策**: 建議使用者優先使用 `conda` (`conda install -c conda-forge cartopy`) 進行安裝。若使用者堅持使用 `pip`，則需在 `quickstart.md` 中明確指出，必須先透過系統套件管理員（如 `apt`) 安裝 `libproj-dev`, `geos-dev` 等底層相依函式庫。
-   **理由**: `conda` 能更好地處理 `cartopy` 複雜的地理空間函式庫相依性（如 PROJ, GEOS），可大幅降低安裝失敗的機率。
-   **替代方案**:
    -   僅提供 `pip` 安裝說明：對新手使用者不友善，容易因環境問題導致安裝失敗。
    -   使用 Docker 容器：雖然能保證環境一致性，但增加了專案的複雜度，對於一個以腳本為主的視覺化專案來說，有點小題大作。

## 任務 3：FuncAnimation 效能

-   **決策**: 在 `FuncAnimation` 中，將 `blit=True` 作為預設選項。
-   **理由**: `blit=True` 會告訴 `matplotlib` 只重繪畫面中發生變化的部分，而非整個畫布。對於縮時攝影這種只有散點位置和標題變動的場景，能顯著提升動畫的流暢度並降低CPU使用率。
-   **替代方案**:
    -   `blit=False`：在每一幀都重繪整個圖表，對於複雜的背景（如地圖）來說，效能開銷極大，容易造成動畫卡頓。
