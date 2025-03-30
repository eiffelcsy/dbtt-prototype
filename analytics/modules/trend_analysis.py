"""
Trend analysis module for forum posts.

This module analyzes trends and patterns in forum discussions to identify 
popular topics, emerging trends, and changes in user sentiment over time.
"""
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import logging

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import (
    PROCESSED_DATA_DIR,
    VISUALIZATIONS_DIR,
    REPORTS_DIR
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def analyze_sentiment_by_category():
    """
    Analyze sentiment distribution across different forum categories.
    
    Returns:
        pandas.DataFrame: DataFrame with sentiment analysis by category
    """
    # Load processed data
    sentiment_path = os.path.join(PROCESSED_DATA_DIR, "topics_sentiment.csv")
    categories_path = os.path.join(PROCESSED_DATA_DIR, "categories.csv")
    
    if not os.path.exists(sentiment_path) or not os.path.exists(categories_path):
        logger.error("Required files for sentiment by category analysis not found")
        return None
        
    sentiment_df = pd.read_csv(sentiment_path)
    categories_df = pd.read_csv(categories_path)
    
    # Merge data
    sentiment_df = sentiment_df.merge(categories_df, left_on='category', right_on='id', how='left')
    
    # Group by category and calculate sentiment statistics
    sentiment_by_category = sentiment_df.groupby('name').agg({
        'sentiment_score': ['mean', 'median', 'std', 'count'],
        'sentiment_label': lambda x: (x == 'positive').mean() * 100,  # % positive
    }).reset_index()
    
    # Flatten multi-level columns
    sentiment_by_category.columns = ['category', 'avg_sentiment', 'median_sentiment', 
                                   'std_sentiment', 'topic_count', 'pct_positive']
    
    # Save results
    sentiment_by_category.to_csv(os.path.join(PROCESSED_DATA_DIR, "sentiment_by_category.csv"), index=False)
    logger.info(f"Saved sentiment by category analysis to {os.path.join(PROCESSED_DATA_DIR, 'sentiment_by_category.csv')}")
    
    # Create visualization
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")
    
    # Create bar chart with sentiment by category
    ax = sns.barplot(x='category', y='avg_sentiment', data=sentiment_by_category, 
                    palette='viridis', order=sentiment_by_category.sort_values('avg_sentiment', ascending=False)['category'])
    
    plt.title('Average Sentiment Score by Forum Category', fontsize=16)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Average Sentiment Score', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save plot
    plt.savefig(os.path.join(VISUALIZATIONS_DIR, "sentiment_by_category.png"), dpi=300, bbox_inches='tight')
    plt.close()
    
    return sentiment_by_category

def analyze_activity_trends(period='week'):
    """
    Analyze activity trends over time.
    
    Args:
        period (str): Time period for aggregation ('day', 'week', 'month')
        
    Returns:
        pandas.DataFrame: DataFrame with activity trends
    """
    # Load processed topics
    topics_path = os.path.join(PROCESSED_DATA_DIR, "topics.csv")
    
    if not os.path.exists(topics_path):
        logger.error(f"Topics file not found: {topics_path}")
        return None
        
    topics_df = pd.read_csv(topics_path)
    
    # Ensure datetime column is datetime type
    if 'datetime' in topics_df.columns:
        topics_df['datetime'] = pd.to_datetime(topics_df['datetime'])
    else:
        logger.error("Datetime column not found in topics data")
        return None
    
    # Group by time period
    if period == 'day':
        topics_df['period'] = topics_df['datetime'].dt.date
    elif period == 'week':
        topics_df['period'] = topics_df['datetime'].dt.to_period('W').dt.start_time.dt.date
    elif period == 'month':
        topics_df['period'] = topics_df['datetime'].dt.to_period('M').dt.start_time.dt.date
    else:
        logger.error(f"Invalid period: {period}")
        return None
    
    # Count topics and engagement by period
    activity_trends = topics_df.groupby('period').agg({
        'id': 'count',
        'replies': 'sum',
        'views': 'sum'
    }).reset_index()
    
    activity_trends.columns = ['period', 'topic_count', 'reply_count', 'view_count']
    
    # Calculate engagement ratio (replies/topic)
    activity_trends['engagement_ratio'] = activity_trends['reply_count'] / activity_trends['topic_count']
    
    # Save results
    activity_trends.to_csv(os.path.join(PROCESSED_DATA_DIR, f"activity_trends_{period}.csv"), index=False)
    logger.info(f"Saved activity trends by {period} to {os.path.join(PROCESSED_DATA_DIR, f'activity_trends_{period}.csv')}")
    
    # Create visualization
    plt.figure(figsize=(14, 8))
    sns.set_style("whitegrid")
    
    # Plot topic count as bars
    ax1 = plt.gca()
    ax1.bar(activity_trends['period'].astype(str), activity_trends['topic_count'], color='steelblue', alpha=0.7, label='Topics')
    ax1.set_xlabel(f'Time ({period.capitalize()})', fontsize=12)
    ax1.set_ylabel('Number of Topics', fontsize=12, color='steelblue')
    ax1.tick_params(axis='y', labelcolor='steelblue')
    
    # Plot engagement ratio as line on secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(activity_trends['period'].astype(str), activity_trends['engagement_ratio'], color='crimson', marker='o', label='Engagement')
    ax2.set_ylabel('Engagement Ratio (Replies/Topic)', fontsize=12, color='crimson')
    ax2.tick_params(axis='y', labelcolor='crimson')
    
    plt.title(f'Forum Activity Trends by {period.capitalize()}', fontsize=16)
    plt.xticks(rotation=45, ha='right')
    
    # Add legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.tight_layout()
    
    # Save plot
    plt.savefig(os.path.join(VISUALIZATIONS_DIR, f"activity_trends_{period}.png"), dpi=300, bbox_inches='tight')
    plt.close()
    
    return activity_trends

def analyze_trending_topics(n_days=30, top_n=10):
    """
    Identify trending topics based on recent engagement.
    
    Args:
        n_days (int): Number of days to consider for recent trends
        top_n (int): Number of top topics to return
        
    Returns:
        pandas.DataFrame: DataFrame with trending topics
    """
    # Load processed topics with sentiment
    sentiment_path = os.path.join(PROCESSED_DATA_DIR, "topics_sentiment.csv")
    
    if not os.path.exists(sentiment_path):
        logger.error(f"Topics with sentiment file not found: {sentiment_path}")
        return None
        
    topics_df = pd.read_csv(sentiment_path)
    
    # Ensure datetime column is datetime type
    if 'datetime' in topics_df.columns:
        topics_df['datetime'] = pd.to_datetime(topics_df['datetime'])
    else:
        logger.error("Datetime column not found in topics data")
        return None
    
    # Filter for recent topics
    cutoff_date = datetime.now() - timedelta(days=n_days)
    recent_topics = topics_df[topics_df['datetime'] >= cutoff_date].copy()
    
    if len(recent_topics) == 0:
        logger.warning(f"No topics found within the last {n_days} days")
        return pd.DataFrame()
    
    # Calculate engagement score
    recent_topics['engagement_score'] = (recent_topics['replies'] * 3) + (recent_topics['views'] * 0.5)
    
    # Sort by engagement score
    trending_topics = recent_topics.sort_values('engagement_score', ascending=False).head(top_n)
    
    # Select relevant columns
    trending_topics = trending_topics[['id', 'title', 'author', 'datetime', 'replies', 
                                     'views', 'engagement_score', 'sentiment_score', 'sentiment_label']]
    
    # Save results
    trending_topics.to_csv(os.path.join(PROCESSED_DATA_DIR, "trending_topics.csv"), index=False)
    logger.info(f"Saved trending topics to {os.path.join(PROCESSED_DATA_DIR, 'trending_topics.csv')}")
    
    # Create visualization
    plt.figure(figsize=(14, 10))
    sns.set_style("whitegrid")
    
    # Sort for visualization
    plot_data = trending_topics.sort_values('engagement_score')
    
    # Create horizontal bar chart
    bars = plt.barh(plot_data['title'], plot_data['engagement_score'], color=sns.color_palette("viridis", len(plot_data)))
    
    plt.title('Top Trending Forum Topics', fontsize=16)
    plt.xlabel('Engagement Score', fontsize=12)
    plt.ylabel('Topic', fontsize=12)
    plt.tight_layout()
    
    # Save plot
    plt.savefig(os.path.join(VISUALIZATIONS_DIR, "trending_topics.png"), dpi=300, bbox_inches='tight')
    plt.close()
    
    return trending_topics

def analyze_sentiment_trends(period='week'):
    """
    Analyze sentiment trends over time.
    
    Args:
        period (str): Time period for aggregation ('day', 'week', 'month')
        
    Returns:
        pandas.DataFrame: DataFrame with sentiment trends
    """
    # Load processed topics with sentiment
    sentiment_path = os.path.join(PROCESSED_DATA_DIR, "topics_sentiment.csv")
    
    if not os.path.exists(sentiment_path):
        logger.error(f"Topics with sentiment file not found: {sentiment_path}")
        return None
        
    topics_df = pd.read_csv(sentiment_path)
    
    # Ensure datetime column is datetime type
    if 'datetime' in topics_df.columns:
        topics_df['datetime'] = pd.to_datetime(topics_df['datetime'])
    else:
        logger.error("Datetime column not found in topics data")
        return None
    
    # Group by time period
    if period == 'day':
        topics_df['period'] = topics_df['datetime'].dt.date
    elif period == 'week':
        topics_df['period'] = topics_df['datetime'].dt.to_period('W').dt.start_time.dt.date
    elif period == 'month':
        topics_df['period'] = topics_df['datetime'].dt.to_period('M').dt.start_time.dt.date
    else:
        logger.error(f"Invalid period: {period}")
        return None
    
    # Calculate sentiment statistics by period
    sentiment_trends = topics_df.groupby('period').agg({
        'sentiment_score': ['mean', 'median', 'std', 'count'],
        'sentiment_label': lambda x: (x == 'positive').mean() * 100,  # % positive
    }).reset_index()
    
    # Flatten multi-level columns
    sentiment_trends.columns = ['period', 'avg_sentiment', 'median_sentiment', 
                             'std_sentiment', 'topic_count', 'pct_positive']
    
    # Save results
    sentiment_trends.to_csv(os.path.join(PROCESSED_DATA_DIR, f"sentiment_trends_{period}.csv"), index=False)
    logger.info(f"Saved sentiment trends by {period} to {os.path.join(PROCESSED_DATA_DIR, f'sentiment_trends_{period}.csv')}")
    
    # Create visualization
    plt.figure(figsize=(14, 8))
    sns.set_style("whitegrid")
    
    # Plot average sentiment as line
    ax1 = plt.gca()
    line1 = ax1.plot(sentiment_trends['period'].astype(str), sentiment_trends['avg_sentiment'], 
              color='blue', marker='o', linestyle='-', linewidth=2, label='Avg Sentiment Score')
    ax1.set_xlabel(f'Time ({period.capitalize()})', fontsize=12)
    ax1.set_ylabel('Average Sentiment Score', fontsize=12, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    # Plot percentage of positive posts on secondary y-axis
    ax2 = ax1.twinx()
    line2 = ax2.plot(sentiment_trends['period'].astype(str), sentiment_trends['pct_positive'], 
              color='green', marker='s', linestyle='--', linewidth=2, label='% Positive Posts')
    ax2.set_ylabel('Percentage of Positive Posts', fontsize=12, color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    
    plt.title(f'Sentiment Trends by {period.capitalize()}', fontsize=16)
    plt.xticks(rotation=45, ha='right')
    
    # Add legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    
    plt.tight_layout()
    
    # Save plot
    plt.savefig(os.path.join(VISUALIZATIONS_DIR, f"sentiment_trends_{period}.png"), dpi=300, bbox_inches='tight')
    plt.close()
    
    return sentiment_trends

def generate_trend_report():
    """
    Generate a comprehensive trend analysis report.
    
    Returns:
        str: Path to the generated report
    """
    # Run all analyses
    logger.info("Running trend analyses to generate comprehensive report")
    
    sentiment_by_category = analyze_sentiment_by_category()
    activity_trends_week = analyze_activity_trends(period='week')
    trending_topics = analyze_trending_topics(n_days=30, top_n=10)
    sentiment_trends_week = analyze_sentiment_trends(period='week')
    
    # Create report content
    report_content = []
    report_content.append("# DVD Retail Business Forum Analysis Report")
    report_content.append(f"## Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    # Add trending topics section
    report_content.append("## Top Trending Topics (Last 30 Days)")
    if trending_topics is not None and not trending_topics.empty:
        report_content.append("| Topic | Author | Replies | Views | Sentiment |")
        report_content.append("|-------|--------|---------|-------|-----------|")
        for _, row in trending_topics.iterrows():
            report_content.append(f"| {row['title']} | {row['author']} | {row['replies']} | {row['views']} | {row['sentiment_label']} |")
    else:
        report_content.append("No trending topics data available.")
    report_content.append("")
    
    # Add sentiment by category section
    report_content.append("## Sentiment Analysis by Category")
    if sentiment_by_category is not None and not sentiment_by_category.empty:
        report_content.append("| Category | Topic Count | Average Sentiment | % Positive |")
        report_content.append("|----------|-------------|-------------------|------------|")
        for _, row in sentiment_by_category.sort_values('avg_sentiment', ascending=False).iterrows():
            report_content.append(f"| {row['category']} | {row['topic_count']} | {row['avg_sentiment']:.4f} | {row['pct_positive']:.1f}% |")
    else:
        report_content.append("No sentiment by category data available.")
    report_content.append("")
    
    # Add activity trends section
    report_content.append("## Activity Trends (Weekly)")
    if activity_trends_week is not None and not activity_trends_week.empty:
        report_content.append("| Week | Topics | Replies | Views | Engagement Ratio |")
        report_content.append("|------|--------|---------|-------|------------------|")
        for _, row in activity_trends_week.iterrows():
            report_content.append(f"| {row['period']} | {row['topic_count']} | {row['reply_count']} | {row['view_count']} | {row['engagement_ratio']:.2f} |")
    else:
        report_content.append("No activity trends data available.")
    report_content.append("")
    
    # Add visualizations reference
    report_content.append("## Visualizations")
    report_content.append("Please refer to the visualizations directory for graphical representations of these trends.")
    
    # Join content and save report
    report_text = "\n".join(report_content)
    report_path = os.path.join(REPORTS_DIR, f"forum_trend_report_{datetime.now().strftime('%Y%m%d')}.md")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    logger.info(f"Saved comprehensive trend report to {report_path}")
    
    return report_path

if __name__ == "__main__":
    # Execute if run as a script
    report_path = generate_trend_report()
    print(f"Trend analysis report generated at: {report_path}") 