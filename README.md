# Customer Experience Analytics for Fintech Apps

This repository contains the code and documentation for the "Customer Experience Analytics for Fintech Apps" project, a real-world data engineering challenge focused on scraping, analyzing, and visualizing Google Play Store reviews for Ethiopian banks.

## Project Objectives

Omega Consultancy is supporting banks to improve their mobile apps to enhance customer retention and satisfaction. As a Data Analyst, the key objectives are to:

- Scrape user reviews from the Google Play Store.
- Analyze sentiment (positive/negative/neutral) and extract themes (e.g., "bugs", "UI").
- Identify satisfaction drivers (e.g., speed) and pain points (e.g., crashes).

## Project Scenarios

This project addresses three key scenarios simulating real consulting tasks:

1.  **Retaining Users**: Analyze app performance for banks like CBE (4.4 stars), BOA (2.8 stars), and Dashen (4.0 stars), focusing on issues like slow loading during transfers.
2.  **Enhancing Features**: Extract desired features (e.g., fingerprint login, faster loading times) through keyword and theme extraction to recommend competitive strategies.
3.  **Managing Complaints**: Cluster and track specific complaints (e.g., “login error”) to guide AI chatbot integration and support resolution.

## Dataset Overview

The dataset will comprise scraped reviews from the Google Play Store for three banks' apps, collecting:

- Review Text: User feedback
- Rating: 1–5 stars
- Date: Posting date
- Bank/App Name: E.g., “Commercial bank of Ethiopia Mobile”
- Source: Google Play

The target is 400 reviews per bank (1200 total). Cleaned data will eventually be stored in an Oracle database, and a final report with visualizations and recommendations will be delivered.

## Technical Stack & Considerations

- **Operating System**: Ubuntu
- **Languages**: Python, SQL
- **Skill Level**: Beginner

---

## Task 1: Data Collection and Preprocessing

This section details the methodology employed for collecting raw user reviews from the Google Play Store and the initial preprocessing steps to prepare the data for subsequent analysis.

### Methodology

#### 1. Data Collection (Web Scraping)

- **Tool Used**: The `google-play-scraper` Python library was utilized for extracting review data directly from the Google Play Store. This library provides a robust and efficient way to programmatically access publicly available app reviews.
- **Target Applications**: Reviews were collected for three specific fintech banking applications:
  - **Commercial Bank of Ethiopia (CBE)**: App ID: `com.combanketh.mobilebanking`
  - **Bank of Abyssinia (BOA)**: App ID: `com.boa.boaMobileBanking`
  - **Dashen Bank**: App ID: `com.dashen.dashensuperapp`
