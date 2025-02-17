import os
import requests

# 從環境變數取得 API 金鑰
API_KEY = os.environ.get("YOUTUBE_API_KEY")
if not API_KEY:
    raise Exception("請設定環境變數 YOUTUBE_API_KEY")

# 設定頻道名稱與對應的頻道 ID
CHANNELS = {
    '中天新聞CtiNews': 'UCpu3bemTQwAU8PqM4kJdoEQ',
    'tvbschannel': 'UCD2SNRlEjxJODlwaKx-BoRw',
    'chopchopshow': 'UCnZDTHNQ77SqXOF-hKmLoXA'
}

BASE_URL = 'https://www.googleapis.com/youtube/v3/search'
live_streams = []

for name, channel_id in CHANNELS.items():
    params = {
        'part': 'snippet',
        'channelId': channel_id,
        'eventType': 'live',
        'type': 'video',
        'key': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    # 若該頻道有正在直播的影片
    for item in data.get('items', []):
        video_id = item['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        live_streams.append(f"{name},{video_url}")

# 如果有直播，則寫入檔案；沒有則不更新檔案
if live_streams:
    with open("live_streams.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(live_streams))
    print("已更新 live_streams.txt")
else:
    print("目前無直播，不更新檔案")
