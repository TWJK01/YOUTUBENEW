import os
import requests

# 從環境變數取得 API 金鑰（請在 GitHub Secrets 中設定 YOUTUBE_API_KEY）
API_KEY = os.environ.get("YOUTUBE_API_KEY")
if not API_KEY:
    raise Exception("請設定環境變數 YOUTUBE_API_KEY")

# 頻道名稱與對應的頻道 ID（請根據實際情況確認 channel id）
CHANNELS = {
    "中天新聞": "UC5l1Yto5oOIgRXlI4p4VKbw",
    "TVBS新聞": "UC5nwNW4KdC0SzrhF9BXEYOQ",
    "11點熱吵店": "UCnZDTHNQ77SqXOF-hKmLoXA"
}

BASE_URL = "https://www.googleapis.com/youtube/v3/search"
live_streams = []

for name, channel_id in CHANNELS.items():
    params = {
        'part': 'snippet',
        'channelId': channel_id,
        'type': 'video',
        'eventType': 'live',
        'key': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    for item in data.get("items", []):
        title = item["snippet"]["title"]
        # 判斷標題中是否包含「直播中」或「LIVE」(不區分大小寫)
        if "直播中" in title or "LIVE" in title.upper():
            video_id = item["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            # 以「中文名稱,網址」格式存入結果
            live_streams.append(f"{name},{video_url}")

# 若有符合條件的直播才寫入檔案，否則不更新檔案
if live_streams:
    with open("live_streams.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(live_streams))
    print("已更新 live_streams.txt")
else:
    print("目前無符合條件的直播，不更新檔案")
