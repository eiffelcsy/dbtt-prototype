"""
Data ingestion module for loading forum data from JSON files.
"""
import json
import pandas as pd
import logging
from datetime import datetime
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import (
    FORUM_TOPICS_FILE, 
    FORUM_REPLIES_FILE, 
    FORUM_CATEGORIES_FILE, 
    FORUM_STATS_FILE,
    PROCESSED_DATA_DIR
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_json_data(file_path):
    """
    Load data from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict or list: The loaded JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded data from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {str(e)}")
        return None

def convert_time_to_datetime(time_str):
    """
    Convert time strings like '2 hours ago', '1 day ago' to datetime objects.
    
    Args:
        time_str (str): The time string to convert
        
    Returns:
        datetime: The calculated datetime object
    """
    if not isinstance(time_str, str):
        return None
        
    now = datetime.now()
    
    if 'minute' in time_str:
        minutes = int(time_str.split()[0])
        return now.replace(microsecond=0) - pd.Timedelta(minutes=minutes)
    elif 'hour' in time_str:
        hours = int(time_str.split()[0])
        return now.replace(microsecond=0) - pd.Timedelta(hours=hours)
    elif 'day' in time_str:
        days = int(time_str.split()[0])
        return now.replace(microsecond=0) - pd.Timedelta(days=days)
    elif 'month' in time_str:
        months = int(time_str.split()[0])
        return now.replace(microsecond=0) - pd.Timedelta(days=months*30)
    elif 'year' in time_str:
        years = int(time_str.split()[0])
        return now.replace(microsecond=0) - pd.Timedelta(days=years*365)
    else:
        return None

def process_topics_data(topics_data):
    """
    Process topics data into a pandas DataFrame.
    
    Args:
        topics_data (list): The topics data
        
    Returns:
        pandas.DataFrame: The processed topics DataFrame
    """
    if not topics_data:
        return None
        
    df_topics = pd.DataFrame(topics_data)
    
    # Convert date strings to datetime objects
    df_topics['datetime'] = df_topics['date'].apply(convert_time_to_datetime)
    
    # Process text data for analysis
    df_topics['text_for_analysis'] = df_topics['title'] + " " + df_topics['content']
    
    return df_topics

def process_replies_data(replies_data):
    """
    Process replies data into a pandas DataFrame.
    
    Args:
        replies_data (list): The replies data
        
    Returns:
        pandas.DataFrame: The processed replies DataFrame
    """
    if not replies_data:
        logger.warning("No replies data to process")
        return None
    
    try:
        # Check if data is in list format (each item is a reply)
        if isinstance(replies_data, list):
            # Ensure all fields exist in each item
            processed_data = []
            required_fields = ['id', 'topic_id', 'author', 'content']
            
            for reply in replies_data:
                # Ensure all required fields exist
                processed_reply = {field: reply.get(field, None) for field in required_fields}
                
                # Add any additional fields
                for key, value in reply.items():
                    if key not in processed_reply:
                        processed_reply[key] = value
                
                processed_data.append(processed_reply)
                
            df_replies = pd.DataFrame(processed_data)
            
        # If data is in dictionary format (keys-values)
        elif isinstance(replies_data, dict):
            # Find the length of each array and ensure they're the same
            lengths = {key: len(value) if isinstance(value, list) else 0 for key, value in replies_data.items()}
            if len(set(lengths.values())) > 1:
                logger.warning("Dictionary has inconsistent lengths, padding shorter arrays")
                max_length = max(lengths.values())
                padded_data = {}
                
                for key, value in replies_data.items():
                    if isinstance(value, list):
                        # Pad shorter arrays with None
                        padded_data[key] = value + [None] * (max_length - len(value))
                    else:
                        padded_data[key] = [value] * max_length
                
                df_replies = pd.DataFrame(padded_data)
            else:
                df_replies = pd.DataFrame(replies_data)
        else:
            logger.error(f"Unexpected data type for replies: {type(replies_data)}")
            return None
            
        # Convert date strings to datetime objects
        if 'date' in df_replies.columns:
            df_replies['datetime'] = df_replies['date'].apply(convert_time_to_datetime)
        
        return df_replies
        
    except Exception as e:
        logger.error(f"Error processing replies data: {str(e)}")
        logger.info(f"Sample of replies data: {str(replies_data)[:500] if replies_data else 'None'}")
        # Create an empty DataFrame with expected columns as fallback
        return pd.DataFrame(columns=['id', 'topic_id', 'author', 'content', 'date'])

def process_categories_data(categories_data):
    """
    Process categories data into a pandas DataFrame.
    
    Args:
        categories_data (list): The categories data
        
    Returns:
        pandas.DataFrame: The processed categories DataFrame
    """
    if not categories_data:
        return None
        
    df_categories = pd.DataFrame(categories_data)
    return df_categories

def get_forum_data():
    """
    Load and process all forum data.
    
    Returns:
        tuple: A tuple containing (topics_df, replies_df, categories_df, stats_data)
    """
    # Load data
    topics_data = load_json_data(FORUM_TOPICS_FILE)
    replies_data = load_json_data(FORUM_REPLIES_FILE)
    categories_data = load_json_data(FORUM_CATEGORIES_FILE)
    stats_data = load_json_data(FORUM_STATS_FILE)
    
    # Process data
    topics_df = process_topics_data(topics_data)
    replies_df = process_replies_data(replies_data)
    categories_df = process_categories_data(categories_data)
    
    # Save processed data to CSV
    if topics_df is not None:
        topics_df.to_csv(os.path.join(PROCESSED_DATA_DIR, "topics.csv"), index=False)
        logger.info(f"Saved processed topics data to {os.path.join(PROCESSED_DATA_DIR, 'topics.csv')}")
    
    if replies_df is not None:
        replies_df.to_csv(os.path.join(PROCESSED_DATA_DIR, "replies.csv"), index=False)
        logger.info(f"Saved processed replies data to {os.path.join(PROCESSED_DATA_DIR, 'replies.csv')}")
    
    if categories_df is not None:
        categories_df.to_csv(os.path.join(PROCESSED_DATA_DIR, "categories.csv"), index=False)
        logger.info(f"Saved processed categories data to {os.path.join(PROCESSED_DATA_DIR, 'categories.csv')}")
    
    return topics_df, replies_df, categories_df, stats_data

if __name__ == "__main__":
    # Execute if run as a script
    topics_df, replies_df, categories_df, stats_data = get_forum_data()
    
    # Print info about loaded data
    if topics_df is not None:
        print(f"Loaded {len(topics_df)} topics")
    if replies_df is not None:
        print(f"Loaded {len(replies_df)} replies")
    if categories_df is not None:
        print(f"Loaded {len(categories_df)} categories")
    if stats_data is not None:
        print(f"Loaded forum stats: {stats_data}") 