import pandas as pd
from google_play_scraper import app, reviews, Sort
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

# Verified Ethiopian banking app IDs
APPS = {
    "CBE": "com.combank.eth.cbe",          # Commercial Bank of Ethiopia
    "BOA": "com.bankofabyssinia.mobile",   # Bank of Abyssinia
    "Dashen": "com.dashen.hayak"           # Dashen Bank
}

def scrape_app_reviews(app_id, bank_name, num_reviews=400):
    """Scrape reviews for a specific app with error handling"""
    try:
        result, _ = reviews(
            app_id,
            lang='en',
            country='et',  # Ethiopia
            sort=Sort.NEWEST,
            count=num_reviews,
            filter_score_with=None  # Get all ratings
        )
        return pd.DataFrame(result)[['content', 'score', 'at']].assign(
            bank=bank_name,
            source='Google Play'
        )
    except Exception as e:
        print(f"Error scraping {bank_name}: {str(e)}")
        return pd.DataFrame()

if __name__ == "__main__":
    all_reviews = []
    
    for bank_name, app_id in APPS.items():
        print(f"Scraping {bank_name}...")
        bank_reviews = scrape_app_reviews(app_id, bank_name)
        if not bank_reviews.empty:
            all_reviews.append(bank_reviews)
    
    if all_reviews:
        final_df = pd.concat(all_reviews)
        print(f"Total reviews scraped: {len(final_df)}")
        
        # Preprocessing
        final_df = final_df.rename(columns={
            'content': 'review',
            'score': 'rating',
            'at': 'date'
        })
        
        # Handle missing data
        final_df = final_df.dropna(subset=['review'])
        final_df = final_df.drop_duplicates(subset=['review'])
        
        # Normalize dates
        final_df['date'] = pd.to_datetime(final_df['date']).dt.strftime('%Y-%m-%d')
        
        # Save to CSV
        final_df[['review', 'rating', 'date', 'bank', 'source']].to_csv(
            'bank_reviews.csv', index=False
        )
        print("Data saved to bank_reviews.csv")
    else:
        print("No reviews scraped. Check app IDs and internet connection")