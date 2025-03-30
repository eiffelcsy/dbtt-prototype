"""
Topic analysis module for forum posts.

This module performs topic modeling and text analysis on forum posts to
identify key themes and topics being discussed.
"""
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import logging
import re
import string
from collections import Counter

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import (
    PROCESSED_DATA_DIR,
    VISUALIZATIONS_DIR
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Download NLTK resources
def download_nltk_resources():
    """Download required NLTK resources."""
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        logger.info("NLTK resources downloaded successfully")
    except Exception as e:
        logger.error(f"Error downloading NLTK resources: {str(e)}")

# Text preprocessing
def preprocess_text(text):
    """
    Preprocess text for topic modeling.
    
    Args:
        text (str): Text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    if not isinstance(text, str):
        return ""
        
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    additional_stopwords = {'film', 'movie', 'watch', 'scene', 'character', 'like', 'really', 'think', 'just', 'good', 'great', 'one', 'see', 'get', 'go', 'would', 'watch', 'watched', 'watching'}
    stop_words.update(additional_stopwords)
    tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
    
    # Join tokens
    return ' '.join(tokens)

def generate_wordcloud(text, title, output_path):
    """
    Generate a word cloud from text.
    
    Args:
        text (str): Text to generate word cloud from
        title (str): Title of the word cloud
        output_path (str): Path to save the word cloud image
    """
    try:
        # Generate word cloud
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color='black',
            colormap='viridis',
            max_words=100,
            contour_width=3,
            contour_color='steelblue'
        ).generate(text)
        
        # Plot
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title, fontsize=18)
        plt.tight_layout(pad=0)
        
        # Save
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Word cloud saved to {output_path}")
    except Exception as e:
        logger.error(f"Error generating word cloud: {str(e)}")

def extract_key_topics(texts, n_topics=5, n_top_words=10):
    """
    Extract key topics from a list of texts using LDA.
    
    Args:
        texts (list): List of preprocessed texts
        n_topics (int): Number of topics to extract
        n_top_words (int): Number of top words per topic to return
        
    Returns:
        tuple: (topics_df, vectorizer, lda_model)
    """
    # Create document-term matrix
    vectorizer = CountVectorizer(
        max_df=0.95,       # Ignore terms that appear in >95% of documents
        min_df=2,          # Ignore terms that appear in <2 documents
        max_features=1000, # Only consider top 1000 terms by frequency
        stop_words='english'
    )
    
    try:
        dtm = vectorizer.fit_transform(texts)
        
        # Create and fit LDA model
        lda_model = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42,
            max_iter=10,
            learning_method='online'
        )
        lda_model.fit(dtm)
        
        # Get feature names
        feature_names = vectorizer.get_feature_names_out()
        
        # Create DataFrame with top words for each topic
        topics_df = pd.DataFrame()
        
        for topic_idx, topic in enumerate(lda_model.components_):
            top_words_idx = topic.argsort()[:-n_top_words-1:-1]
            top_words = [feature_names[i] for i in top_words_idx]
            topics_df[f'Topic {topic_idx+1}'] = top_words
            
        return topics_df, vectorizer, lda_model
    except Exception as e:
        logger.error(f"Error in topic extraction: {str(e)}")
        return pd.DataFrame(), None, None

def analyze_forum_topics():
    """
    Analyze forum topics to identify key themes and generate visualizations.
    
    Returns:
        dict: Dictionary containing analysis results
    """
    # Load processed topics
    topics_path = os.path.join(PROCESSED_DATA_DIR, "topics.csv")
    if not os.path.exists(topics_path):
        logger.error(f"Topics file not found: {topics_path}")
        return None
    
    topics_df = pd.read_csv(topics_path)
    logger.info(f"Loaded {len(topics_df)} topics for text analysis")
    
    # Download NLTK resources
    download_nltk_resources()
    
    # Preprocess texts
    logger.info("Preprocessing forum texts")
    topics_df['processed_text'] = topics_df['text_for_analysis'].apply(preprocess_text)
    
    # Generate overall word cloud
    all_text = ' '.join(topics_df['processed_text'].tolist())
    wordcloud_path = os.path.join(VISUALIZATIONS_DIR, "forum_topics_wordcloud.png")
    generate_wordcloud(all_text, "DVD Forum Topics Word Cloud", wordcloud_path)
    
    # Extract topics
    logger.info("Extracting key topics from forum posts")
    topics_result, vectorizer, lda_model = extract_key_topics(topics_df['processed_text'].tolist())
    
    # Save topics to CSV
    if not topics_result.empty:
        topics_result.to_csv(os.path.join(PROCESSED_DATA_DIR, "forum_key_topics.csv"), index=False)
        logger.info(f"Saved key topics to {os.path.join(PROCESSED_DATA_DIR, 'forum_key_topics.csv')}")
    
    # Extract keyword frequency
    keywords = []
    for text in topics_df['processed_text'].tolist():
        keywords.extend(text.split())
    
    keyword_counter = Counter(keywords)
    top_keywords = pd.DataFrame(keyword_counter.most_common(30), columns=['keyword', 'frequency'])
    top_keywords.to_csv(os.path.join(PROCESSED_DATA_DIR, "forum_top_keywords.csv"), index=False)
    
    # Create keyword frequency plot
    plt.figure(figsize=(12, 8))
    plt.barh(top_keywords['keyword'][:15], top_keywords['frequency'][:15], color='steelblue')
    plt.xlabel('Frequency')
    plt.ylabel('Keyword')
    plt.title('Top 15 Keywords in Forum Discussions')
    plt.tight_layout()
    plt.savefig(os.path.join(VISUALIZATIONS_DIR, "forum_keyword_frequency.png"), dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        "topics_result": topics_result,
        "top_keywords": top_keywords,
        "wordcloud_path": wordcloud_path
    }

if __name__ == "__main__":
    # Execute if run as a script
    results = analyze_forum_topics()
    
    if results is not None and 'topics_result' in results and not results['topics_result'].empty:
        print("\nKey Topics Identified:")
        for col in results['topics_result'].columns:
            print(f"\n{col}:")
            print(", ".join(results['topics_result'][col].tolist()))
            
        print("\nTop 10 Keywords:")
        for _, row in results['top_keywords'].head(10).iterrows():
            print(f"{row['keyword']}: {row['frequency']}") 