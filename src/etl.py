# -*- coding: utf-8 -*-
"""
Module for ETL processes.
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

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and transform the raw traffic accident data.

    Args:
        df (pd.DataFrame): The raw data.

    Returns:
        pd.DataFrame: The cleaned data.
    """
    # 1. 標準化欄位名稱
    df = df.rename(columns=COLUMN_MAP)

    # 2. 處理時間欄位
    df['year'] = df['year'] + 1911
    dt_str_df = df[['year', 'month', 'day', 'hour', 'minute']].astype(str)
    dt_str = dt_str_df['year'] + '-' + dt_str_df['month'].str.zfill(2) + '-' + \
             dt_str_df['day'].str.zfill(2) + ' ' + dt_str_df['hour'].str.zfill(2) + ':' + \
             dt_str_df['minute'].str.zfill(2)

    tpe = ZoneInfo("Asia/Taipei")
    dt_series = pd.to_datetime(dt_str, errors="coerce")
    df["acc_dt"] = dt_series.dt.tz_localize(tpe, nonexistent="shift_forward", ambiguous="NaT")
    df["date"] = df["acc_dt"].dt.date
    
    # 3. 處理光線欄位
    df["light_bin"] = df["light"].map(LIGHT_MAP_FROM_NUMERIC).fillna("unknown")

    # 4. 處理經緯度
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")

    # 5. 提取事故類別
    df['case_type'] = df['case_type_full'].map(CASE_TYPE_MAP)

    # 6. 處理行政區
    df['district'] = df['district'].map(DISTRICT_MAP).fillna('未知')

    # 7. 移除無效資料
    df = df.dropna(subset=["longitude", "latitude", "acc_dt", "case_type"])

    # 8. 修整文字欄位
    if 'vehicle_type' in df.columns:
        df['vehicle_type'] = df['vehicle_type'].str.strip()

    # 9. 移除重複資料
    df = df.drop_duplicates(subset=['acc_dt', 'longitude', 'latitude'])
    
    # 10. 選擇並排序最終需要的欄位
    final_cols = [
        'acc_dt', 'date', 'hour', 'district', 'case_type', 'light_bin', 
        'vehicle_type', 'longitude', 'latitude'
    ]
    for col in final_cols:
        if col not in df.columns:
            df[col] = None

    return df[final_cols]
