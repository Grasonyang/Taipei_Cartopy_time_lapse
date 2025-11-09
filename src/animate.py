# -*- coding: utf-8 -*-
"""
Module for generating animated visualizations.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from src.config import PROCESSED_DATA_FILE, VIDEOS_DIR, BASE_DIR

# --- 中文字型設定 ---
# (與其他腳本相同)
import matplotlib.font_manager as fm
font_path = None
for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
    if 'NotoSansCJKtc-Regular' in font:
        font_path = font
        break
if font_path:
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
else:
    print("警告：找不到 'Noto Sans CJK TC' 字型，動畫中的中文可能顯示為亂碼。")
plt.rcParams['axes.unicode_minus'] = False

def create_timelapse(df: pd.DataFrame):
    """
    建立交通事故的縮時攝影動畫。
    """
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([121.45, 121.65, 24.95, 25.2], crs=ccrs.PlateCarree())

    # 繪製台北市邊界
    taipei_shp = str(BASE_DIR / 'data' / 'taipei' / 'G97_A_CAVLGE_P.shp')
    ax.add_geometries(shpreader.Reader(taipei_shp).geometries(),
                      ccrs.PlateCarree(),
                      facecolor='#e0e0e0', edgecolor='black')
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

    # 取得所有獨立的日期
    dates = sorted(df["date"].dropna().unique())
    
    # 初始化散點物件
    scat_day = ax.scatter([], [], s=15, alpha=0.7, label="白天", color="orange", transform=ccrs.PlateCarree())
    scat_night = ax.scatter([], [], s=15, alpha=0.7, label="夜晚", color="blue", transform=ccrs.PlateCarree())
    title = ax.set_title("")
    ax.legend()

    def init():
        scat_day.set_offsets([])
        scat_night.set_offsets([])
        title.set_text("")
        return scat_day, scat_night, title

    def update(frame):
        # 取得當天的日期
        current_date = dates[frame]
        
        # 篩選當天的資料
        sub_df = df[df["date"] == current_date]
        day_df = sub_df[sub_df["light_bin"] == "day"]
        night_df = sub_df[sub_df["light_bin"] == "night"]
        
        # 更新散點位置
        scat_day.set_offsets(day_df[['longitude', 'latitude']].to_numpy())
        scat_night.set_offsets(night_df[['longitude', 'latitude']].to_numpy())
        
        # 更新標題
        title.set_text(f"台北市交通事故: {current_date.strftime('%Y-%m-%d')}")
        
        return scat_day, scat_night, title

    # 建立動畫
    ani = animation.FuncAnimation(fig, update, frames=len(dates),
                                  init_func=init, blit=True, interval=200)

    # 儲存動畫
    output_path = VIDEOS_DIR / "timelapse.mp4"
    try:
        ani.save(output_path, writer='ffmpeg', fps=10, dpi=150)
        print(f"動畫已儲存至: {output_path}")
    except FileNotFoundError:
        print("\n錯誤：找不到 'ffmpeg'。")
        print("請確認您已安裝 ffmpeg 並將其加入系統路徑中。")
        print("若未安裝，動畫將無法儲存。")

    plt.close()

def main():
    if not PROCESSED_DATA_FILE.exists():
        print(f"錯誤：找不到處理後的資料檔案於 {PROCESSED_DATA_FILE}")
        return
        
    df = pd.read_parquet(PROCESSED_DATA_FILE)
    # 將 'date' 欄位轉為 datetime 物件以便排序
    df['date'] = pd.to_datetime(df['date'])
    
    print("開始製作縮時攝影動畫...")
    create_timelapse(df)
    print("動畫製作完成。")

if __name__ == "__main__":
    main()
