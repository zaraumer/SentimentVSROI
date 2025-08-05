from flask import Flask, render_template, request, jsonify
import yfinance as yf
import praw
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from scipy.stats import pearsonr
import re
import os
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv()

# Download VADER lexicon if not already present
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

app = Flask(__name__)

class StockSentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        print(self.sia)
        # Reddit API credentials (you'll need to set these up)
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
         
    
    def validate_ticker(self, ticker):
        """Validate if ticker exists in Yahoo Finance by checking for historical data"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            return not hist.empty
        except Exception as e:
            print(f"Ticker validation error: {e}")
            return False
    
    def get_stock_data(self, ticker, days=30):
        """Get stock price data for the last N days"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)
            
            if hist.empty:
                return None
            
            # Calculate daily percentage change
            hist['pct_change'] = hist['Close'].pct_change() * 100
            hist['date'] = hist.index.strftime('%Y-%m-%d')
            
            return hist[['Close', 'pct_change', 'date']].dropna()
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return None
    
    def get_reddit_posts(self, ticker, days=30):
        """Get Reddit posts mentioning the ticker from r/stocks and r/investing"""
        try:
            posts = []
            subreddits = ['stocks', 'investing']
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            start_timestamp = start_date.timestamp()
            
            for subreddit_name in subreddits:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Search for posts mentioning the ticker
                for post in subreddit.search(ticker, time_filter='month', limit=100):
                    if post.created_utc >= start_timestamp:
                        # Check if ticker is actually mentioned in title or text
                        text_content = f"{post.title} {post.selftext}".lower()
                        if re.search(rf'\b{ticker.lower()}\b', text_content):
                            posts.append({
                                'title': post.title,
                                'text': post.selftext,
                                'created_utc': post.created_utc,
                                'score': post.score,
                                'date': datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d')
                            })
            
            return posts
        except Exception as e:
            print(f"Error fetching Reddit posts: {e}")
            return []
    
    def analyze_sentiment(self, posts):
        """Analyze sentiment of Reddit posts using VADER"""
        daily_sentiments = defaultdict(list)
        
        for post in posts:
            text = f"{post['title']} {post['text']}"
            sentiment_score = self.sia.polarity_scores(text)
            
            # Use compound score (-1 to 1)
            compound_score = sentiment_score['compound']
            daily_sentiments[post['date']].append(compound_score)
        
        # Calculate daily average sentiment
        daily_avg_sentiment = {}
        for date, scores in daily_sentiments.items():
            daily_avg_sentiment[date] = np.mean(scores)
        
        return daily_avg_sentiment
    
    def calculate_correlation(self, stock_data, sentiment_data):
        """Calculate correlation between sentiment and stock price changes"""
        try:
            # Merge data by date
            merged_data = []
            
            for _, row in stock_data.iterrows():
                date = row['date']
                if date in sentiment_data:
                    merged_data.append({
                        'date': date,
                        'price_change': row['pct_change'],
                        'sentiment': sentiment_data[date]
                    })
            
            if len(merged_data) < 5:  # Need at least 5 data points
                return None, None
            
            df = pd.DataFrame(merged_data)
            correlation, p_value = pearsonr(df['sentiment'], df['price_change'])
            
            return correlation, df
        except Exception as e:
            print(f"Error calculating correlation: {e}")
            return None, None
    
    def interpret_correlation(self, correlation):
        """Interpret correlation strength"""
        if correlation is None:
            return "No correlation data available"
        
        abs_corr = abs(correlation)
        if abs_corr >= 0.7:
            return "Strong correlation"
        elif abs_corr >= 0.3:
            return "Moderate correlation"
        elif abs_corr >= 0.1:
            return "Weak correlation"
        else:
            return "No significant correlation"

analyzer = StockSentimentAnalyzer()
print(analyzer.reddit)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        ticker = request.json.get('ticker', '').upper().strip()
        
        if not ticker:
            return jsonify({'error': 'Please enter a stock ticker'}), 400
        
        # Validate ticker
        if not analyzer.validate_ticker(ticker):
            return jsonify({'error': 'Stock ticker not found'}), 400
        
        # Get stock data
        stock_data = analyzer.get_stock_data(ticker)
        if stock_data is None or len(stock_data) < 10:
            return jsonify({'error': 'Insufficient stock price data'}), 400
        
        # Get Reddit posts
        reddit_posts = analyzer.get_reddit_posts(ticker)
        if len(reddit_posts) < 20:
            return jsonify({'error': 'Not enough social media data (minimum 20 posts required)'}), 400
        
        # Analyze sentiment
        sentiment_data = analyzer.analyze_sentiment(reddit_posts)
        if not sentiment_data:
            return jsonify({'error': 'Unable to analyze sentiment data'}), 400
        
        # Calculate correlation
        correlation, merged_df = analyzer.calculate_correlation(stock_data, sentiment_data)
        if correlation is None:
            return jsonify({'error': 'Unable to calculate correlation'}), 400
        
        # Prepare chart data
        chart_data = {
            'dates': merged_df['date'].tolist(),
            'sentiment': merged_df['sentiment'].tolist(),
            'price_change': merged_df['price_change'].tolist()
        }
        
        # Prepare response
        result = {
            'ticker': ticker,
            'correlation': round(correlation, 3),
            'correlation_text': analyzer.interpret_correlation(correlation),
            'posts_analyzed': len(reddit_posts),
            'data_points': len(merged_df),
            'chart_data': chart_data
        }
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Analysis error: {e}")
        return jsonify({'error': 'Service unavailable, please try again'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
