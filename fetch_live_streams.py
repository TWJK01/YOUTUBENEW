import requests
import os

# 從環境變數讀取 API 金鑰
API_KEY = os.environ.get("YOUTUBE_API_KEY")

# 請將下面頻道ID替換為實際的 YouTube 頻道 ID
CHANNELS = {
    "中天新聞": "UCpu3bemTQwAU8PqM4kJdoEQ",   # 替換成中天新聞的頻道ID
    "TVBS": "UC5nwNW4KdC0SzrhF9BXEYOQ",          # 替換成TVBS的頻道ID
    "11點熱吵店": "UCnZDTHNQ77SqXOF-hKmLoXA"  # 替換成ChopChopShow的頻道ID
}

OUTPUT_FILE = "live_streams.txt"

def get_live_stream(channel_id):
    url = (
        f"https://www.googleapis.com/youtube/v3/search?"
        f"part=snippet&channelId={channel_id}&eventType=live&type=video&key={API_KEY}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("items"):
            # 取得第一筆直播影片資訊，若需要處理多筆可擴展
            item = data["items"][0]
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            return title, f"https://www.youtube.com/watch?v={video_id}"
    return None, None

def main():
    live_entries = []
    for name, channel_id in CHANNELS.items():
        title, url = get_live_stream(channel_id)
        if title and url:
            # 格式：直播影片標題,影片網址
            live_entries.append(f"{title},{url}")
            print(f"{name} 直播中：{title} - {url}")
        else:
            print(f"{name} 無直播")
    
    # 若有直播資料則更新檔案，無則清空
    with open(OUTPUT_FILE, "w", encoding="utf8") as f:
        if live_entries:
            f.write("\n".join(live_entries))
        else:
            f.write("")

if __name__ == "__main__":
    main()
