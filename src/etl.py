# -*- coding: utf-8 -*-
"""
ETL 資料處理流程模組
分為兩階段:
1. raw → interim: 基礎清洗和轉換
2. interim → processed: 特徵工程和最終處理
"""
import pandas as pd
from zoneinfo import ZoneInfo
from src.config import COLUMN_MAP

# 根據 CSV 檔案中的實際值更新行政區對應
DISTRICT_MAP = {
    '01大同區': '大同區',
    '02萬華區': '萬華區',
    '03中山區': '中山區',
    '04大安區': '大安區',
    '05中正區': '中正區',
    '06松山區': '松山區',
    '07信義區': '信義區',
    '08士林區': '士林區',
    '09北投區': '北投區',
    '10文山區': '文山區',
    '11南港區': '南港區',
    '12內湖區': '內湖區'
}

# 根據資料字典或推斷，建立光線對應
# 假設 5=白天, 6=夜間有照明, 7=夜間無照明
LIGHT_MAP_FROM_NUMERIC = {
    5.0: "day",
    6.0: "night",
    7.0: "night"
}

# 根據資料字典或推斷，建立事故類別對應
CASE_TYPE_MAP = {
    1: 'A1',
    2: 'A2'
}


def clean_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    階段 1: 將原始資料進行基礎清洗和轉換 (raw → interim)
    
    處理步驟:
    1. 標準化欄位名稱
    2. 轉換時間格式 (民國年 → 西元年)
    3. 建立 datetime 欄位
    4. 轉換經緯度為數值
    5. 提取事故類別
    6. 移除明顯無效的資料
    
    Args:
        df (pd.DataFrame): 原始資料
    
    Returns:
        pd.DataFrame: 清洗後的中間資料
    """
    print("\n【階段 1: 基礎清洗】raw → interim")
    print(f"  原始資料筆數: {len(df)}")
    
    # 1. 標準化欄位名稱
    df = df.rename(columns=COLUMN_MAP)
    print(f"  ✓ 欄位名稱標準化完成")
    
    # 2. 處理時間欄位 (民國年轉西元年)
    df['year'] = df['year'] + 1911
    dt_str_df = df[['year', 'month', 'day', 'hour', 'minute']].astype(str)
    dt_str = dt_str_df['year'] + '-' + dt_str_df['month'].str.zfill(2) + '-' + \
             dt_str_df['day'].str.zfill(2) + ' ' + dt_str_df['hour'].str.zfill(2) + ':' + \
             dt_str_df['minute'].str.zfill(2)
    
    tpe = ZoneInfo("Asia/Taipei")
    dt_series = pd.to_datetime(dt_str, errors="coerce")
    df["acc_dt"] = dt_series.dt.tz_localize(tpe, nonexistent="shift_forward", ambiguous="NaT")
    print(f"  ✓ 時間欄位轉換完成 (民國 → 西元)")
    
    # 3. 處理經緯度
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    print(f"  ✓ 經緯度轉換為數值")
    
    # 4. 提取事故類別
    df['case_type'] = df['case_type_full'].map(CASE_TYPE_MAP)
    print(f"  ✓ 事故類別提取完成")
    
    # 5. 移除明顯無效的資料 (缺少關鍵欄位)
    before_drop = len(df)
    df = df.dropna(subset=["longitude", "latitude", "acc_dt", "case_type"])
    after_drop = len(df)
    print(f"  ✓ 移除無效資料: {before_drop - after_drop} 筆")
    
    # 6. 移除重複資料
    before_dedup = len(df)
    df = df.drop_duplicates(subset=['acc_dt', 'longitude', 'latitude'])
    after_dedup = len(df)
    print(f"  ✓ 移除重複資料: {before_dedup - after_dedup} 筆")
    
    print(f"  清洗後資料筆數: {len(df)}\n")
    
    return df


def process_interim_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    階段 2: 將中間資料進行特徵工程和最終處理 (interim → processed)
    
    處理步驟:
    1. 提取日期欄位
    2. 處理光線資訊
    3. 處理行政區名稱
    4. 修整文字欄位
    5. 選擇最終欄位
    
    Args:
        df (pd.DataFrame): 中間資料
    
    Returns:
        pd.DataFrame: 最終處理後的資料
    """
    print("【階段 2: 特徵工程】interim → processed")
    print(f"  中間資料筆數: {len(df)}")
    
    # 1. 提取日期欄位
    df["date"] = df["acc_dt"].dt.date
    print(f"  ✓ 提取日期欄位")
    
    # 2. 處理光線欄位
    df["light_bin"] = df["light"].map(LIGHT_MAP_FROM_NUMERIC).fillna("unknown")
    print(f"  ✓ 光線資訊分類完成")
    
    # 3. 處理行政區名稱 (移除編號前綴)
    df['district'] = df['district'].map(DISTRICT_MAP).fillna('未知')
    print(f"  ✓ 行政區名稱標準化")
    
    # 4. 修整文字欄位
    if 'vehicle_type' in df.columns:
        df['vehicle_type'] = df['vehicle_type'].str.strip()
        print(f"  ✓ 文字欄位修整完成")
    
    # 5. 選擇並排序最終需要的欄位
    final_cols = [
        'acc_dt', 'date', 'hour', 'district', 'case_type', 'light_bin', 
        'vehicle_type', 'longitude', 'latitude'
    ]
    for col in final_cols:
        if col not in df.columns:
            df[col] = None
    
    df_final = df[final_cols]
    print(f"  ✓ 選擇最終欄位: {len(final_cols)} 個")
    print(f"  最終資料筆數: {len(df_final)}\n")
    
    return df_final


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    完整的 ETL 流程 (向後相容)
    
    Args:
        df (pd.DataFrame): 原始資料
    
    Returns:
        pd.DataFrame: 最終處理後的資料
    """
    # 階段 1: 基礎清洗
    df_interim = clean_raw_data(df)
    
    # 階段 2: 特徵工程
    df_processed = process_interim_data(df_interim)
    
    return df_processed
