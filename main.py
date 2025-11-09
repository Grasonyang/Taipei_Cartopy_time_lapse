# -*- coding: utf-8 -*-
"""
主要 ETL 執行腳本
分階段處理: raw → interim → processed
"""
from src.ingest import load_raw_data
from src.etl import clean_raw_data, process_interim_data
from src.config import INTERIM_DATA_FILE, PROCESSED_DATA_FILE


def main():
    """
    執行完整的 ETL 流程
    
    流程:
    1. raw/: 載入原始資料
    2. interim/: 基礎清洗和轉換
    3. processed/: 特徵工程和最終處理
    """
    print("="*60)
    print("開始 ETL 流程")
    print("="*60)
    
    # ==================== 階段 1: 載入原始資料 ====================
    print("\n【資料載入】從 raw/ 讀取原始資料")
    raw_df = load_raw_data()
    print(f"✓ 載入完成: {len(raw_df)} 筆原始資料")
    
    # ==================== 階段 2: 基礎清洗 → interim ====================
    interim_df = clean_raw_data(raw_df)
    
    # 儲存中間資料
    INTERIM_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    interim_df.to_parquet(INTERIM_DATA_FILE, index=False)
    print(f"✓ 中間資料已儲存至: {INTERIM_DATA_FILE}")
    
    # ==================== 階段 3: 特徵工程 → processed ====================
    processed_df = process_interim_data(interim_df)
    
    # 儲存最終資料
    PROCESSED_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    processed_df.to_parquet(PROCESSED_DATA_FILE, index=False)
    print(f"✓ 最終資料已儲存至: {PROCESSED_DATA_FILE}")
    
    # ==================== 總結 ====================
    print("\n" + "="*60)
    print("ETL 流程完成")
    print("="*60)
    print(f"\n資料統計:")
    print(f"  原始資料 (raw):      {len(raw_df):,} 筆")
    print(f"  中間資料 (interim):  {len(interim_df):,} 筆")
    print(f"  最終資料 (processed): {len(processed_df):,} 筆")
    print(f"\n資料流程:")
    print(f"  raw/      → {INTERIM_DATA_FILE.relative_to(INTERIM_DATA_FILE.parent.parent.parent)}")
    print(f"  interim/  → {PROCESSED_DATA_FILE.relative_to(PROCESSED_DATA_FILE.parent.parent.parent)}")
    
    print(f"\n最終資料欄位: {list(processed_df.columns)}")
    print(f"\n前 5 筆資料預覽:")
    print(processed_df.head())
    
    print(f"\n事故類別統計:")
    print(processed_df['case_type'].value_counts())


if __name__ == "__main__":
    main()
