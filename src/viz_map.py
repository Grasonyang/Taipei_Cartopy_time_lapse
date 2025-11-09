# -*- coding: utf-8 -*-
"""
在基礎台北市地圖上繪製交通事故分布
基於 viz_raw_map.py 的基礎地圖,加入事故點位資料
"""

import sys
from pathlib import Path

# 確保可以找到 src 模組
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib.font_manager import FontProperties
from src.config import PROCESSED_DATA_DIR, FIGURES_DIR

# 配置中文字型
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_prop = FontProperties(fname=font_path)


def load_taipei_boundary():
    """
    載入台北市行政區邊界 Shapefile 並轉換為 WGS84
    (與 viz_raw_map.py 共用的函數)
    
    Returns:
        GeoDataFrame: 台北市邊界資料 (WGS84 座標系統)
    """
    shapefile_path = 'data/taipei/G97_A_CAVLGE_P.shp'
    
    try:
        gdf = gpd.read_file(shapefile_path)
        gdf_wgs84 = gdf.to_crs(epsg=4326)
        return gdf_wgs84
    except Exception as e:
        print(f"✗ 讀取 Shapefile 失敗: {e}")
        return None


def load_accident_data():
    """
    載入處理過的交通事故資料
    
    Returns:
        DataFrame: 包含事故經緯度的資料
    """
    parquet_file = PROCESSED_DATA_DIR / 'taipei_113_clean.parquet'
    
    try:
        df = pd.read_parquet(parquet_file)
        print(f"✓ 成功讀取 {len(df)} 筆事故資料")
        return df
    except Exception as e:
        print(f"✗ 讀取事故資料失敗: {e}")
        return None


def create_accident_map():
    """
    創建台北市交通事故分布地圖
    - 基於 viz_raw_map.py 的粉紅色底圖
    - 加入 A1/A2 事故點位
    - 正方形畫布 (14x14)
    """
    print("\n" + "="*60)
    print("創建台北市交通事故分布地圖")
    print("="*60 + "\n")
    
    # 載入資料
    gdf_boundary = load_taipei_boundary()
    df_accidents = load_accident_data()
    
    if gdf_boundary is None or df_accidents is None:
        print("✗ 無法創建地圖")
        return
    
    # 計算地圖範圍,確保 1:1 正方形
    bounds = gdf_boundary.total_bounds
    lon_range = bounds[2] - bounds[0]
    lat_range = bounds[3] - bounds[1]
    
    lon_center = (bounds[0] + bounds[2]) / 2
    lat_center = (bounds[1] + bounds[3]) / 2
    
    max_range = max(lon_range, lat_range)
    margin = max_range * 0.05
    square_size = max_range + margin * 2
    
    # 創建正方形畫布 (與 viz_raw_map.py 一致)
    fig = plt.figure(figsize=(14, 14))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    
    # 設定 1:1 aspect ratio
    ax.set_aspect('equal')
    
    print("繪製地圖...")
    
    # 1. 繪製基礎台北市邊界 (與 viz_raw_map.py 相同設定)
    print("  - 繪製台北市邊界 (粉紅色底圖)")
    gdf_boundary.plot(
        ax=ax,
        facecolor='pink',
        edgecolor='gray',  # 淺灰色邊框
        linewidth=0.5,          # 更細的線條
        alpha=0.3,              # 透明度
        transform=ccrs.PlateCarree()
    )
    
    # 2. 繪製交通事故點位
    print("  - 繪製交通事故點位")
    
    # A1 類事故 (紅色,較大點)
    df_a1 = df_accidents[df_accidents['case_type'] == 'A1']
    ax.scatter(
        df_a1['longitude'], 
        df_a1['latitude'],
        c='red',
        s=30,               # 較大的點
        alpha=0.7,
        label=f'A1類事故 ({len(df_a1)}件)',
        transform=ccrs.PlateCarree(),
        zorder=3,
        edgecolors='darkred',
        linewidths=0.5
    )
    
    # A2 類事故 (橘色,較小點)
    df_a2 = df_accidents[df_accidents['case_type'] == 'A2']
    ax.scatter(
        df_a2['longitude'], 
        df_a2['latitude'],
        c='orange',
        s=8,                # 較小的點
        alpha=0.4,
        label=f'A2類事故 ({len(df_a2)}件)',
        transform=ccrs.PlateCarree(),
        zorder=2
    )
    
    # 3. 設定正方形地圖範圍 (與 viz_raw_map.py 一致)
    ax.set_extent([
        lon_center - square_size/2,
        lon_center + square_size/2,
        lat_center - square_size/2,
        lat_center + square_size/2
    ], crs=ccrs.PlateCarree())
    
    # 4. 加入淺色網格線 (與 viz_raw_map.py 一致)
    gl = ax.gridlines(
        draw_labels=True,
        linewidth=0.3,
        alpha=0.3,
        linestyle='--',
        color='gray'
    )
    gl.top_labels = False
    gl.right_labels = False
    
    # 5. 設定標題
    ax.set_title(
        '113年台北市交通事故分布圖',
        fontproperties=font_prop,
        fontsize=16,
        pad=20
    )
    
    # 6. 圖例
    ax.legend(
        loc='upper right',
        prop=font_prop,
        framealpha=0.9,
        fontsize=11
    )
    
    # 7. 確保輸出目錄存在
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    
    # 8. 儲存圖片
    output_path = FIGURES_DIR / 'taipei_accident_map.png'
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)  # 移除 bbox_inches='tight' 保持正方形
    plt.close()
    
    print(f"\n✓ 事故分布地圖已儲存至: {output_path}")
    print(f"  - 畫布大小: 14x14 英吋 (正方形)")
    print(f"  - A1事故: {len(df_a1)} 件 (紅色)")
    print(f"  - A2事故: {len(df_a2)} 件 (橘色)")
    print(f"  - 總計: {len(df_accidents)} 件事故")
    print(f"  - 解析度: 300 DPI")


if __name__ == "__main__":
    create_accident_map()
