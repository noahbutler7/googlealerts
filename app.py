from flask import Flask, render_template, request
from google_alerts import fetch_google_alerts
from tts_utils import text_to_speech_from_articles
from synthesia_videos import create_synthesia_video  # ✅ new import
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form.get('keywords', '').strip()

        if not keyword:
            return render_template("result.html", summary="<p>Please enter a keyword.</p>", audio_file=None, video_url=None)

        # Fetch Google News results
        articles = fetch_google_alerts(keyword)

        if not articles:
            summary_html = "<p>No Google Alerts results found for that keyword.</p>"
            audio_file = text_to_speech_from_articles([])
            video_url = None
        else:
            # Build readable summary for page
            summary_html = ""
            for a in articles:
                summary_html += f"<p><strong>{a['title']}</strong><br><a href='{a['link']}' target='_blank'>{a['link']}</a></p>\n"

            # Generate audio file
            audio_file = text_to_speech_from_articles(articles)

            # ✅ Create a Synthesia video from the top headline
            video_url = None
            first_article = articles[0]
            if first_article and first_article.get("title"):
                headline = first_article.get("title")
                link = first_article.get("link", "")
                print(f"🎬 Creating Synthesia video for: {headline}")
                video_url = create_synthesia_video(headline, link)
                print(f"✅ Synthesia video URL: {video_url}")

        # Render result page with audio + video
        return render_template("result.html", summary=summary_html, audio_file=audio_file, video_url=video_url)

    # Default GET route (renders form)
    return render_template("index.html")


if __name__ == '__main__':
    os.makedirs("static/audio", exist_ok=True)
    port = int(os.environ.get("PORT", 5000))  # ✅ use Render’s dynamic port
    app.run(host="0.0.0.0", port=port, debug=False)






