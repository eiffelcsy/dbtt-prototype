#!/usr/bin/env python3
"""
Sentiment Analysis Script for DVD Forum Analytics

This script analyzes the sentiment of forum posts and replies
to understand customer sentiment about different movie genres and titles.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import logging
import sys
from wordcloud import WordCloud
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("analytics/logs/sentiment_analysis.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create necessary directories
os.makedirs("analytics/logs", exist_ok=True)
os.makedirs("analytics/reports/sentiment", exist_ok=True)
os.makedirs("analytics/reports/sentiment/charts", exist_ok=True)
os.makedirs("analytics/reports/sentiment/wordclouds", exist_ok=True)

# Download necessary NLTK resources
nltk_data_path = os.path.join(os.path.expanduser("~"), "nltk_data")
os.makedirs(nltk_data_path, exist_ok=True)

def download_nltk_data():
    """Download all necessary NLTK data."""
    try:
        # Set download directory
        nltk.data.path.append(nltk_data_path)
        
        # Essential resources for our analysis
        resources = ['punkt', 'stopwords', 'wordnet', 'punkt_tab']
        for resource in resources:
            try:
                logger.info(f"Downloading NLTK resource: {resource}")
                nltk.download(resource, quiet=False, download_dir=nltk_data_path)
            except Exception as e:
                logger.error(f"Error downloading {resource}: {str(e)}")
                
        logger.info("NLTK resources download complete")
    except Exception as e:
        logger.error(f"Error during NLTK resources download: {str(e)}")

# Ensure NLTK data is downloaded before proceeding
download_nltk_data()

def clean_text(text):
    """Clean and preprocess text for analysis."""
    if not isinstance(text, str):
        return ""
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove special characters and numbers
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Convert to lowercase
    text = text.lower().strip()
    
    return text

def get_sentiment(text):
    """Analyze sentiment of text using TextBlob."""
    if not text:
        return {"polarity": 0, "subjectivity": 0, "sentiment": "neutral"}
    
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity
    
    # Determine sentiment category
    if polarity > 0.1:
        sentiment = "positive"
    elif polarity < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "sentiment": sentiment
    }

def simple_tokenize(text):
    """
    A simple tokenizer that doesn't rely on NLTK's punkt model.
    This is a fallback method that splits text by whitespace.
    """
    if not isinstance(text, str) or not text.strip():
        return []
    
    # Simple whitespace-based tokenization
    tokens = text.lower().split()
    
    # Remove very short tokens
    tokens = [t for t in tokens if len(t) > 3]
    
    return tokens

def extract_keywords(text, n=5):
    """Extract the most important keywords from text."""
    if not isinstance(text, str) or not text.strip():
        return []
    
    try:
        # Try to use NLTK's tokenizer
        word_tokens = word_tokenize(text.lower())
    except Exception as e:
        # Fallback to simple tokenization if NLTK fails
        logger.warning(f"Failed to use NLTK tokenizer: {str(e)}. Using simple tokenizer instead.")
        word_tokens = simple_tokenize(text)
    
    try:
        # Try to use NLTK's stopwords
        stop_words = set(stopwords.words('english'))
    except Exception as e:
        # Fallback to a minimal set of stopwords if NLTK fails
        logger.warning(f"Failed to use NLTK stopwords: {str(e)}. Using minimal stopword list instead.")
        stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
                     'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 
                     'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 
                     'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 
                     'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 
                     'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 
                     'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
                     'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 
                     'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
                     'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
                     'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 
                     'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 
                     'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very'}
    
    # Filter out stopwords and short words
    filtered_words = [w for w in word_tokens if w not in stop_words and len(w) > 3]
    
    # Count word frequencies
    word_freq = {}
    for word in filtered_words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    
    # Sort by frequency and return top n keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:n]]

def generate_wordcloud(text, title, filename):
    """Generate and save wordcloud for the given text."""
    if not text or not isinstance(text, str):
        logger.warning(f"Cannot generate wordcloud for '{title}': empty or invalid text")
        return
    
    try:
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color='black',
            max_words=150,
            colormap='viridis',
            contour_width=1,
            contour_color='steelblue'
        ).generate(text)
        
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title(title, fontsize=16)
        plt.tight_layout()
        plt.savefig(f"analytics/reports/sentiment/wordclouds/{filename}.png", dpi=300)
        plt.close()
        
        logger.info(f"Generated wordcloud for '{title}'")
    except Exception as e:
        logger.error(f"Error generating wordcloud for '{title}': {str(e)}")

def analyze_sentiment_by_category(data, categories_df):
    """Analyze sentiment across different forum categories."""
    logger.info("Analyzing sentiment by category")
    
    # Join with categories
    merged_data = pd.merge(
        data,
        categories_df[['id', 'name']],
        left_on='category_id',
        right_on='id',
        how='left'
    )
    merged_data.rename(columns={'name': 'category_name'}, inplace=True)
    
    # Group by category and calculate average sentiment
    category_sentiment = merged_data.groupby('category_name').agg({
        'polarity': 'mean',
        'subjectivity': 'mean'
    }).reset_index()
    
    # Count sentiment types by category
    sentiment_counts = merged_data.groupby(['category_name', 'sentiment']).size().unstack(fill_value=0)
    
    # Merge the data
    category_analysis = pd.merge(
        category_sentiment,
        sentiment_counts,
        on='category_name',
        how='left'
    )
    
    # Calculate total posts and sentiment percentages
    category_analysis['total_posts'] = category_analysis['positive'] + category_analysis['neutral'] + category_analysis['negative']
    category_analysis['positive_pct'] = (category_analysis['positive'] / category_analysis['total_posts']) * 100
    category_analysis['neutral_pct'] = (category_analysis['neutral'] / category_analysis['total_posts']) * 100
    category_analysis['negative_pct'] = (category_analysis['negative'] / category_analysis['total_posts']) * 100
    
    # Save to CSV
    category_analysis.to_csv("analytics/reports/sentiment/category_sentiment.csv", index=False)
    
    # Create visualization
    plt.figure(figsize=(12, 6))
    sns.barplot(x='category_name', y='polarity', data=category_analysis)
    plt.title('Average Sentiment by Category', fontsize=16)
    plt.ylabel('Sentiment Polarity (Higher = More Positive)')
    plt.xlabel('Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("analytics/reports/sentiment/charts/category_sentiment.png", dpi=300)
    plt.close()
    
    # Create stacked bar chart for sentiment distribution
    plt.figure(figsize=(12, 6))
    category_analysis[['category_name', 'positive_pct', 'neutral_pct', 'negative_pct']].set_index('category_name').plot(
        kind='bar', 
        stacked=True,
        colormap='RdYlGn',
        figsize=(12, 6)
    )
    plt.title('Sentiment Distribution by Category', fontsize=16)
    plt.ylabel('Percentage')
    plt.xlabel('Category')
    plt.legend(title='Sentiment')
    plt.tight_layout()
    plt.savefig("analytics/reports/sentiment/charts/category_sentiment_distribution.png", dpi=300)
    plt.close()
    
    # Generate wordclouds for each category
    for category in merged_data['category_name'].unique():
        category_text = ' '.join(merged_data[merged_data['category_name'] == category]['cleaned_text'].dropna())
        generate_wordcloud(
            category_text, 
            f"Frequently Used Words in {category}", 
            f"wordcloud_category_{category.lower().replace(' & ', '_').replace(' ', '_')}"
        )
    
    logger.info("Category sentiment analysis complete")
    return category_analysis

def main():
    """Main function to perform sentiment analysis on forum data."""
    logger.info("Starting sentiment analysis process")
    
    # Load the processed data
    try:
        combined_data = pd.read_csv("analytics/data/combined_forum_data.csv")
        categories_df = pd.read_csv("analytics/data/categories.csv")
        logger.info(f"Loaded {len(combined_data)} posts for sentiment analysis")
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return
    
    # Clean the text
    combined_data['cleaned_text'] = combined_data['content'].apply(clean_text)
    
    # Analyze sentiment
    logger.info("Analyzing sentiment of forum posts")
    
    sentiment_results = []
    for idx, row in combined_data.iterrows():
        text = row['cleaned_text']
        sentiment_data = get_sentiment(text)
        keywords = extract_keywords(text)
        
        sentiment_results.append({
            'id': row['id'],
            'topic_id': row['topic_id'],
            'is_topic': row['is_topic'],
            'polarity': sentiment_data['polarity'],
            'subjectivity': sentiment_data['subjectivity'],
            'sentiment': sentiment_data['sentiment'],
            'keywords': ','.join(keywords),
            'category_id': row['category_id']
        })
    
    # Create DataFrame from sentiment results
    sentiment_df = pd.DataFrame(sentiment_results)
    
    # Merge with the original data
    combined_with_sentiment = pd.merge(
        combined_data,
        sentiment_df,
        on=['id', 'topic_id', 'is_topic', 'category_id'],
        how='left'
    )
    
    # Save the results
    combined_with_sentiment.to_csv("analytics/data/forum_data_with_sentiment.csv", index=False)
    
    # Calculate overall sentiment statistics
    overall_stats = {
        'total_posts': len(combined_with_sentiment),
        'avg_polarity': combined_with_sentiment['polarity'].mean(),
        'avg_subjectivity': combined_with_sentiment['subjectivity'].mean(),
        'positive_posts': len(combined_with_sentiment[combined_with_sentiment['sentiment'] == 'positive']),
        'neutral_posts': len(combined_with_sentiment[combined_with_sentiment['sentiment'] == 'neutral']),
        'negative_posts': len(combined_with_sentiment[combined_with_sentiment['sentiment'] == 'negative'])
    }
    
    # Calculate percentages
    overall_stats['positive_pct'] = (overall_stats['positive_posts'] / overall_stats['total_posts']) * 100
    overall_stats['neutral_pct'] = (overall_stats['neutral_posts'] / overall_stats['total_posts']) * 100
    overall_stats['negative_pct'] = (overall_stats['negative_posts'] / overall_stats['total_posts']) * 100
    
    # Save overall stats
    pd.DataFrame([overall_stats]).to_csv("analytics/reports/sentiment/overall_sentiment_stats.csv", index=False)
    
    # Analyze sentiment by category
    category_analysis = analyze_sentiment_by_category(combined_with_sentiment, categories_df)
    
    # Analyze topic-specific sentiment
    topics_only = combined_with_sentiment[combined_with_sentiment['is_topic'] == True].copy()
    replies_only = combined_with_sentiment[combined_with_sentiment['is_topic'] == False].copy()
    
    # Compare topic vs. reply sentiment
    comparison_data = [
        {
            'post_type': 'Topics',
            'avg_polarity': topics_only['polarity'].mean(),
            'positive_pct': len(topics_only[topics_only['sentiment'] == 'positive']) / len(topics_only) * 100,
            'neutral_pct': len(topics_only[topics_only['sentiment'] == 'neutral']) / len(topics_only) * 100,
            'negative_pct': len(topics_only[topics_only['sentiment'] == 'negative']) / len(topics_only) * 100
        },
        {
            'post_type': 'Replies',
            'avg_polarity': replies_only['polarity'].mean(),
            'positive_pct': len(replies_only[replies_only['sentiment'] == 'positive']) / len(replies_only) * 100,
            'neutral_pct': len(replies_only[replies_only['sentiment'] == 'neutral']) / len(replies_only) * 100,
            'negative_pct': len(replies_only[replies_only['sentiment'] == 'negative']) / len(replies_only) * 100
        }
    ]
    
    pd.DataFrame(comparison_data).to_csv("analytics/reports/sentiment/topic_vs_reply_sentiment.csv", index=False)
    
    # Generate overall wordcloud
    all_text = ' '.join(combined_with_sentiment['cleaned_text'].dropna())
    generate_wordcloud(all_text, "Frequently Used Words in All Forum Posts", "wordcloud_all_posts")
    
    # Generate positive and negative wordclouds
    positive_text = ' '.join(combined_with_sentiment[combined_with_sentiment['sentiment'] == 'positive']['cleaned_text'].dropna())
    negative_text = ' '.join(combined_with_sentiment[combined_with_sentiment['sentiment'] == 'negative']['cleaned_text'].dropna())
    
    generate_wordcloud(positive_text, "Words in Positive Sentiment Posts", "wordcloud_positive_posts")
    generate_wordcloud(negative_text, "Words in Negative Sentiment Posts", "wordcloud_negative_posts")
    
    logger.info("Sentiment analysis complete")
    logger.info(f"Results saved to analytics/reports/sentiment/")

if __name__ == "__main__":
    main() 