"""
Sentiment analysis module for forum posts.

This module uses the Hugging Face transformers library to perform sentiment analysis
on forum posts to determine customer sentiment about DVD titles and topics.
"""
import os
import sys
import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import logging
from tqdm import tqdm

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import (
    SENTIMENT_MODEL, 
    SENTIMENT_BATCH_SIZE, 
    SENTIMENT_MAX_LENGTH,
    PROCESSED_DATA_DIR,
    MODELS_DIR
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """
    Class for sentiment analysis of text using transformer models.
    """
    def __init__(self, model_name=SENTIMENT_MODEL, device=None):
        """
        Initialize the sentiment analyzer.
        
        Args:
            model_name (str): Name of the pre-trained model to use
            device (str, optional): Device to use ('cuda' or 'cpu'). If None, will use CUDA if available.
        """
        self.model_name = model_name
        
        # Set device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        logger.info(f"Using device: {self.device}")
        
        # Load tokenizer and model
        self.tokenizer = None
        self.model = None
        self._load_model()
        
    def _load_model(self):
        """
        Load the pre-trained tokenizer and model.
        """
        try:
            logger.info(f"Loading tokenizer and model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.model.to(self.device)
            logger.info("Tokenizer and model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def predict_sentiment(self, texts, batch_size=SENTIMENT_BATCH_SIZE):
        """
        Predict sentiment for a list of texts.
        
        Args:
            texts (list): List of texts to analyze
            batch_size (int): Batch size for processing
            
        Returns:
            pandas.DataFrame: DataFrame with sentiment scores (negative, neutral, positive)
        """
        if not texts:
            return pd.DataFrame()
            
        if self.model is None or self.tokenizer is None:
            logger.error("Model or tokenizer not loaded")
            return pd.DataFrame()
        
        results = []
        
        # Process in batches
        logger.info(f"Analyzing sentiment for {len(texts)} texts")
        for i in tqdm(range(0, len(texts), batch_size)):
            batch_texts = texts[i:i+batch_size]
            
            # Tokenize
            inputs = self.tokenizer(
                batch_texts, 
                padding=True, 
                truncation=True, 
                max_length=SENTIMENT_MAX_LENGTH, 
                return_tensors="pt"
            ).to(self.device)
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                
            # Process outputs
            scores = torch.nn.functional.softmax(outputs.logits, dim=1)
            scores_np = scores.cpu().numpy()
            
            for j, score in enumerate(scores_np):
                sentiment_result = {
                    'text': batch_texts[j][:100] + '...' if len(batch_texts[j]) > 100 else batch_texts[j],
                    'sentiment_score': scores_np[j][1],  # Positive class probability
                    'sentiment_label': 'positive' if scores_np[j][1] >= 0.6 else 'negative' if scores_np[j][1] <= 0.4 else 'neutral'
                }
                results.append(sentiment_result)
                
        return pd.DataFrame(results)

def analyze_forum_sentiment():
    """
    Run sentiment analysis on forum posts and save the results.
    
    Returns:
        pandas.DataFrame: DataFrame containing sentiment analysis results
    """
    # Load processed topics
    topics_path = os.path.join(PROCESSED_DATA_DIR, "topics.csv")
    if not os.path.exists(topics_path):
        logger.error(f"Topics file not found: {topics_path}")
        return None
    
    topics_df = pd.read_csv(topics_path)
    logger.info(f"Loaded {len(topics_df)} topics for sentiment analysis")
    
    # Initialize sentiment analyzer
    analyzer = SentimentAnalyzer()
    
    # Analyze texts
    texts = topics_df['text_for_analysis'].tolist()
    sentiment_results = analyzer.predict_sentiment(texts)
    
    # Combine with original data
    result_df = pd.concat([topics_df.reset_index(drop=True), sentiment_results[['sentiment_score', 'sentiment_label']]], axis=1)
    
    # Save results
    output_path = os.path.join(PROCESSED_DATA_DIR, "topics_sentiment.csv")
    result_df.to_csv(output_path, index=False)
    logger.info(f"Saved sentiment analysis results to {output_path}")
    
    return result_df

if __name__ == "__main__":
    # Execute if run as a script
    result_df = analyze_forum_sentiment()
    
    if result_df is not None:
        # Print distribution of sentiment
        sentiment_counts = result_df['sentiment_label'].value_counts()
        print("Sentiment distribution:")
        for label, count in sentiment_counts.items():
            print(f"{label}: {count} ({count/len(result_df)*100:.1f}%)") 