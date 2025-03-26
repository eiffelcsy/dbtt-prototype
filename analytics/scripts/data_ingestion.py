#!/usr/bin/env python3
"""
Data Ingestion Script for DVD Forum Analytics

This script extracts data from the JSON files containing forum data and prepares
it for analysis. It combines topic data with replies and categories.
"""

import json
import os
import pandas as pd
from datetime import datetime
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("analytics/logs/data_ingestion.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create logs directory if it doesn't exist
os.makedirs("analytics/logs", exist_ok=True)

# Create data directory if it doesn't exist
os.makedirs("analytics/data", exist_ok=True)

def load_json_data(file_path):
    """Load data from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading {file_path}: {str(e)}")
        return None

def convert_relative_time_to_datetime(relative_time):
    """Convert relative time strings to datetime objects."""
    try:
        # This is a simplified version - in production, you would want to handle all possible formats
        if 'ago' not in relative_time:
            return relative_time
        
        parts = relative_time.split(' ')
        if len(parts) < 2:
            return relative_time
        
        value = int(parts[0])
        unit = parts[1]
        
        now = datetime.now()
        
        if 'minute' in unit:
            return now.replace(minute=now.minute - value)
        elif 'hour' in unit:
            return now.replace(hour=now.hour - value)
        elif 'day' in unit:
            return now.replace(day=now.day - value)
        else:
            return relative_time
    except:
        return relative_time

def main():
    """Main function to ingest forum data."""
    logger.info("Starting data ingestion process")
    
    # Load data from JSON files
    base_dir = "pohkim/public"
    topics_data = load_json_data(os.path.join(base_dir, "forum-topics.json"))
    categories_data = load_json_data(os.path.join(base_dir, "forum-categories.json"))
    replies_data = load_json_data(os.path.join(base_dir, "forum-replies.json"))
    stats_data = load_json_data(os.path.join(base_dir, "forum-stats.json"))
    
    if not all([topics_data, categories_data, replies_data, stats_data]):
        logger.error("Failed to load all required data files")
        return
    
    logger.info(f"Loaded {len(topics_data)} topics, {len(categories_data)} categories")
    
    # Convert to DataFrames
    topics_df = pd.DataFrame(topics_data)
    categories_df = pd.DataFrame(categories_data)
    
    # Process replies data
    all_replies = []
    for topic_id, replies in replies_data.items():
        for reply in replies:
            reply['topic_id'] = int(topic_id)
            all_replies.append(reply)
    
    replies_df = pd.DataFrame(all_replies)
    
    # Convert relative times to datetime objects
    topics_df['datetime'] = topics_df['date'].apply(convert_relative_time_to_datetime)
    replies_df['datetime'] = replies_df['date'].apply(convert_relative_time_to_datetime)
    
    # Merge topics with categories
    topics_with_categories = pd.merge(
        topics_df, 
        categories_df[['id', 'name']], 
        left_on='category', 
        right_on='id', 
        suffixes=('', '_category')
    )
    topics_with_categories.rename(columns={'name': 'category_name'}, inplace=True)
    
    # Save processed data to CSV files for analysis
    topics_with_categories.to_csv("analytics/data/processed_topics.csv", index=False)
    replies_df.to_csv("analytics/data/processed_replies.csv", index=False)
    categories_df.to_csv("analytics/data/categories.csv", index=False)
    
    # Create a combined dataset with topics and their replies
    combined_data = []
    for topic in topics_data:
        topic_id = topic['id']
        topic_replies = replies_data.get(str(topic_id), [])
        
        # Add topic as a post
        topic_entry = {
            'id': f"t{topic_id}",
            'topic_id': topic_id,
            'author': topic['author'],
            'date': topic['date'],
            'content': topic['content'],
            'is_topic': True,
            'category_id': topic['category']
        }
        combined_data.append(topic_entry)
        
        # Add replies
        for reply in topic_replies:
            reply_entry = {
                'id': f"r{reply['id']}",
                'topic_id': topic_id,
                'author': reply['author'],
                'date': reply['date'],
                'content': reply['content'],
                'is_topic': False,
                'category_id': topic['category']
            }
            combined_data.append(reply_entry)
    
    combined_df = pd.DataFrame(combined_data)
    combined_df['datetime'] = combined_df['date'].apply(convert_relative_time_to_datetime)
    combined_df.to_csv("analytics/data/combined_forum_data.csv", index=False)
    
    logger.info("Data ingestion completed successfully")
    logger.info(f"Processed {len(topics_df)} topics and {len(replies_df)} replies")
    logger.info(f"Output saved to analytics/data/ directory")

if __name__ == "__main__":
    main() 