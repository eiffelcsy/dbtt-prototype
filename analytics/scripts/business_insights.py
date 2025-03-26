#!/usr/bin/env python3
"""
Business Insights Generator for DVD Forum Analytics

This script analyzes forum data with sentiment analysis results to generate
actionable business insights for DVD retail business decisions.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging
import sys
import re
from collections import Counter
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("analytics/logs/business_insights.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create necessary directories
os.makedirs("analytics/logs", exist_ok=True)
os.makedirs("analytics/reports/insights", exist_ok=True)
os.makedirs("analytics/reports/insights/charts", exist_ok=True)

def extract_movie_titles(text):
    """
    Extract potential movie titles from text.
    This is a simplified approach - in production, you'd want to use named entity recognition.
    """
    if not isinstance(text, str):
        return []
    
    # Look for text in quotes which might be movie titles
    quoted_titles = re.findall(r'\'([^\']+)\'|"([^"]+)"', text)
    flat_quoted = [item for sublist in quoted_titles for item in sublist if item]
    
    # Look for capitalized phrases which might be movie titles
    # This is a simplified approach
    cap_pattern = r'\b(?:[A-Z][a-z]*\s+){1,5}[A-Z][a-z]*\b'
    capitalized_titles = re.findall(cap_pattern, text)
    
    # Combine and remove duplicates
    all_potential_titles = list(set(flat_quoted + capitalized_titles))
    
    # Filter out common phrases that aren't titles
    common_phrases = ["I think", "I feel", "I believe", "In my opinion"]
    filtered_titles = [t for t in all_potential_titles if t not in common_phrases and len(t) > 3]
    
    return filtered_titles

def identify_trending_titles(data):
    """Identify trending movie titles based on mention frequency and sentiment."""
    logger.info("Identifying trending movie titles from forum posts")
    
    # Extract movie titles from all posts
    all_titles = []
    for idx, row in data.iterrows():
        titles = extract_movie_titles(row['content'])
        if titles:
            for title in titles:
                all_titles.append({
                    'title': title,
                    'post_id': row['id'],
                    'topic_id': row['topic_id'],
                    'sentiment': row['sentiment'],
                    'polarity': row['polarity'],
                    'is_topic': row['is_topic'],
                    'category_id': row['category_id']
                })
    
    # Convert to DataFrame
    if not all_titles:
        logger.warning("No movie titles identified in the data")
        return pd.DataFrame()
    
    titles_df = pd.DataFrame(all_titles)
    
    # Count title mentions
    title_counts = titles_df['title'].value_counts().reset_index()
    title_counts.columns = ['title', 'mentions']
    
    # Only consider titles mentioned multiple times
    trending_titles = title_counts[title_counts['mentions'] > 1]
    
    # Join with sentiment data
    title_sentiment = titles_df.groupby('title').agg({
        'polarity': 'mean',
        'topic_id': 'nunique'
    }).reset_index()
    title_sentiment.rename(columns={'topic_id': 'topics_mentioned_in'}, inplace=True)
    
    trending_with_sentiment = pd.merge(
        trending_titles,
        title_sentiment,
        on='title',
        how='left'
    )
    
    # Calculate sentiment distribution
    sentiment_distribution = titles_df.groupby(['title', 'sentiment']).size().unstack(fill_value=0).reset_index()
    trending_complete = pd.merge(
        trending_with_sentiment,
        sentiment_distribution,
        on='title',
        how='left'
    )
    
    # Fill NaN values with 0
    for col in ['positive', 'neutral', 'negative']:
        if col in trending_complete.columns:
            trending_complete[col] = trending_complete[col].fillna(0)
        else:
            trending_complete[col] = 0
    
    # Calculate total sentiment posts and percentages
    trending_complete['total_sentiment_posts'] = trending_complete['positive'] + trending_complete['neutral'] + trending_complete['negative']
    for col in ['positive', 'neutral', 'negative']:
        trending_complete[f'{col}_pct'] = (trending_complete[col] / trending_complete['total_sentiment_posts']) * 100
    
    # Sort by mentions and sentiment
    trending_complete = trending_complete.sort_values(['mentions', 'polarity'], ascending=[False, False])
    
    # Save the trending titles data
    trending_complete.to_csv("analytics/reports/insights/trending_titles.csv", index=False)
    
    # Visualize top titles
    top_n = min(10, len(trending_complete))
    top_titles = trending_complete.head(top_n)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='title', y='mentions', hue='polarity', data=top_titles, palette='RdYlGn')
    plt.title('Top Trending Titles by Mentions and Sentiment', fontsize=16)
    plt.xlabel('Title')
    plt.ylabel('Mentions')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("analytics/reports/insights/charts/top_trending_titles.png", dpi=300)
    plt.close()
    
    logger.info(f"Identified {len(trending_complete)} trending titles from forum discussions")
    return trending_complete

def identify_potential_acquisitions(trending_titles):
    """Identify potential DVD acquisitions based on positive sentiment and popularity."""
    if trending_titles.empty:
        logger.warning("No trending titles data available for acquisition recommendations")
        return pd.DataFrame()
    
    logger.info("Identifying potential DVD acquisitions based on forum sentiment")
    
    # Define criteria for potential acquisitions:
    # 1. Positive sentiment (polarity > 0.2)
    # 2. Mentioned in multiple topics
    # 3. Multiple mentions overall
    potential_acquisitions = trending_titles[
        (trending_titles['polarity'] > 0.2) & 
        (trending_titles['topics_mentioned_in'] > 1) &
        (trending_titles['mentions'] > 2)
    ].copy()
    
    # Calculate an acquisition score (simplified)
    potential_acquisitions['acquisition_score'] = (
        potential_acquisitions['polarity'] * 0.4 +
        potential_acquisitions['topics_mentioned_in'] * 0.3 +
        potential_acquisitions['mentions'] * 0.3
    )
    
    # Sort by acquisition score
    potential_acquisitions = potential_acquisitions.sort_values('acquisition_score', ascending=False)
    
    # Save recommendations
    potential_acquisitions.to_csv("analytics/reports/insights/acquisition_recommendations.csv", index=False)
    
    logger.info(f"Generated {len(potential_acquisitions)} acquisition recommendations")
    return potential_acquisitions

def analyze_category_performance(data, categories_df):
    """Analyze category performance based on engagement and sentiment."""
    logger.info("Analyzing category performance based on forum engagement and sentiment")
    
    # Join with categories
    merged_data = pd.merge(
        data,
        categories_df[['id', 'name']],
        left_on='category_id',
        right_on='id',
        how='left'
    )
    merged_data.rename(columns={'name': 'category_name'}, inplace=True)
    
    # Calculate engagement by category
    category_engagement = pd.DataFrame({
        'category_name': merged_data.groupby('category_name')['category_name'].first().values,
        'unique_topics': merged_data.groupby('category_name')['topic_id'].nunique().values,
        'total_posts': merged_data.groupby('category_name')['topic_id'].count().values,
        'polarity': merged_data.groupby('category_name')['polarity'].mean().values
    })
    
    # Calculate replies per topic
    topic_counts = merged_data[merged_data['is_topic'] == True].groupby('category_name').size()
    reply_counts = merged_data[merged_data['is_topic'] == False].groupby('category_name').size()
    
    category_engagement = pd.merge(
        category_engagement,
        topic_counts.reset_index(name='topic_count'),
        on='category_name',
        how='left'
    )
    
    category_engagement = pd.merge(
        category_engagement,
        reply_counts.reset_index(name='reply_count'),
        on='category_name',
        how='left'
    )
    
    # Fill NaN values with 0
    category_engagement['reply_count'] = category_engagement['reply_count'].fillna(0)
    
    # Calculate replies per topic
    category_engagement['replies_per_topic'] = category_engagement['reply_count'] / category_engagement['topic_count']
    
    # Calculate an engagement score
    category_engagement['engagement_score'] = (
        (category_engagement['total_posts'] / category_engagement['total_posts'].max()) * 0.4 +
        (category_engagement['replies_per_topic'] / category_engagement['replies_per_topic'].max()) * 0.4 +
        ((category_engagement['polarity'] + 1) / 2) * 0.2  # Normalize polarity to 0-1 range
    )
    
    # Rank categories by engagement score
    category_engagement['engagement_rank'] = category_engagement['engagement_score'].rank(ascending=False)
    
    # Save category performance data
    category_engagement.to_csv("analytics/reports/insights/category_performance.csv", index=False)
    
    # Visualize category performance
    plt.figure(figsize=(12, 6))
    sns.scatterplot(
        x='total_posts', 
        y='polarity', 
        size='replies_per_topic',
        hue='engagement_score', 
        data=category_engagement, 
        sizes=(100, 1000),
        palette='viridis'
    )
    
    # Add category labels
    for idx, row in category_engagement.iterrows():
        plt.annotate(
            row['category_name'], 
            (row['total_posts'], row['polarity']),
            xytext=(5, 5),
            textcoords='offset points'
        )
    
    plt.title('Category Performance Matrix', fontsize=16)
    plt.xlabel('Total Posts (Popularity)')
    plt.ylabel('Average Sentiment (Positivity)')
    plt.tight_layout()
    plt.savefig("analytics/reports/insights/charts/category_performance.png", dpi=300)
    plt.close()
    
    logger.info("Category performance analysis complete")
    return category_engagement

def generate_inventory_recommendations(category_performance, acquisition_recommendations):
    """Generate inventory recommendations based on category performance and trending titles."""
    logger.info("Generating inventory recommendations for DVD retail business")
    
    # Create inventory recommendations for high-performing categories
    top_categories = category_performance.sort_values('engagement_score', ascending=False).head(3)['category_name'].tolist()
    
    recommendations = {
        "high_performing_categories": top_categories,
        "category_recommendations": [],
        "specific_title_recommendations": []
    }
    
    # Generate category-specific recommendations
    for idx, row in category_performance.iterrows():
        category_name = row['category_name']
        engagement_score = row['engagement_score']
        engagement_rank = row['engagement_rank']
        sentiment = row['polarity']
        
        recommendation = {
            "category": category_name,
            "engagement_score": round(engagement_score, 2),
            "rank": int(engagement_rank),
            "sentiment": round(sentiment, 2),
            "recommendation": ""
        }
        
        # Generate recommendation based on engagement and sentiment
        if engagement_score > 0.7 and sentiment > 0.2:
            recommendation["recommendation"] = "EXPAND: High engagement and positive sentiment indicates strong customer interest. Increase inventory and promotional focus."
            recommendation["inventory_action"] = "Increase by 20-30%"
        elif engagement_score > 0.7 and sentiment < 0:
            recommendation["recommendation"] = "IMPROVE: High engagement but negative sentiment suggests customer interest but issues with content quality. Curate higher quality titles."
            recommendation["inventory_action"] = "Maintain but improve quality"
        elif engagement_score > 0.5:
            recommendation["recommendation"] = "MAINTAIN: Good engagement indicates steady interest. Maintain current inventory levels."
            recommendation["inventory_action"] = "Maintain current levels"
        elif engagement_score > 0.3:
            recommendation["recommendation"] = "SELECTIVE FOCUS: Moderate engagement suggests selective focus on popular sub-genres."
            recommendation["inventory_action"] = "Selective reduction, focus on high performers"
        else:
            recommendation["recommendation"] = "REDUCE: Low engagement suggests limited customer interest. Consider reducing inventory."
            recommendation["inventory_action"] = "Reduce by 10-20%"
        
        recommendations["category_recommendations"].append(recommendation)
    
    # Add specific title recommendations from acquisition recommendations
    if not acquisition_recommendations.empty:
        top_acquisitions = acquisition_recommendations.head(10)
        for idx, row in top_acquisitions.iterrows():
            title_rec = {
                "title": row['title'],
                "mentions": int(row['mentions']),
                "sentiment": round(row['polarity'], 2),
                "acquisition_score": round(row['acquisition_score'], 2),
                "recommendation": "ACQUIRE: High positive sentiment and frequent mentions indicate strong customer interest."
            }
            recommendations["specific_title_recommendations"].append(title_rec)
    
    # Save recommendations to JSON file
    with open("analytics/reports/insights/inventory_recommendations.json", 'w') as f:
        json.dump(recommendations, f, indent=2)
    
    # Create a simplified CSV version
    category_recommendations_df = pd.DataFrame(recommendations["category_recommendations"])
    category_recommendations_df.to_csv("analytics/reports/insights/category_inventory_recommendations.csv", index=False)
    
    if recommendations["specific_title_recommendations"]:
        title_recommendations_df = pd.DataFrame(recommendations["specific_title_recommendations"])
        title_recommendations_df.to_csv("analytics/reports/insights/title_inventory_recommendations.csv", index=False)
    
    logger.info("Inventory recommendations generated successfully")
    return recommendations

def main():
    """Main function to generate business insights from forum data analysis."""
    logger.info("Starting business insights generation process")
    
    # Load the sentiment analysis data
    try:
        data = pd.read_csv("analytics/data/forum_data_with_sentiment.csv")
        categories_df = pd.read_csv("analytics/data/categories.csv")
        logger.info(f"Loaded {len(data)} analyzed forum posts")
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return
    
    # Identify trending titles
    trending_titles = identify_trending_titles(data)
    
    # Identify potential acquisitions
    acquisition_recommendations = identify_potential_acquisitions(trending_titles)
    
    # Analyze category performance
    category_performance = analyze_category_performance(data, categories_df)
    
    # Generate inventory recommendations
    inventory_recommendations = generate_inventory_recommendations(
        category_performance, 
        acquisition_recommendations
    )
    
    # Generate executive summary
    exec_summary = {
        "overview": {
            "total_posts_analyzed": len(data),
            "overall_sentiment": round(data['polarity'].mean(), 2),
            "positive_posts_percentage": round(len(data[data['sentiment'] == 'positive']) / len(data) * 100, 1),
            "trending_titles_identified": len(trending_titles) if not trending_titles.empty else 0,
            "acquisition_recommendations": len(acquisition_recommendations) if not acquisition_recommendations.empty else 0
        },
        "top_performing_categories": category_performance.sort_values('engagement_score', ascending=False).head(3)[['category_name', 'engagement_score', 'polarity']].to_dict('records'),
        "key_insights": [
            "Customer engagement is highest in the " + category_performance.iloc[0]['category_name'] + " category, suggesting potential for expanded inventory",
            "Sentiment analysis reveals strong positive reception for titles in the " + category_performance.sort_values('polarity', ascending=False).iloc[0]['category_name'] + " category",
            f"Identified {len(acquisition_recommendations) if not acquisition_recommendations.empty else 0} potential new title acquisitions based on positive forum discussions"
        ],
    }
    
    # Save executive summary
    with open("analytics/reports/insights/executive_summary.json", 'w') as f:
        json.dump(exec_summary, f, indent=2)
    
    logger.info("Business insights generation complete")
    logger.info("Results saved to analytics/reports/insights/")

if __name__ == "__main__":
    main() 