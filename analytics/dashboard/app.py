"""
Dashboard application for DVD retail business analytics.

This dashboard visualizes forum analytics to provide actionable insights.
"""
import os
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
from datetime import datetime
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import (
    PROCESSED_DATA_DIR,
    DASHBOARD_ASSETS_DIR,
    DASHBOARD_PORT,
    DASHBOARD_DEBUG
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    assets_folder=DASHBOARD_ASSETS_DIR
)
app.title = "DVD Retail Analytics Dashboard"

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("DVD Retail Business Analytics Dashboard", className="text-center mt-4 mb-4"),
            html.P("Forum Analytics & Sentiment Analysis", className="text-center text-muted mb-5")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Forum Activity Overview"),
                dbc.CardBody([
                    dcc.Graph(id="forum-activity-graph")
                ])
            ], className="mb-4")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Sentiment Analysis by Category"),
                dbc.CardBody([
                    dcc.Graph(id="sentiment-category-graph")
                ])
            ], className="mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Sentiment Trends"),
                dbc.CardBody([
                    dcc.Dropdown(
                        id="sentiment-period-dropdown",
                        options=[
                            {"label": "Weekly", "value": "week"},
                            {"label": "Monthly", "value": "month"}
                        ],
                        value="week",
                        clearable=False,
                        className="mb-3 text-dark"
                    ),
                    dcc.Graph(id="sentiment-trend-graph")
                ])
            ], className="mb-4")
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top Keywords"),
                dbc.CardBody([
                    dcc.Graph(id="top-keywords-graph")
                ])
            ], className="mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Trending Topics"),
                dbc.CardBody([
                    dash_table.DataTable(
                        id="trending-topics-table",
                        style_cell={
                            'backgroundColor': '#303030',
                            'color': 'white',
                            'textAlign': 'left',
                            'padding': '15px',
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                        style_header={
                            'backgroundColor': '#404040',
                            'fontWeight': 'bold',
                            'border': '1px solid #505050'
                        },
                        style_data_conditional=[
                            {
                                'if': {'column_id': 'sentiment_label', 'filter_query': '{sentiment_label} = "positive"'},
                                'backgroundColor': 'rgba(50, 205, 50, 0.2)',
                                'color': 'lightgreen'
                            },
                            {
                                'if': {'column_id': 'sentiment_label', 'filter_query': '{sentiment_label} = "negative"'},
                                'backgroundColor': 'rgba(255, 0, 0, 0.2)',
                                'color': 'tomato'
                            },
                            {
                                'if': {'column_id': 'sentiment_label', 'filter_query': '{sentiment_label} = "neutral"'},
                                'backgroundColor': 'rgba(160, 160, 160, 0.2)',
                                'color': 'lightgray'
                            }
                        ],
                        page_size=5
                    )
                ])
            ], className="mb-4")
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.P(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                   className="text-muted text-center mb-4"),
            html.Div([
                dcc.Interval(
                    id='interval-component',
                    interval=300 * 1000,
                    n_intervals=0
                )
            ])
        ], width=12)
    ])
], fluid=True)

