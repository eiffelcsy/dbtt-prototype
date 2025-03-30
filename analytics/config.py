"""
Configuration settings for the DVD retail business analytics pipeline.
"""
import os
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.absolute()
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
FORUM_DATA_DIR = os.path.join(PROJECT_ROOT.parent, "pohkim", "public")

# Input data files
FORUM_TOPICS_FILE = os.path.join(FORUM_DATA_DIR, "forum-topics.json")
FORUM_REPLIES_FILE = os.path.join(FORUM_DATA_DIR, "forum-replies.json")
FORUM_CATEGORIES_FILE = os.path.join(FORUM_DATA_DIR, "forum-categories.json")
FORUM_STATS_FILE = os.path.join(FORUM_DATA_DIR, "forum-stats.json")

# Output directories
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = os.path.join(DATA_DIR, "models")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")
VISUALIZATIONS_DIR = os.path.join(DATA_DIR, "visualizations")

# Dashboard settings
DASHBOARD_ASSETS_DIR = os.path.join(PROJECT_ROOT, "dashboard", "assets")
DASHBOARD_PORT = 8050
DASHBOARD_DEBUG = True

# Sentiment analysis settings
SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
SENTIMENT_BATCH_SIZE = 16
SENTIMENT_MAX_LENGTH = 512

# Create directories if they don't exist
for directory in [DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, REPORTS_DIR, 
                  VISUALIZATIONS_DIR, DASHBOARD_ASSETS_DIR]:
    os.makedirs(directory, exist_ok=True) 