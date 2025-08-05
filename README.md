# Stock Sentiment to ROI Tool - MVP

A Flask web application that analyzes the correlation between Reddit sentiment and stock price movements over the last 30 days.

## Features

- **Stock Analysis**: Enter any stock ticker to analyze sentiment correlation
- **Reddit Integration**: Analyzes posts from r/stocks and r/investing
- **Sentiment Analysis**: Uses VADER sentiment analyzer for natural language processing
- **Correlation Calculation**: Computes Pearson correlation between sentiment and price changes
- **Interactive Visualization**: Chart.js powered charts showing sentiment vs price movement
- **Real-time Analysis**: Processes data in memory for fast results

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Reddit API Setup (Required)
You need to create a Reddit application to access the Reddit API:

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Note down your `client_id` and `client_secret`

### 3. Set Environment Variables
Set the following environment variables with your Reddit API credentials:

**Windows (PowerShell):**
```powershell
$env:REDDIT_CLIENT_ID="your_client_id_here"
$env:REDDIT_CLIENT_SECRET="your_client_secret_here"
```

**Windows (Command Prompt):**
```cmd
set REDDIT_CLIENT_ID=your_client_id_here
set REDDIT_CLIENT_SECRET=your_client_secret_here
```

**Linux/Mac:**
```bash
export REDDIT_CLIENT_ID="your_client_id_here"
export REDDIT_CLIENT_SECRET="your_client_secret_here"
```

### 4. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## How to Use

1. **Enter Stock Ticker**: Type any valid stock ticker (e.g., AAPL, TSLA, MSFT)
2. **Click Analyze**: The app will fetch Reddit posts and stock data
3. **View Results**: See the correlation score and interactive chart
4. **Interpret Results**: 
   - Strong correlation: |r| ≥ 0.7
   - Moderate correlation: 0.3 ≤ |r| < 0.7
   - Weak correlation: 0.1 ≤ |r| < 0.3
   - No correlation: |r| < 0.1

## Technical Details

### Data Sources
- **Stock Data**: Yahoo Finance API (via yfinance)
- **Sentiment Data**: Reddit API (r/stocks and r/investing subreddits)

### Analysis Process
1. Validates stock ticker exists
2. Fetches 30 days of stock price data
3. Searches Reddit for posts mentioning the ticker
4. Analyzes sentiment using VADER (compound scores -1 to +1)
5. Calculates daily average sentiment scores
6. Computes Pearson correlation coefficient
7. Displays results with interactive visualization

### Requirements
- Minimum 20 Reddit posts required for analysis
- 30-day analysis window
- At least 5 overlapping data points for correlation

## Error Handling

The app handles various error scenarios:
- Invalid or non-existent stock tickers
- Insufficient Reddit data (< 20 posts)
- API rate limiting
- Network connectivity issues
- Data processing errors

## Limitations (MVP)

- Reddit data only (no Twitter, news, etc.)
- 30-day analysis period only
- No user accounts or data persistence
- Single stock analysis at a time
- No real-time updates
- Basic mobile optimization

## Future Enhancements

- Multiple data sources (Twitter, news articles)
- Historical analysis beyond 30 days
- User authentication and saved analyses
- Portfolio-level analysis
- Real-time sentiment tracking
- Advanced ML models
- Mobile app

## Architecture

```
Frontend: HTML/CSS/JavaScript + Chart.js
Backend: Python Flask
APIs: Reddit API + Yahoo Finance
NLP: VADER Sentiment Analysis (NLTK)
Database: None (in-memory processing)
```

## Performance

- Analysis typically completes in 10-30 seconds
- Designed for 1-5 concurrent users
- Memory-efficient processing
- No database overhead

## Troubleshooting

### Common Issues

1. **"Stock ticker not found"**
   - Ensure ticker is valid and traded on major exchanges
   - Try common tickers like AAPL, MSFT, GOOGL

2. **"Not enough social media data"**
   - Stock may not be frequently discussed on Reddit
   - Try more popular stocks with higher social media presence

3. **Reddit API errors**
   - Check your Reddit API credentials
   - Ensure environment variables are set correctly
   - Verify your Reddit app is configured as "script" type

4. **Service unavailable**
   - Check internet connection
   - APIs may be temporarily down
   - Try again in a few minutes

### Debug Mode
The app runs in debug mode by default for development. For production deployment, set `debug=False` in `app.py`.

## License

This project is for educational and research purposes. Please respect API rate limits and terms of service for Reddit and Yahoo Finance.