@app.callback(
    Output("forum-activity-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_forum_activity_graph(n):
    try:
        activity_file = os.path.join(PROCESSED_DATA_DIR, "activity_trends_week.csv")
        if not os.path.exists(activity_file):
            return create_empty_figure("No activity data available")
            
        df = pd.read_csv(activity_file)
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(
                x=df['period'],
                y=df['topic_count'],
                name="Topics",
                marker_color='royalblue'
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['period'],
                y=df['engagement_ratio'],
                name="Engagement",
                marker_color='firebrick',
                mode='lines+markers'
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            title_text="Forum Activity Trends",
            template="plotly_dark",
            plot_bgcolor='rgba(50, 50, 50, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        fig.update_xaxes(title_text="Week")
        
        fig.update_yaxes(title_text="Number of Topics", secondary_y=False)
        fig.update_yaxes(title_text="Engagement Ratio (Replies/Topic)", secondary_y=True)
        
        return fig
    except Exception as e:
        logger.error(f"Error creating forum activity graph: {str(e)}")
        return create_empty_figure(f"Error: {str(e)}")

@app.callback(
    Output("sentiment-category-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_sentiment_category_graph(n):
    try:
        sentiment_file = os.path.join(PROCESSED_DATA_DIR, "sentiment_by_category.csv")
        if not os.path.exists(sentiment_file):
            return create_empty_figure("No sentiment by category data available")
            
        df = pd.read_csv(sentiment_file)
        
        df = df.sort_values('avg_sentiment', ascending=False)
        
        fig = px.bar(
            df, 
            x='category', 
            y='avg_sentiment',
            color='pct_positive',
            color_continuous_scale='RdYlGn',
            labels={
                'category': 'Forum Category',
                'avg_sentiment': 'Average Sentiment Score',
                'pct_positive': '% Positive'
            },
            hover_data=['topic_count', 'pct_positive']
        )
        
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(50, 50, 50, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            height=400,
            margin=dict(l=20, r=20, t=20, b=80)
        )
        
        fig.update_xaxes(tickangle=45)
        
        return fig
    except Exception as e:
        logger.error(f"Error creating sentiment category graph: {str(e)}")
        return create_empty_figure(f"Error: {str(e)}")

@app.callback(
    Output("sentiment-trend-graph", "figure"),
    [Input("sentiment-period-dropdown", "value"),
     Input("interval-component", "n_intervals")]
)
def update_sentiment_trend_graph(period, n):
    try:
        sentiment_file = os.path.join(PROCESSED_DATA_DIR, f"sentiment_trends_{period}.csv")
        if not os.path.exists(sentiment_file):
            return create_empty_figure(f"No sentiment trends data available for {period}")
            
        df = pd.read_csv(sentiment_file)
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(
                x=df['period'],
                y=df['avg_sentiment'],
                name="Avg Sentiment",
                marker_color='dodgerblue',
                mode='lines+markers'
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['period'],
                y=df['pct_positive'],
                name="% Positive",
                marker_color='limegreen',
                mode='lines+markers'
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            title_text=f"Sentiment Trends ({period.capitalize()})",
            template="plotly_dark",
            plot_bgcolor='rgba(50, 50, 50, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        fig.update_xaxes(title_text=period.capitalize())
        
        fig.update_yaxes(title_text="Average Sentiment Score", secondary_y=False)
        fig.update_yaxes(title_text="% Positive Posts", secondary_y=True)
        
        return fig
    except Exception as e:
        logger.error(f"Error creating sentiment trend graph: {str(e)}")
        return create_empty_figure(f"Error: {str(e)}")

@app.callback(
    Output("top-keywords-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_keywords_graph(n):
    try:
        keywords_file = os.path.join(PROCESSED_DATA_DIR, "forum_top_keywords.csv")
        if not os.path.exists(keywords_file):
            return create_empty_figure("No keywords data available")
            
        df = pd.read_csv(keywords_file)
        
        df = df.head(15)
        
        fig = px.bar(
            df,
            y='keyword',
            x='frequency',
            orientation='h',
            color='frequency',
            color_continuous_scale='Viridis',
            labels={
                'keyword': 'Keyword',
                'frequency': 'Frequency'
            }
        )
        
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(50, 50, 50, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    except Exception as e:
        logger.error(f"Error creating keywords graph: {str(e)}")
        return create_empty_figure(f"Error: {str(e)}")

@app.callback(
    Output("trending-topics-table", "data"),
    Output("trending-topics-table", "columns"),
    Input("interval-component", "n_intervals")
)
def update_trending_topics_table(n):
    try:
        topics_file = os.path.join(PROCESSED_DATA_DIR, "trending_topics.csv")
        if not os.path.exists(topics_file):
            return [], []
            
        df = pd.read_csv(topics_file)
        
        display_df = df[['title', 'author', 'replies', 'views', 'sentiment_label']].copy()
        
        columns = [
            {"name": "Title", "id": "title"},
            {"name": "Author", "id": "author"},
            {"name": "Replies", "id": "replies"},
            {"name": "Views", "id": "views"},
            {"name": "Sentiment", "id": "sentiment_label"}
        ]
        
        return display_df.to_dict('records'), columns
    except Exception as e:
        logger.error(f"Error creating trending topics table: {str(e)}")
        return [], []

def create_empty_figure(message):
    """Create an empty figure with a message."""
    fig = go.Figure()
    
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(50, 50, 50, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )
    
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16)
    )
    
    return fig

def main():
    app.run(debug=DASHBOARD_DEBUG, port=DASHBOARD_PORT)

if __name__ == "__main__":
    main() 