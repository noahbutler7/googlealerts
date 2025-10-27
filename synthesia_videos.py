from config import SYNTHESIA_API_KEY
import requests
import time

def create_synthesia_video(headline, link):
    """Create a Synthesia video for a single headline and return its final URL."""
    url = "https://api.synthesia.io/v2/videos"
    script = f"{headline}. Read more at {link}."

    payload = {
        "title": f"AI News: {headline[:50]}",
        "visibility": "private",
        "input": [
            {
                "scriptText": script,
                "avatar": "Anna",  # Replace with your preferred avatar
                "voice": "en-US-Jenny",
                "background": "white"
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {SYNTHESIA_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 201:
        print("❌ Synthesia API error:", response.status_code, response.text)
        return None

    video_id = response.json()["id"]
    print(f"🎬 Created Synthesia video: {video_id}")

    # Wait for rendering to complete
    return wait_for_video_completion(video_id)


def wait_for_video_completion(video_id):
    """Poll the Synthesia API until the video is finished."""
    headers = {"Authorization": f"Bearer {SYNTHESIA_API_KEY}"}
    url = f"https://api.synthesia.io/v2/videos/{video_id}"

    print(f"⏳ Waiting for Synthesia video {video_id} to render...")
    for _ in range(60):  # wait up to ~10 minutes total (polling every 10s)
        response = requests.get(url, headers=headers)
        data = response.json()
        status = data.get("status")

        if status == "complete":
            video_url = data.get("download") or data.get("asset_url") or data.get("videoUrl")
            print(f"✅ Synthesia video ready: {video_url}")
            return video_url

        if status == "failed":
            print("❌ Synthesia video failed to render.")
            return None

        time.sleep(10)

    print("⚠️ Synthesia video timed out waiting for render.")
    return None



