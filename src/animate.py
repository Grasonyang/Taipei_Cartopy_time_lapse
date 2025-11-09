# -*- coding: utf-8 -*-
"""
縮時攝影動畫模組
基於 viz_raw_map.py 的基礎地圖,產生交通事故的時間序列動畫
"""

import sys
from pathlib import Path

# 確保可以找到 src 模組
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
from matplotlib.font_manager import FontProperties
from src.config import PROCESSED_DATA_DIR, VIDEOS_DIR

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
        DataFrame: 包含事故經緯度和時間的資料
    """
    parquet_file = PROCESSED_DATA_DIR / 'taipei_113_clean.parquet'
    
    try:
        df = pd.read_parquet(parquet_file)
        # 確保 date 是 datetime 類型
        df['date'] = pd.to_datetime(df['date'])
        print(f"✓ 成功讀取 {len(df)} 筆事故資料")
        return df
    except Exception as e:
        print(f"✗ 讀取事故資料失敗: {e}")
        return None


def create_timelapse():
    """
    建立台北市交通事故縮時攝影動畫
    
    特點:
    - 基於 viz_raw_map.py 的粉紅色底圖
    - 正方形畫布 (14x14)
    - 按日期顯示累積事故
    - A1/A2 事故分別以不同顏色顯示
    """
    print("\n" + "="*60)
    print("開始製作縮時攝影動畫")
    print("="*60 + "\n")
    
    # 載入資料
    gdf_boundary = load_taipei_boundary()
    df_accidents = load_accident_data()
    
    if gdf_boundary is None or df_accidents is None:
        print("✗ 無法創建動畫")
        return
    
    # 取得所有日期並排序
    dates = sorted(df_accidents['date'].dropna().unique())
    print(f"  動畫時間範圍: {dates[0].strftime('%Y-%m-%d')} ~ {dates[-1].strftime('%Y-%m-%d')}")
    print(f"  總幀數: {len(dates)} 幀")
    
    # 計算地圖範圍,確保 1:1 正方形
    bounds = gdf_boundary.total_bounds
    lon_range = bounds[2] - bounds[0]
    lat_range = bounds[3] - bounds[1]
    
    lon_center = (bounds[0] + bounds[2]) / 2
    lat_center = (bounds[1] + bounds[3]) / 2
    
    max_range = max(lon_range, lat_range)
    margin = max_range * 0.05
    square_size = max_range + margin * 2
    
    # 創建正方形畫布
    fig = plt.figure(figsize=(14, 14))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_aspect('equal')
    
    # 繪製基礎台北市邊界 (與 viz_raw_map.py 相同設定)
    gdf_boundary.plot(
        ax=ax,
        facecolor='pink',
        edgecolor='lightgray',
        linewidth=0.3,
        alpha=0.3,
        transform=ccrs.PlateCarree()
    )
    
    # 設定正方形地圖範圍
    ax.set_extent([
        lon_center - square_size/2,
        lon_center + square_size/2,
        lat_center - square_size/2,
        lat_center + square_size/2
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
    
    # 初始化散點物件 (累積顯示)
    scat_a1 = ax.scatter(
        [], [], 
        c='red', 
        s=30, 
        alpha=0.7, 
        label='A1類事故',
        transform=ccrs.PlateCarree(),
        zorder=3,
        edgecolors='darkred',
        linewidths=0.5
    )
    
    scat_a2 = ax.scatter(
        [], [], 
        c='orange', 
        s=8, 
        alpha=0.4, 
        label='A2類事故',
        transform=ccrs.PlateCarree(),
        zorder=2
    )
    
    # 標題
    title_text = ax.set_title(
        '',
        fontproperties=font_prop,
        fontsize=16,
        pad=20
    )
    
    # 圖例 (暫時不使用中文字型以避免動畫渲染問題)
    ax.legend(loc='upper right', framealpha=0.9, fontsize=11, labels=['A1 Accidents', 'A2 Accidents'])
    
    # 累積資料列表 (用於顯示從開始到當前日期的所有事故)
    cumulative_a1_coords = []
    cumulative_a2_coords = []
    
    def init():
        """初始化動畫"""
        scat_a1.set_offsets(np.empty((0, 2)))
        scat_a2.set_offsets(np.empty((0, 2)))
        title_text.set_text('')
        return scat_a1, scat_a2, title_text
    
    def update(frame):
        """
        更新函式 - 每幀更新
        
        Args:
            frame (int): 當前幀數
            
        Returns:
            tuple: 需要更新的藝術家物件
        """
        nonlocal cumulative_a1_coords, cumulative_a2_coords
        
        # 取得當前日期
        current_date = dates[frame]
        
        # 篩選到當前日期為止的所有資料 (累積顯示)
        sub_df = df_accidents[df_accidents['date'] <= current_date]
        
        # 分離 A1 和 A2 事故
        df_a1 = sub_df[sub_df['case_type'] == 'A1']
        df_a2 = sub_df[sub_df['case_type'] == 'A2']
        
        # 更新散點位置 (累積)
        if len(df_a1) > 0:
            scat_a1.set_offsets(df_a1[['longitude', 'latitude']].to_numpy())
        
        if len(df_a2) > 0:
            scat_a2.set_offsets(df_a2[['longitude', 'latitude']].to_numpy())
        
        # 更新標題
        title_text.set_text(
            f'113年台北市交通事故累積分布\n'
            f'{current_date.strftime("%Y-%m-%d")} '
            f'(A1: {len(df_a1)}, A2: {len(df_a2)})'
        )
        
        return scat_a1, scat_a2, title_text
    
    print("\n開始生成動畫...")
    
    # 建立動畫
    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(dates),
        init_func=init,
        blit=True,
        interval=100,  # 每幀100ms
        repeat=True
    )
    
    # 確保輸出目錄存在
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 儲存動畫為 MP4
    output_path = VIDEOS_DIR / 'taipei_timelapse.mp4'
    
    try:
        print(f"  正在儲存動畫... (這可能需要幾分鐘)")
        ani.save(
            output_path,
            writer='ffmpeg',
            fps=10,
            dpi=100,  # 降低 DPI 以減少記憶體使用
            metadata={
                'title': '台北市113年交通事故縮時攝影',
                'artist': 'Taipei Traffic Analysis',
                'comment': 'A1/A2 traffic accidents time-lapse visualization'
            }
        )
        print(f"\n✓ 動畫已成功儲存至: {output_path}")
        
        # 顯示檔案資訊
        file_size = output_path.stat().st_size / (1024 * 1024)  # MB
        print(f"  檔案大小: {file_size:.2f} MB")
        print(f"  總幀數: {len(dates)} 幀")
        print(f"  播放速度: 10 fps")
        print(f"  預計播放時間: {len(dates)/10:.1f} 秒")
        
    except FileNotFoundError:
        print("\n✗ 錯誤: 找不到 'ffmpeg'")
        print("  請安裝 ffmpeg 以儲存動畫:")
        print("  Ubuntu/Debian: sudo apt install ffmpeg")
        print("  macOS: brew install ffmpeg")
        print("  Windows: https://ffmpeg.org/download.html")
        
    except Exception as e:
        print(f"\n✗ 儲存動畫時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        plt.close()


if __name__ == "__main__":
    create_timelapse()
