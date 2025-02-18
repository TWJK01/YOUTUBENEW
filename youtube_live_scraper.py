import requests
import json
import os
from datetime import datetime

# 設定 YouTube Data API Key
API_KEY = os.getenv("YOUTUBE_API_KEY")  # 可以在 GitHub Actions 設定環境變數
CHANNEL_IDS = {
    "中天新聞CtiNews": "UCpu3bemTQwAU8PqM4kJdoEQ",
    "TVBS": "UC5nwNW4KdC0SzrhF9BXEYOQ",
    "11點熱吵店": "UCnZDTHNQ77SqXOF-hKmLoXA"
}

# 文字檔存放路徑
OUTPUT_FILE = "live_streams.txt"


def get_live_streams():
    live_streams = []
    for name, channel_id in CHANNEL_IDS.items():
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&type=video&eventType=live&key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if "items" in data and len(data["items"]) > 0:
            video_id = data["items"][0]["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            live_streams.append(f"{name},{video_url}")

    return live_streams


def save_to_file(live_streams):
    if live_streams:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(live_streams) + "\n")
        print(f"{datetime.now()} - 已更新 {OUTPUT_FILE}")
    else:
        print(f"{datetime.now()} - 沒有正在直播的頻道")
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)  # 沒有直播時刪除檔案


def main():
    live_streams = get_live_streams()
    save_to_file(live_streams)


if __name__ == "__main__":
    main()
