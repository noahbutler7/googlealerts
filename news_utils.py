import requests

def get_news_summary(keywords):
    """Fetch headlines from NewsAPI or another source."""
    # Replace with your NewsAPI key
    API_KEY = "YOUR_NEWSAPI_KEY"
    query = '+'.join(keywords.split(','))
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize=5&apiKey={API_KEY}"

    response = requests.get(url).json()

    if 'articles' not in response:
        return "No news found for the provided keywords."

    articles = response['articles']
    summary = ""
    for article in articles:
        summary += f"- {article['title']}\n"

    return summary



