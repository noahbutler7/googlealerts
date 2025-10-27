from gtts import gTTS
import os

def text_to_speech_from_articles(articles, filename="static/audio/daily_update.mp3"):
    """Convert all article headlines to a single spoken audio file."""

    if not articles:
        text = "No news found for your keyword today."
    else:
        # Build readable speech text with just the headlines
        text = "Here are the top headlines today.\n"
        for i, a in enumerate(articles, start=1):
            title = a.get("title", "").strip()
            if title:
                text += f"Headline {i}: {title}.\n"

    # Limit total length so gTTS doesn’t hang
    if len(text) > 4000:
        text = text[:4000] + " ...and more headlines available online."

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    try:
        print(f"🎙 Generating audio... ({len(text)} characters)")
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(filename)
        print(f"✅ Audio saved to {filename}")
        return filename
    except Exception as e:
        print("❌ Error generating TTS:", e)
        # Make a blank file as fallback
        with open(filename, "wb") as f:
            f.write(b"")
        return filename


