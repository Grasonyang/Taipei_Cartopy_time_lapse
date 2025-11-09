# -*- coding: utf-8 -*-
"""
繪製最基礎的台北市行政區邊界地圖
- 粉紅色填充
- 淺灰色邊框
- 正方形畫布
- 使用 GeoPandas + Cartopy
"""

import sys
from pathlib import Path

# 確保可以找到 src 模組
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib.font_manager import FontProperties
from src.config import FIGURES_DIR

# 配置中文字型
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_prop = FontProperties(fname=font_path)


def load_taipei_boundary():
    """
    載入台北市行政區邊界 Shapefile 並轉換為 WGS84
    
    Returns:
        GeoDataFrame: 台北市邊界資料 (WGS84 座標系統)
    """
    shapefile_path = 'data/taipei/G97_A_CAVLGE_P.shp'
    
    try:
        # 讀取 Shapefile (原始座標系統: EPSG:3826 TWD97 TM2)
        gdf = gpd.read_file(shapefile_path)
        
        # 轉換座標系統到 WGS84 (EPSG:4326) - Cartopy PlateCarree 使用的座標系統
        gdf_wgs84 = gdf.to_crs(epsg=4326)
        
        print(f"✓ 成功讀取台北市邊界")
        print(f"  - 原始座標系統: {gdf.crs}")
        print(f"  - 轉換為: WGS84 (EPSG:4326)")
        print(f"  - 包含行政里數: {len(gdf_wgs84)}")
        
        bounds = gdf_wgs84.total_bounds
        print(f"  - 經度範圍: {bounds[0]:.6f} ~ {bounds[2]:.6f}")
        print(f"  - 緯度範圍: {bounds[1]:.6f} ~ {bounds[3]:.6f}")
        
        return gdf_wgs84
        
    except Exception as e:
        print(f"✗ 讀取 Shapefile 失敗: {e}")
        import traceback
        traceback.print_exc()
        return None


def create_raw_map():
    """
    創建最基礎的台北市邊界地圖
    - 粉紅色填充 (alpha=0.3)
    - 淺灰色邊框 (lightgray, linewidth=0.3)
    - 正方形畫布 (14x14)
    - 網格線淺色顯示
    """
    print("\n" + "="*60)
    print("創建基礎台北市邊界地圖")
    print("="*60 + "\n")
    
    # 載入邊界資料
    gdf_boundary = load_taipei_boundary()
    
    if gdf_boundary is None:
        print("✗ 無法創建地圖")
        return
    
    # 計算地圖範圍,確保 1:1 正方形
    bounds = gdf_boundary.total_bounds
    lon_range = bounds[2] - bounds[0]  # 經度範圍
    lat_range = bounds[3] - bounds[1]  # 緯度範圍
    
    # 計算中心點
    lon_center = (bounds[0] + bounds[2]) / 2
    lat_center = (bounds[1] + bounds[3]) / 2
    
    # 使用較大的範圍作為正方形邊長
    max_range = max(lon_range, lat_range)
    margin = max_range * 0.05  # 5% 邊距
    square_size = max_range + margin * 2
    
    # 創建正方形畫布
    fig = plt.figure(figsize=(14, 14))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    
    # 設定 1:1 aspect ratio
    ax.set_aspect('equal')
    
    print("\n繪製地圖...")
    
    # 繪製台北市邊界
    # - facecolor: 粉紅色填充
    # - edgecolor: 淺灰色邊框 (更淡)
    # - linewidth: 更細的線條
    # - alpha: 透明度
    gdf_boundary.plot(
        ax=ax,
        facecolor='pink',
        edgecolor='lightgray',  # 淺灰色邊框
        linewidth=0.3,          # 更細的線條
        alpha=0.3,              # 透明度
        transform=ccrs.PlateCarree()
    )
    
    # 設定正方形地圖範圍
    ax.set_extent([
        lon_center - square_size/2,  # min longitude
        lon_center + square_size/2,  # max longitude
        lat_center - square_size/2,  # min latitude
        lat_center + square_size/2   # max latitude
    ], crs=ccrs.PlateCarree())
    
    # 加入淺色網格線
    gl = ax.gridlines(
        draw_labels=True,
        linewidth=0.3,
        alpha=0.3,
        linestyle='--',
        color='gray'
    )
    gl.top_labels = False
    gl.right_labels = False
    
    # 設定標題
    ax.set_title(
        '台北市行政區邊界圖',
        fontproperties=font_prop,
        fontsize=16,
        pad=20
    )
    
    # 確保輸出目錄存在
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    
    # 儲存圖片
    output_path = FIGURES_DIR / 'taipei_raw_map.png'
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)  # 移除 bbox_inches='tight' 保持正方形
    plt.close()
    
    print(f"\n✓ 基礎地圖已儲存至: {output_path}")
    print(f"  - 畫布大小: 14x14 英吋 (正方形)")
    print(f"  - 填充顏色: 粉紅色 (alpha=0.3)")
    print(f"  - 邊框顏色: 淺灰色 (linewidth=0.3)")
    print(f"  - 解析度: 300 DPI")


if __name__ == "__main__":
    create_raw_map()
