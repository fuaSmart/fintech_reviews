import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

# --- NLTK Data Downloads ---
# These are essential for text preprocessing (stopwords, wordnet for lemmatization, and tagger for wordnet)
# NLTK's download function will handle checking if the data is already present.
print("Downloading NLTK 'stopwords' data if not present...")
nltk.download('stopwords', quiet=True) # quiet=True prevents excessive output if already downloaded
print("Downloading NLTK 'wordnet' data if not present...")
nltk.download('wordnet', quiet=True)
print("Downloading NLTK 'averaged_perceptron_tagger' data if not present...")
nltk.download('averaged_perceptron_tagger', quiet=True)

# Load data with sentiment
try:
    df = pd.read_csv("reviews_with_sentiment.csv")
    print(f"Loaded {len(df)} reviews from reviews_with_sentiment.csv for thematic analysis.")
except FileNotFoundError:
    print("Error: reviews_with_sentiment.csv not found. Please ensure sentiment analysis is completed.")
    exit()

# --- Text Preprocessing for TF-IDF ---
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text_for_tfidf(text):
    text = str(text).lower() # Ensure text is string and lowercase
    text = re.sub(r'[^a-z\s]', '', text) # Remove non-alphabetic characters
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

df['processed_review_text'] = df['review_text'].apply(preprocess_text_for_tfidf)

# --- Keyword Extraction using TF-IDF ---
negative_reviews_df = df[df['sentiment_label'] == 'NEGATIVE'].copy()
positive_reviews_df = df[df['sentiment_label'] == 'POSITIVE'].copy()

vectorizer = TfidfVectorizer(max_df=0.85, min_df=5, stop_words='english', ngram_range=(1, 2))

print("\nExtracting keywords from NEGATIVE reviews...")
if not negative_reviews_df.empty:
    tfidf_matrix_neg = vectorizer.fit_transform(negative_reviews_df['processed_review_text'])
    feature_names_neg = vectorizer.get_feature_names_out()
    print("Top Negative Keywords per Bank:")
    for bank in negative_reviews_df['bank_name'].unique():
        bank_reviews = negative_reviews_df[negative_reviews_df['bank_name'] == bank]
        if not bank_reviews.empty:
            bank_indices = [negative_reviews_df.index.get_loc(idx) for idx in bank_reviews.index]
            avg_tfidf_scores = tfidf_matrix_neg[bank_indices].mean(axis=0).A1
            sorted_indices = avg_tfidf_scores.argsort()[::-1]
            top_keywords = [feature_names_neg[i] for i in sorted_indices[:10]]
            print(f"- {bank}: {', '.join(top_keywords)}")
else:
    print("No negative reviews to analyze for keywords.")

print("\nExtracting keywords from POSITIVE reviews...")
if not positive_reviews_df.empty:
    tfidf_matrix_pos = vectorizer.fit_transform(positive_reviews_df['processed_review_text'])
    feature_names_pos = vectorizer.get_feature_names_out()
    print("Top Positive Keywords per Bank:")
    for bank in positive_reviews_df['bank_name'].unique():
        bank_reviews = positive_reviews_df[positive_reviews_df['bank_name'] == bank]
        if not bank_reviews.empty:
            bank_indices = [positive_reviews_df.index.get_loc(idx) for idx in bank_reviews.index]
            avg_tfidf_scores = tfidf_matrix_pos[bank_indices].mean(axis=0).A1
            sorted_indices = avg_tfidf_scores.argsort()[::-1]
            top_keywords = [feature_names_pos[i] for i in sorted_indices[:10]]
            print(f"- {bank}: {', '.join(top_keywords)}")
else:
    print("No positive reviews to analyze for keywords.")


# --- Manual/Rule-Based Thematic Clustering ---
themes = {
    'App Stability & Bugs': ['crash', 'bug', 'error', 'login error', 'freezing', 'update problem', 'not working', 'fix app'],
    'Transaction Performance': ['slow', 'transfer', 'transaction', 'delay', 'pending', 'speed', 'fast', 'quick'],
    'User Interface & Experience': ['ui', 'interface', 'easy use', 'confusing', 'design', 'simple', 'user friendly', 'layout', 'good ui', 'bad ui'],
    'Customer Support': ['support', 'customer service', 'help', 'respond', 'call', 'chatbot', 'contact'],
    'Feature Requests & Completeness': ['fingerprint', 'otp', 'new feature', 'add', 'option', 'loan', 'transfer money', 'budgeting'],
    'Account Access': ['login', 'account', 'password', 'otp', 'access', 'blocked', 'register'],
}

def assign_themes(review_text, themes_dict):
    assigned = []
    text_lower = str(review_text).lower()
    for theme, keywords in themes_dict.items():
        if any(keyword in text_lower for keyword in keywords):
            assigned.append(theme)
    return assigned if assigned else ['Other']

print("\nAssigning themes to reviews...")
df['identified_themes'] = df['processed_review_text'].apply(lambda x: assign_themes(x, themes))

theme_counts = df['identified_themes'].explode().value_counts()
print("\nOverall Theme Distribution:")
print(theme_counts)

output_filename = "reviews_with_sentiment_and_themes.csv"
df.to_csv(output_filename, index=False, encoding='utf-8')
print(f"\nReviews with sentiment and themes saved to {output_filename}")
print(f"Final dataset size: {len(df)} rows.")

print("\nFirst 5 rows of data with sentiment and themes:")
print(df[['review_text', 'sentiment_label', 'sentiment_score', 'identified_themes']].head())