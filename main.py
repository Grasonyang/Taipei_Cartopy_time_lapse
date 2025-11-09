# -*- coding: utf--8 -*-
"""
Main script to run the ETL pipeline.
"""
from src.ingest import load_raw_data
from src.etl import clean_data
from src.config import PROCESSED_DATA_FILE

def main():
    """
    Main function to run the ETL pipeline.
    """
    print("Starting ETL pipeline...")
    
    # 1. Ingest
    print("Loading raw data...")
    raw_df = load_raw_data()
    
    # 2. ETL
    print("Cleaning data...")
    clean_df = clean_data(raw_df)
    
    # 3. Persist
    print(f"Saving cleaned data to {PROCESSED_DATA_FILE}...")
    PROCESSED_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_parquet(PROCESSED_DATA_FILE, index=False)
    
    print("ETL pipeline completed successfully.")
    print(f"\nCleaned data has {len(clean_df)} rows.")
    print("\nFirst 5 rows of cleaned data:")
    print(clean_df.head())

if __name__ == "__main__":
    main()