- **Target Review Count**: For each bank, an attempt was made to scrape approximately 400 reviews, aiming for a total of at least 1,200 reviews across all three banks. The `google-play-scraper`'s `reviews` function was configured to fetch the newest reviews up to a specified count.
- **Data Points Collected**: For each review, the following information was extracted:
  - `review_id`
  - `review_text` (content)
  - `rating` (1-5 stars)
  - `review_date` (posting date and time)
  - `user_name` (reviewer's name)
  - `thumbs_up` (number of helpful votes)
  - `bank_name` (assigned during scraping based on the app ID)
  - `source` (set to 'Google Play')

#### 2. Data Preprocessing

The raw scraped data underwent a series of preprocessing steps to ensure data quality and consistency, as outlined below:

- **Duplicate Removal**: Reviews were checked for duplicates based on their unique `review_id`. Any redundant entries were removed to prevent biased analysis, ensuring each unique review is represented only once.
- **Handling Missing Data**:
  - Rows with missing `review_text` or `rating` were dropped, as these fields are critical for sentiment and thematic analysis.
  - Other less critical missing fields (e.g., `user_name`) were handled by imputation (e.g., filling with 'Anonymous') or retained if their absence did not impede core analysis.
- **Date Normalization**: The `review_date` column, initially in a datetime object format, was converted and normalized to a consistent `YYYY-MM-DD` string format for easier readability and integration with other systems.
- **Final Data Structure**: The cleaned data was structured into a Pandas DataFrame and saved as a CSV file (`cleaned_fintech_reviews.csv`) with the following core columns: `review_text`, `rating`, `review_date`, `bank_name`, and `source`.

This methodical approach ensures that the dataset is clean, reliable, and ready for in-depth sentiment and thematic analysis in subsequent tasks.

## Task 2: Sentiment and Thematic Analysis

This phase of the project focuses on extracting deeper meaning from the collected user reviews by quantifying sentiment and identifying recurring themes.

### Methodology

#### 1. Sentiment Analysis

- **Model Used**: Given the constraints and to ensure timely execution, the **VADER (Valence Aware Dictionary and sEntiment Reasoner)** lexicon and rule-based sentiment analysis tool was employed. VADER is particularly well-suited for social media text and provides robust sentiment scores without requiring extensive training data or large model downloads.
- **Approach**: For each review text, VADER calculates polarity scores (positive, negative, neutral, and a compound score). These scores were then used to assign a categorical sentiment label:
  - **POSITIVE**: Compound score $\ge 0.05$
  - **NEGATIVE**: Compound score $\le -0.05$
  - **NEUTRAL**: Compound score between $-0.05$ and $0.05$
- **Results**: The sentiment label (`POSITIVE`, `NEGATIVE`, `NEUTRAL`) and its corresponding score (representing confidence in the sentiment) were appended to each review record. Aggregated sentiment (e.g., average sentiment score per bank and rating) was also calculated to provide an overview.

#### 2. Thematic Analysis

Thematic analysis aimed to identify overarching concepts and topics within the reviews, transforming unstructured text into actionable categories.

- **Preprocessing Pipeline**: Prior to keyword extraction, review texts underwent a standard NLP preprocessing pipeline using `nltk` (Natural Language Toolkit):
  - **Tokenization**: Breaking down text into individual words or phrases.
  - **Stop-word Removal**: Eliminating common words (e.g., "the", "is", "a") that carry little semantic meaning.
  - **Lemmatization**: Reducing words to their base or root form (e.g., "running" to "run", "crashes" to "crash") to standardize terms.
- **Keyword Extraction**: The **TF-IDF (Term Frequency-Inverse Document Frequency)** method from `scikit-learn` was used to identify significant keywords and n-grams (sequences of words like "login error", "slow transfer"). TF-IDF assigns a weight to each term based on its frequency in a document relative to its frequency across all documents, highlighting terms unique and important to specific reviews. Keyword extraction was performed separately for negative and positive reviews to differentiate pain points from satisfaction drivers.
- **Theme Clustering (Manual/Rule-Based)**: Based on the extracted keywords and n-grams, a manual, rule-based approach was used to cluster related terms into 3-5 overarching themes. This involved defining a `themes` dictionary (within the `analyze_themes.py` script) where each theme (e.g., 'App Stability & Bugs', 'Transaction Performance', 'User Interface & Experience', 'Customer Support', 'Feature Requests & Completeness', 'Account Access') was associated with a set of relevant keywords. Reviews were then assigned to one or more themes if they contained any of the associated keywords. This method provides direct control and transparency in theme identification.

### Key Findings and Insights

Preliminary analysis from sentiment and thematic clustering reveals critical insights:

- **Common Pain Points**: Across all banks, prominent issues consistently emerged in negative reviews, including:
  - **"Slow loading/transfer"**: Directly addressing Scenario 1, this indicates that slow performance during transfers is a widespread frustration, not limited to a single bank. This warrants immediate investigation into backend processing, network latency, and app-side optimizations.
  - **"Login issues" and "App crashes"**: These fundamental stability problems are major drivers of negative sentiment and user churn. Resolving these core bugs should be a top priority for engineering teams.
  - **"Unresponsive support"**: Points to a need for improved customer service channels, potentially through better AI chatbot integration or faster human agent response times (aligning with Scenario 3).
- **Specific Drivers (Satisfaction)**: Positive reviews frequently highlighted terms like "easy to use," "convenient," and "good UI," indicating that user-friendly interfaces and streamlined processes are key satisfaction drivers.
- **Feature Gaps**: Keyword analysis also hinted at desired features, such as "fingerprint login" and requests for enhanced "transaction tracking" or "budgeting tools" (relevant to Scenario 2). These represent opportunities for innovation to stay competitive.
- **Bank-Specific Observations**:
  - **Bank of Abyssinia (BOA)**: Consistent with its lower average rating, BOA exhibits a significantly higher proportion of negative sentiment and more frequent complaints related to `Transaction Performance` and overall `App Stability`. This suggests systemic issues requiring comprehensive remediation.
  - **CBE & Dashen Bank**: While generally higher rated, even these banks show a noticeable volume of negative reviews concerning `App Stability & Bugs` and `Customer Support`, indicating room for improvement in these areas.

This analysis provides a clear roadmap for product, engineering, and marketing teams to address user pain points and enhance satisfaction.
