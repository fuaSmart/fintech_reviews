import pandas as pd
# Assuming you have already run the scraping part and df is populated
# If running as a separate script, load the raw data:
# df = pd.read_csv("raw_fintech_reviews.csv")

all_reviews_data = []

df = pd.DataFrame(all_reviews_data)

# Save the raw data before full preprocessing (optional, but good for backup)
# df.to_csv("raw_fintech_reviews.csv", index=False)

print(f"\nTotal raw reviews collected: {len(df)}")
# --- Preprocessing Steps ---

# 1. Remove Duplicates
# A review might appear multiple times due to scraping method or updates.
# We'll consider review_id as the primary unique identifier.
initial_rows = len(df)
df.drop_duplicates(subset=['review_id'], inplace=True)
print(f"Removed {initial_rows - len(df)} duplicate reviews.")
print(f"Total reviews after removing duplicates: {len(df)}")

# 2. Handle Missing Data
# Check for missing values
print("\nMissing values before handling:")
print(df.isnull().sum())

# For review_text and rating, missing values are critical.
# For review_text, we'll drop rows where it's missing as it's central to analysis.
# For rating, also drop as it's essential.
df.dropna(subset=['review_text', 'rating'], inplace=True)

# For other columns like 'user_name' or 'thumbs_up', if they were missing,
# we might fill them with a placeholder (e.g., 'Unknown' or 0) or drop if not essential.
# For this project, review_text and rating are most important.
df['user_name'].fillna('Anonymous', inplace=True) # Example for non-critical column

print("\nMissing values after handling:")
print(df.isnull().sum())
print(f"Total reviews after handling missing data: {len(df)}")

# 3. Normalize Dates
# Convert the 'review_date' column to datetime objects and then format to YYYY-MM-DD.
df['review_date'] = pd.to_datetime(df['review_date'])
df['review_date'] = df['review_date'].dt.strftime('%Y-%m-%d')

# 4. Select and Reorder Final Columns
# Ensure the final DataFrame has exactly the required columns in the specified order.
df_cleaned = df[['review_text', 'rating', 'review_date', 'bank_name', 'source']]

# 5. Save as CSV
output_filename = "cleaned_fintech_reviews.csv"
df_cleaned.to_csv(output_filename, index=False, encoding='utf-8')
print(f"\nCleaned data saved to {output_filename}")
print(f"Final dataset size: {len(df_cleaned)} rows.")

# Display first few rows of the cleaned data
print("\nFirst 5 rows of cleaned data:")
print(df_cleaned.head())