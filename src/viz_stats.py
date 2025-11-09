# -*- coding: utf-8 -*-
"""
Module for generating statistical visualizations.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from src.config import PROCESSED_DATA_FILE, FIGURES_DIR

# --- 中文字型設定 ---
# 下載 'Noto Sans CJK TC' 字型，或指定您系統中已有的中文字型路徑
# FONT_PATH = '/path/to/your/chinese.ttf'
# if Path(FONT_PATH).exists():
#     fm.fontManager.addfont(FONT_PATH)
#     plt.rcParams['font.family'] = fm.FontProperties(fname=FONT_PATH).get_name()
# else:
#     print(f"警告：找不到中文字型於 {FONT_PATH}，圖表中的中文可能顯示為亂碼。")
#     # 使用 Matplotlib 內建的備用字型
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC', 'Microsoft JhengHei', 'Heiti TC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

def plot_by_district(df: pd.DataFrame):
    """
    繪製各行政區 A1/A2 事故數量的堆疊長條圖。
    """
    # 確保 FIGURE_DIR 存在
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    
    agg = (df.groupby(["district", "case_type"])
             .size().unstack(fill_value=0))
    
    # 確保 A1, A2 欄位存在
    if 'A1' not in agg.columns:
        agg['A1'] = 0
    if 'A2' not in agg.columns:
        agg['A2'] = 0
        
    agg['total'] = agg['A1'] + agg['A2']
    agg = agg.sort_values(by='total', ascending=True)
    
    ax = agg[['A1', 'A2']].plot(kind="barh", stacked=True, figsize=(10, 8), 
                               color=['#d62728', '#1f77b4'])

    ax.set_title("113年 台北市各行政區 A1/A2 交通事故數量", fontsize=16)
    ax.set_xlabel("事故數量", fontsize=12)
    ax.set_ylabel("行政區", fontsize=12)
    
    # 在長條圖上顯示總數
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
    
    if 'A1' not in agg.columns:
        agg['A1'] = 0
    if 'A2' not in agg.columns:
        agg['A2'] = 0

    ax = agg.plot(kind='bar', stacked=True, figsize=(12, 6),
                  color=['#d62728', '#1f77b4'])
    
    ax.set_title('113年 台北市各時段 A1/A2 交通事故數量', fontsize=16)
    ax.set_xlabel('小時 (24小時制)', fontsize=12)
    ax.set_ylabel('事故數量', fontsize=12)
    ax.tick_params(axis='x', rotation=0)
    
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
