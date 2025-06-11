# data_validation.py
import pandas as pd

def validate_data(file_path):
    df = pd.read_csv(file_path)
    
    # KPI 1: Total reviews
    total_reviews = len(df)
    
    # KPI 2: Missing data percentage
    missing_pct = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
    
    # KPI 3: Per-bank count
    bank_counts = df['bank'].value_counts().to_dict()
    
    print(f"Total Reviews: {total_reviews}")
    print(f"Missing Data: {missing_pct:.2f}%")
    print("Per Bank Counts:")
    for bank, count in bank_counts.items():
        print(f"- {bank}: {count} reviews")
    
    return total_reviews >= 1200 and missing_pct < 5

if __name__ == "__main__":
    is_valid = validate_data('bank_reviews.csv')
    print(f"Data Quality: {'PASS' if is_valid else 'FAIL'}")