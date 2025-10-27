import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

def fetch_google_alerts(keyword):
    """Fetch public Google News RSS for a keyword (acts like Google Alerts)."""
    keyword_encoded = quote_plus(keyword)
    url = f"https://news.google.com/rss/search?q={keyword_encoded}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error fetching Google Alerts feed:", e)
        return []

    try:
        root = ET.fromstring(response.content)
        items = []
        for item in root.findall(".//item"):
            title = item.findtext("title")
            link = item.findtext("link")
            items.append({"title": title, "link": link})
        return items
    except ET.ParseError as e:
        print("Error parsing XML:", e)
        return []



