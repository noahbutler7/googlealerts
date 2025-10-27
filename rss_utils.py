import os
from xml.etree import ElementTree as ET

RSS_FILE = "static/podcast_feed.xml"
BASE_URL = "http://127.0.0.1:5000/static/audio"  # change to your domain when hosted

def update_rss_feed(articles, audio_path, date):
    """Append a new item to the podcast RSS feed."""
    if not os.path.exists(RSS_FILE):
        # create base structure
        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")
        ET.SubElement(channel, "title").text = "Daily AI News Podcast"
        ET.SubElement(channel, "link").text = BASE_URL
        ET.SubElement(channel, "description").text = "Automated AI news read daily."
    else:
        rss = ET.parse(RSS_FILE).getroot()
        channel = rss.find("channel")

    # create new item
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = f"AI News for {date}"
    ET.SubElement(item, "description").text = "Automatically generated daily podcast from Google News."
    ET.SubElement(item, "pubDate").text = date
    ET.SubElement(item, "enclosure", url=f"{BASE_URL}/{os.path.basename(audio_path)}", type="audio/mpeg")

    ET.ElementTree(rss).write(RSS_FILE, encoding="utf-8", xml_declaration=True)
    print(f"📡 RSS updated: {RSS_FILE}")

