import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

# Load the cleaned data from Task 1
try:
    df = pd.read_csv("cleaned_fintech_reviews.csv")
    print(f"Loaded {len(df)} reviews from cleaned_fintech_reviews.csv")
except FileNotFoundError:
    print("Error: cleaned_fintech_reviews.csv not found. Please ensure Task 1 is completed.")
    exit()

# Initialize VADER sentiment intensity analyzer
print("Initializing VADER sentiment analyzer...")
analyzer = SentimentIntensityAnalyzer()
print("VADER analyzer loaded successfully.")

# Function to get sentiment for a single review using VADER
def get_vader_sentiment(text):
    if pd.isna(text) or not isinstance(text, str) or text.strip() == "":
        return {'label': 'NEUTRAL', 'score': 0.0} # Handle empty or non-string reviews

    vs = analyzer.polarity_scores(text)
    # VADER gives 'compound' score (range -1 to +1) and scores for neg, neu, pos.
    # We'll classify based on the compound score.
    compound_score = vs['compound']

    if compound_score >= 0.05:
        label = "POSITIVE"
        score = vs['pos'] # Use positive score for confidence
    elif compound_score <= -0.05:
        label = "NEGATIVE"
        score = vs['neg'] # Use negative score for confidence
    else:
        label = "NEUTRAL"
        score = vs['neu'] # Use neutral score for confidence
    return {'label': label, 'score': score}

# Apply sentiment analysis
print("Applying VADER sentiment analysis to reviews (this should be fast)...")
start_time = time.time()
df['sentiment_raw'] = df['review_text'].apply(get_vader_sentiment)

# Extract label and score into separate columns
df['sentiment_label'] = df['sentiment_raw'].apply(lambda x: x['label'])
df['sentiment_score'] = df['sentiment_raw'].apply(lambda x: x['score'])
df.drop(columns=['sentiment_raw'], inplace=True) # Drop the raw output column

end_time = time.time()
print(f"VADER sentiment analysis completed in {end_time - start_time:.2f} seconds.")

# Aggregate by bank and rating (example: mean sentiment score for 1-star reviews)
print("\nAggregating sentiment by bank and rating:")
# Map POSITIVE/NEGATIVE/NEUTRAL to numerical values for aggregation
sentiment_mapping = {'POSITIVE': 1, 'NEUTRAL': 0, 'NEGATIVE': -1}
df['sentiment_numerical'] = df['sentiment_label'].map(sentiment_mapping)

aggregated_sentiment = df.groupby(['bank_name', 'rating'])['sentiment_numerical'].mean().unstack()
print(aggregated_sentiment)

# Save the DataFrame with sentiment results
output_filename = "reviews_with_sentiment.csv"
df.to_csv(output_filename, index=False, encoding='utf-8')
print(f"\nReviews with sentiment saved to {output_filename}")
print(f"Number of reviews with sentiment scores: {len(df[df['sentiment_score'].notna()])} out of {len(df)}")

# Display first few rows of the data with sentiment
print("\nFirst 5 rows of data with sentiment:")
print(df[['review_text', 'sentiment_label', 'sentiment_score']].head())