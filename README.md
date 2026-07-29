# Stock Sentiment vs. ROI Tool

A Flask web application that compares Reddit sentiment with a stock's price movement over the past 30 days. Given a stock ticker, the app collects Reddit discussions, analyzes sentiment using VADER, retrieves historical price data from Yahoo Finance, and calculates the correlation between the two.

## Tech Stack

- Python
- Flask
- VADER (NLTK)
- Chart.js
- yfinance
- Reddit API

## Running the Project

Clone the repository and install the dependencies.

```bash
pip install -r requirements.txt
```

### Reddit API Setup

Create a Reddit application:

1. Visit https://www.reddit.com/prefs/apps
2. Click **Create App**
3. Select **script**
4. Copy your `client_id` and `client_secret`

Set the environment variables.

**PowerShell**

```powershell
$env:REDDIT_CLIENT_ID="your_client_id"
$env:REDDIT_CLIENT_SECRET="your_client_secret"
```

**Command Prompt**

```cmd
set REDDIT_CLIENT_ID=your_client_id
set REDDIT_CLIENT_SECRET=your_client_secret
```

**Linux / macOS**

```bash
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
```

Start the application.

```bash
python app.py
```

Open:

```
http://localhost:5000
```

## How It Works

1. Enter a stock ticker.
2. The app downloads the last 30 days of stock prices.
3. Reddit posts mentioning the ticker are collected from **r/stocks** and **r/investing**.
4. VADER assigns a sentiment score to each post.
5. Daily sentiment is compared with daily stock returns using the Pearson correlation coefficient.
6. Results are displayed with an interactive Chart.js visualization.

## Data Sources

- Yahoo Finance (via `yfinance`)
- Reddit API
- VADER Sentiment Analyzer (NLTK)

## Project Structure

```
app.py              Flask application
templates/          HTML templates
static/             CSS and JavaScript
requirements.txt    Python dependencies
```

## Requirements

- Reddit API credentials
- At least 20 Reddit posts mentioning the ticker
- 30 days of historical stock data
- Minimum of 5 overlapping days for correlation

## Current Limitations

This is an MVP, so a few things are intentionally simple.

- Reddit is the only sentiment source.
- Only one stock can be analyzed at a time.
- Analysis is limited to a 30-day window.
- Results are processed in memory (no database).
- No user accounts or saved analyses.

## Common Issues

### Invalid ticker

Make sure the ticker exists and is listed on Yahoo Finance.

### Not enough Reddit data

Some stocks simply don't have enough discussion to calculate a meaningful correlation.

### Reddit API errors

Verify your API credentials and make sure your Reddit application is configured as a **script** application.

## Notes

Typical analysis takes around **10–30 seconds**, depending on Reddit API response time and the amount of available data.

This project was built as an exploration of whether online discussion and short-term market performance show measurable relationships. It is intended for educational purposes and should not be used as financial advice.
