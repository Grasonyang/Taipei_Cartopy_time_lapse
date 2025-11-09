# -*- coding: utf-8 -*-
"""
Module for generating statistical visualizations.
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from src.config import PROCESSED_DATA_FILE, FIGURES_DIR

# --- 中文字型設定 ---
# 透過絕對路徑直接載入字型檔案，這是最可靠的方法
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
CHINESE_FONT = FontProperties(fname=FONT_PATH)
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

def plot_by_district(df: pd.DataFrame):
    """
    繪製各行政區 A1/A2 事故數量的堆疊長條圖。
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    
    agg = (df.groupby(["district", "case_type"])
             .size().unstack(fill_value=0))
    
    if 'A1' not in agg.columns: agg['A1'] = 0
    if 'A2' not in agg.columns: agg['A2'] = 0
        
    agg['total'] = agg['A1'] + agg['A2']
    agg = agg.sort_values(by='total', ascending=True)
    
    ax = agg[['A1', 'A2']].plot(kind="barh", stacked=True, figsize=(10, 8), 
                               color=['#d62728', '#1f77b4'])

    ax.set_title("113年 台北市各行政區 A1/A2 交通事故數量", fontproperties=CHINESE_FONT, fontsize=16)
    ax.set_xlabel("事故數量", fontproperties=CHINESE_FONT, fontsize=12)
    ax.set_ylabel("行政區", fontproperties=CHINESE_FONT, fontsize=12)
    
    # 設定 y 軸刻度標籤的字型
    for label in ax.get_yticklabels():
        label.set_fontproperties(CHINESE_FONT)
        
    # 設定圖例字型
    ax.legend(prop=CHINESE_FONT)
    
    for i, total in enumerate(agg['total']):
        ax.text(total + 5, i, str(total), va='center')
        
    plt.tight_layout()
    output_path = FIGURES_DIR / "district_distribution.png"
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"圖表已儲存至: {output_path}")

def plot_by_hour(df: pd.DataFrame):
    """
    繪製每小時 A1/A2 事故數量的長條圖。
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    
    agg = df.groupby(['hour', 'case_type']).size().unstack(fill_value=0)
    
    if 'A1' not in agg.columns: agg['A1'] = 0
    if 'A2' not in agg.columns: agg['A2'] = 0

    ax = agg.plot(kind='bar', stacked=True, figsize=(12, 6),
                  color=['#d62728', '#1f77b4'])
    
    ax.set_title('113年 台北市各時段 A1/A2 交通事故數量', fontproperties=CHINESE_FONT, fontsize=16)
    ax.set_xlabel('小時 (24小時制)', fontproperties=CHINESE_FONT, fontsize=12)
    ax.set_ylabel('事故數量', fontproperties=CHINESE_FONT, fontsize=12)
    ax.tick_params(axis='x', rotation=0)
    ax.legend(prop=CHINESE_FONT)
    
    plt.tight_layout()
    output_path = FIGURES_DIR / "hourly_distribution.png"
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"圖表已儲存至: {output_path}")

def main():
    """
    主函式，用於載入資料並執行所有繪圖函式。
    """
    if not PROCESSED_DATA_FILE.exists():
        print(f"錯誤：找不到處理後的資料檔案於 {PROCESSED_DATA_FILE}")
        print("請先執行 ETL 流程 (例如: python main.py)")
        return
        
    df = pd.read_parquet(PROCESSED_DATA_FILE)
    
    print("開始繪製統計圖表...")
    plot_by_district(df)
    plot_by_hour(df)
    print("統計圖表繪製完成。")

if __name__ == "__main__":
    main()
