"""
Main script to run the DVD retail business analytics pipeline.

This script orchestrates the entire analytics pipeline including:
1. Data ingestion from forum
2. Sentiment analysis
3. Topic modeling and text analysis
4. Trend analysis and reporting
"""
import os
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('analytics', 'pipeline.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_pipeline():
    """
    Run the complete analytics pipeline.
    """
    start_time = time.time()
    logger.info("Starting DVD retail business analytics pipeline")
    
    try:
        # Step 1: Data Ingestion
        logger.info("Step 1: Data Ingestion")
        from modules.data_ingestion import get_forum_data
        topics_df, replies_df, categories_df, stats_data = get_forum_data()
        logger.info(f"Loaded {len(topics_df) if topics_df is not None else 0} topics, " + 
                    f"{len(replies_df) if replies_df is not None else 0} replies, " + 
                    f"{len(categories_df) if categories_df is not None else 0} categories")
        
        # Step 2: Sentiment Analysis
        logger.info("Step 2: Sentiment Analysis")
        from modules.sentiment_analysis import analyze_forum_sentiment
        sentiment_df = analyze_forum_sentiment()
        logger.info(f"Completed sentiment analysis on {len(sentiment_df) if sentiment_df is not None else 0} forum posts")
        
        # Step 3: Topic Analysis
        logger.info("Step 3: Topic Modeling and Text Analysis")
        from modules.topic_analysis import analyze_forum_topics
        topic_results = analyze_forum_topics()
        logger.info("Completed topic modeling and text analysis")
        
        # Step 4: Trend Analysis
        logger.info("Step 4: Trend Analysis and Reporting")
        from modules.trend_analysis import generate_trend_report
        report_path = generate_trend_report()
        logger.info(f"Generated trend analysis report: {report_path}")
        
        # Calculate total runtime
        end_time = time.time()
        runtime = end_time - start_time
        logger.info(f"Analytics pipeline completed successfully in {runtime:.2f} seconds")
        
        print("\n" + "="*50)
        print(f"DVD Retail Business Analytics Pipeline Complete")
        print(f"Report generated at: {report_path}")
        print(f"Run dashboard with: python -m analytics.dashboard.app")
        print("="*50 + "\n")
        
        return True
    
    except Exception as e:
        logger.error(f"Error in analytics pipeline: {str(e)}")
        logger.exception("Stack trace:")
        
        # Calculate total runtime even if error occurs
        end_time = time.time()
        runtime = end_time - start_time
        logger.info(f"Analytics pipeline failed after {runtime:.2f} seconds")
        
        print("\n" + "="*50)
        print(f"DVD Retail Business Analytics Pipeline Failed")
        print(f"See logs for details")
        print("="*50 + "\n")
        
        return False

if __name__ == "__main__":
    run_pipeline() 