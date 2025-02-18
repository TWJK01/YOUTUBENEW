import os
import requests

# 從環境變數取得 YouTube API 金鑰
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise Exception("請設定 YOUTUBE_API_KEY 環境變數！")

# 設定要查詢的頻道，請自行填入各頻道的 channelId
channels = [
    {"name": "中天新聞CtiNews", "channel_id": "UC5l1Yto5oOIgRXlI4p4VKbw"},
    {"name": "TVBS", "channel_id": "UC5nwNW4KdC0SzrhF9BXEYOQ"},
    {"name": "11點熱吵店", "channel_id": "UCnZDTHNQ77SqXOF-hKmLoXA"},
]

def get_live_stream(channel_id):
    """
    使用 YouTube Data API 查詢頻道目前正在直播的影片（若有）。
    """
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": channel_id,
        "eventType": "live",
        "type": "video",
        "key": YOUTUBE_API_KEY,
    }
    response = requests.get(search_url, params=params)
    if response.status_code != 200:
        print(f"Error fetching channel {channel_id}: {response.text}")
        return None

    data = response.json()
    items = data.get("items", [])
    if items:
        # 取得第一筆直播資料
        video = items[0]
        video_id = video["id"]["videoId"]
        video_title = video["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return {"title": video_title, "url": video_url}
    return None

def main():
    output_lines = []
    for channel in channels:
        live_info = get_live_stream(channel["channel_id"])
        if live_info:
            # 格式：頻道中文名稱,直播網址
            output_lines.append(f"{channel['name']},{live_info['url']}")
            print(f"找到 {channel['name']} 的直播：{live_info['url']}")
        else:
            print(f"{channel['name']} 沒有直播。")
    
    # 只有有直播時才寫入檔案 (若無則清空檔案)
    with open("live_streams.txt", "w", encoding="utf-8") as f:
        if output_lines:
            f.write("\n".join(output_lines))
        else:
            f.write("")

if __name__ == "__main__":
    main()
