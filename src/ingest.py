# -*- coding: utf-8 -*-
"""
Module for ingesting raw data.
"""
import pandas as pd
from src.config import RAW_DATA_FILE

def load_raw_data() -> pd.DataFrame:
    """
    Load raw data from the CSV file.
    
    Returns:
        pd.DataFrame: The raw data.
    """
    if not RAW_DATA_FILE.exists():
        raise FileNotFoundError(f"Raw data file not found at: {RAW_DATA_FILE}")
    
    # 加上 encoding='utf-8' 來確保能正確讀取中文內容
    return pd.read_csv(RAW_DATA_FILE, encoding='utf-8')
