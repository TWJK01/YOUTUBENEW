import requests
import os

API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNELS = {
    "中天新聞": "UCyR8daX6qjgO5tzZuhb6Ikg",
    "TVBS": "UCmH3X9pDS66aRupq1Df7LBQ",
    "ChopChopShow": "UCqM3TqkQ7N1wzWm8o5W8rWg"
}

OUTPUT_FILE = "live_streams.txt"

def get_live_streams(channel_id):
    url = (
        f"https://www.googleapis.com/youtube/v3/search?"
        f"part=snippet&channelId={channel_id}&eventType=live&type=video&key={API_KEY}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data and data["items"]:
            item = data["items"][0]
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            return title, f"https://www.youtube.com/watch?v={video_id}"
    return None, None

def main():
    live_entries = []
    for name, channel_id in CHANNELS.items():
        title, url = get_live_streams(channel_id)
        if title and url:
            live_entries.append(f"{name},{url}")
            print(f"Found live stream for {name}: {title} - {url}")
        else:
            print(f"No live stream for {name}")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        if live_entries:
            f.write("\n".join(live_entries))
        else:
            f.write("")

if __name__ == "__main__":
    main()
