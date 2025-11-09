# -*- coding: utf-8 -*-
"""
Module for generating map-based visualizations.
"""
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from src.config import PROCESSED_DATA_FILE, FIGURES_DIR

# --- 中文字型設定 ---
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC', 'Microsoft JhengHei', 'Heiti TC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def plot_map(df: pd.DataFrame):
    """
    繪製台北市事故分佈的散點圖。
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # 設定地圖範圍為台北市
    ax.set_extent([121.4, 121.7, 24.9, 25.2], crs=ccrs.PlateCarree())

    # 加入地圖特徵
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

    # 繪製網格線
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

    # 區分白天與夜晚的資料
    day_df = df[df['light_bin'] == 'day']
    night_df = df[df['light_bin'] == 'night']

    # 繪製散點
    ax.scatter(day_df['longitude'], day_df['latitude'],
               s=5, alpha=0.5, transform=ccrs.PlateCarree(),
               label='白天', color='orange')
    
    ax.scatter(night_df['longitude'], night_df['latitude'],
               s=5, alpha=0.5, transform=ccrs.PlateCarree(),
               label='夜晚', color='blue')

    ax.set_title("113年 台北市 A1/A2 交通事故分佈 (白天 vs 夜晚)", fontsize=16)
    ax.legend()

    plt.tight_layout()
    output_path = FIGURES_DIR / "map_distribution.png"
    plt.savefig(output_path, dpi=220)
    plt.close()
    print(f"地圖已儲存至: {output_path}")

def main():
    """
    主函式，用於載入資料並執行繪圖。
    """
    if not PROCESSED_DATA_FILE.exists():
        print(f"錯誤：找不到處理後的資料檔案於 {PROCESSED_DATA_FILE}")
        return
        
    df = pd.read_parquet(PROCESSED_DATA_FILE)
    
    print("開始繪製地圖散點圖...")
    plot_map(df)
    print("地圖散點圖繪製完成。")

if __name__ == "__main__":
    main()
