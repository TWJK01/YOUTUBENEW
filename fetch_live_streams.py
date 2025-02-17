import requests
import os

API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNELS = {
    "中天新聞": "UCpu3bemTQwAU8PqM4kJdoEQ",   # 替換成中天新聞的頻道ID
    "TVBS": "UC5nwNW4KdC0SzrhF9BXEYOQ",          # 替換成TVBS的頻道ID
    "11點熱吵店": "UCnZDTHNQ77SqXOF-hKmLoXA"  # 替換成ChopChopShow的頻道ID
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
