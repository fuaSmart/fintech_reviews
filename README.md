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
