# -*- coding: utf-8 -*-
"""
Configuration file for the Taipei Cartopy time lapse project.
"""
from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"  # 中間處理資料
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = BASE_DIR / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"
VIDEOS_DIR = OUTPUT_DIR / "videos"

# --- Data Files ---
RAW_DATA_FILE = RAW_DATA_DIR / "113年-臺北市A1及A2類交通事故明細.csv"
INTERIM_DATA_FILE = INTERIM_DATA_DIR / "taipei_113_cleaned.parquet"  # 清洗後的中間資料
PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "taipei_113_clean.parquet"  # 最終處理後的資料

# --- Column Mappings ---
COLUMN_MAP = {
    "發生年度": "year",
    "發生月": "month",
    "發生日": "day",
    "發生時-Hours": "hour",
    "發生分": "minute",
    "區序": "district",
    "道路照明設備": "light",
    "天候": "weather",
    "車種": "vehicle_type",
    "座標-X": "longitude",
    "座標-Y": "latitude",
    "處理別-編號": "case_type_full" # A1 or A2 is inside this string
}

LIGHT_MAP = {
    "白天": "day",
    "日間": "day",
    "夜間": "night",
    "夜晚": "night",
    "昏暗": "night"
}
