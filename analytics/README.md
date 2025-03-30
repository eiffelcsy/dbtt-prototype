# DVD Retail Business Analytics Pipeline

This analytics pipeline processes data from the community forum in the DVD retail business web app, performs sentiment analysis, topic modeling, and trend analysis to derive actionable business insights.

## Features

- **Data Ingestion**: Extract forum topics, replies, and user activity data
- **Sentiment Analysis**: Analyze the sentiment of forum posts using transformer models
- **Topic Modeling**: Identify key themes and topics in forum discussions
- **Trend Analysis**: Track sentiment and engagement trends over time
- **Business Insights**: Generate actionable recommendations for DVD retail business
- **Interactive Dashboard**: Visualize analytics results in a web-based dashboard

## Directory Structure

```
analytics/
├── config.py                  # Configuration settings
├── data/                      # Data directory
│   ├── models/                # Saved ML models
│   ├── processed/             # Processed data files
│   ├── reports/               # Analysis reports
│   └── visualizations/        # Generated visualizations
├── dashboard/                 # Dashboard application
│   ├── app.py                 # Dash application
│   └── assets/                # Dashboard assets
├── modules/                   # Analysis modules
│   ├── data_ingestion.py      # Forum data extraction
│   ├── sentiment_analysis.py  # Sentiment analysis
│   ├── topic_analysis.py      # Topic modeling and text analysis
│   └── trend_analysis.py      # Trend analysis and reporting
├── run_pipeline.py            # Main pipeline script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Setup

1. Create a Python virtual environment:
   ```
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Full Pipeline

To run the complete analytics pipeline:

```
python -m analytics.run_pipeline
```

This will execute the following steps:
1. Data ingestion from forum
2. Sentiment analysis
3. Topic modeling and text analysis
4. Trend analysis and reporting

### Running Individual Components

You can also run individual components of the pipeline:

```
# Data ingestion only
python -m analytics.modules.data_ingestion

# Sentiment analysis only
python -m analytics.modules.sentiment_analysis

# Topic analysis only
python -m analytics.modules.topic_analysis

# Trend analysis only
python -m analytics.modules.trend_analysis
```

### Launching the Dashboard

To launch the interactive analytics dashboard:

```
python -m analytics.dashboard.app
```

Then open your web browser and navigate to `http://127.0.0.1:8050/`.

## Analytics Dashboard

The interactive dashboard provides visualizations of:

- Forum activity trends
- Sentiment distribution by category
- Sentiment trends over time
- Trending topics
- Keyword frequency
- Business insights and recommendations

## Business Value

This analytics pipeline provides valuable insights for the DVD retail business:

1. **Inventory Management**: Identify popular topics and sentiment to guide DVD purchasing decisions
2. **Marketing Strategy**: Target marketing efforts based on trending discussions and customer sentiment
3. **Customer Experience**: Address negative sentiment topics and amplify positive sentiment drivers
4. **Content Strategy**: Develop blog posts and content around topics of interest
5. **Competitive Intelligence**: Understand competitors mentioned in forum discussions

## Technical Details

- **Sentiment Analysis**: Uses DistilBERT transformer model fine-tuned on SST-2 dataset
- **Topic Modeling**: Employs Latent Dirichlet Allocation (LDA) for topic extraction
- **Data Visualization**: Combines matplotlib/seaborn for static visuals and Plotly/Dash for interactive dashboard
- **NLP**: Uses NLTK for text processing and analysis

## Future Enhancements

- Real-time analytics via streaming pipeline
- User segmentation based on forum behavior
- Integration with sales data for correlation analysis
- Automated recommendations for inventory management
- Anomaly detection for unusual forum activity