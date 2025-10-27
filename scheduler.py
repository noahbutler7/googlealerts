from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os

from google_alerts import fetch_google_alerts
from tts_utils import text_to_speech_from_articles
from rss_utils import update_rss_feed
from synthesia_videos import generate_synthesia_videos  # ✅ new import

def generate_daily_podcast():
    """Fetch headlines, generate audio, videos, and update podcast feed."""
    keyword = "AI"  # You can make this configurable
    print(f"[{datetime.now()}] 📰 Generating daily podcast for keyword: {keyword}")

    articles = fetch_google_alerts(keyword)
    if not articles:
        print("⚠️ No new articles today.")
        return

    # Save audio file with today's date
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"static/audio/{today}.mp3"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Generate podcast audio
    text_to_speech_from_articles(articles, filename)
    update_rss_feed(articles, filename, today)

    # ✅ Automatically create Synthesia videos
    print("🎬 Creating Synthesia videos for today's top headlines...")
    generate_synthesia_videos(articles)

    print("✅ Daily podcast and videos generated!")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_daily_podcast, "cron", hour=8, minute=0)  # 8:00 AM daily
    scheduler.start()
    print("🕒 Scheduler started — daily podcast + videos will auto-generate at 8 AM.")



