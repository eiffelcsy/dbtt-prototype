# DVD Retail Analytics Pipeline

This analytics pipeline extracts data from the community forum, performs sentiment analysis, and generates business insights for the DVD retail business.

## Features

- **Data Ingestion**: Extracts forum data (topics, replies, categories) from JSON files
- **Sentiment Analysis**: Analyzes sentiment of forum posts using TextBlob
- **Business Insights**: Identifies trending titles, potential acquisitions, and category performance
- **Inventory Recommendations**: Generates actionable recommendations for inventory management

## Directory Structure

```
analytics/
├── data/                     # Processed data files
├── models/                   # ML models (for future use)
├── reports/                  # Analysis reports
│   ├── insights/             # Business insights
│   └── sentiment/            # Sentiment analysis reports
├── scripts/                  # Pipeline scripts
│   ├── data_ingestion.py     # Data extraction and preprocessing
│   ├── sentiment_analysis.py # Sentiment analysis
│   └── business_insights.py  # Business insights generation
├── requirements.txt          # Required Python packages
├── run_pipeline.py           # Pipeline orchestration script
└── README.md                 # This file
```

## Installation

1. Ensure you have Python 3.8+ installed
2. Run the following command to install dependencies:

```bash
pip install -r analytics/requirements.txt
```

## Usage

To run the complete analytics pipeline:

```bash
python analytics/run_pipeline.py
```

This will:
1. Ingest data from the forum
2. Perform sentiment analysis
3. Generate business insights

## Individual Components

If you want to run specific parts of the pipeline:

```bash
# Data ingestion only
python analytics/scripts/data_ingestion.py

# Sentiment analysis only (requires data ingestion to be run first)
python analytics/scripts/sentiment_analysis.py

# Business insights only (requires sentiment analysis to be run first)
python analytics/scripts/business_insights.py
```

## Output Files

### Data Files
- `analytics/data/processed_topics.csv`: Processed forum topics
- `analytics/data/processed_replies.csv`: Processed forum replies
- `analytics/data/categories.csv`: Forum categories
- `analytics/data/combined_forum_data.csv`: Combined topics and replies
- `analytics/data/forum_data_with_sentiment.csv`: Data with sentiment analysis results

### Report Files
- `analytics/reports/sentiment/overall_sentiment_stats.csv`: Overall sentiment statistics
- `analytics/reports/sentiment/category_sentiment.csv`: Sentiment by category
- `analytics/reports/sentiment/topic_vs_reply_sentiment.csv`: Comparison of topic vs. reply sentiment
- `analytics/reports/insights/trending_titles.csv`: Trending titles from forum discussions
- `analytics/reports/insights/acquisition_recommendations.csv`: Recommended DVDs to acquire
- `analytics/reports/insights/category_performance.csv`: Category performance metrics
- `analytics/reports/insights/inventory_recommendations.json`: Inventory management recommendations
- `analytics/reports/insights/executive_summary.json`: Executive summary of findings

## Future Enhancements

- Advanced sentiment analysis using transformers
- Named entity recognition for more accurate movie title extraction
- Time-series analysis of sentiment trends
- Competitor analysis from forum discussions
- Integration with sales data for revenue impact predictions 