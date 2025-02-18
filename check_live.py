#!/usr/bin/env python
import requests
import re
import json
import os

# 設定你的 YouTube Data API key
API_KEY = os.environ.get("YOUTUBE_API_KEY", "YOUR_API_KEY")

# 要查詢的頻道名稱與對應 /streams 網址
CHANNELS = {
    "中天新聞CtiNews": "https://www.youtube.com/@中天新聞CtiNews/streams",
    "中天電視": "https://www.youtube.com/@中天電視CtiTv/streams",
    "TVBS": "https://www.youtube.com/@tvbschannel/streams",
    "ChopChopShow": "https://www.youtube.com/@chopchopshow/streams"
}

# 用來儲存直播結果
live_results = []

def extract_video_ids(data_obj, collected):
    """遞迴搜尋 JSON 物件中的 videoId"""
    if isinstance(data_obj, dict):
        if "videoId" in data_obj:
            collected.add(data_obj["videoId"])
        for value in data_obj.values():
            extract_video_ids(value, collected)
    elif isinstance(data_obj, list):
        for item in data_obj:
            extract_video_ids(item, collected)

def get_live_video_info(video_id):
    """利用 YouTube Data API 查詢影片是否為直播，同時取得影片標題"""
    api_url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "id": video_id,
        "part": "snippet,liveStreamingDetails",
        "key": API_KEY
    }
    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        print(f"Error fetching video {video_id}: HTTP {response.status_code}")
        return None

    data = response.json()
    if "items" in data and len(data["items"]) > 0:
        item = data["items"][0]
        # snippet.liveBroadcastContent 可為 "live", "none", "upcoming"
        if item["snippet"].get("liveBroadcastContent") == "live":
            return item
    return None

def process_channel(channel_name, url):
    print(f"處理頻道：{channel_name}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"取得 {url} 失敗，狀態碼：{resp.status_code}")
            return
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return

    html = resp.text
    # 嘗試抓取內嵌 JSON 資料 (ytInitialData)
    m = re.search(r"var ytInitialData = ({.*?});", html)
    if not m:
        print("找不到 ytInitialData")
        return

    try:
        data = json.loads(m.group(1))
    except Exception as e:
        print(f"JSON 解析錯誤: {e}")
        return

    # 取得頁面中所有 videoId
    video_ids = set()
    extract_video_ids(data, video_ids)

    # 檢查每支影片是否為直播
    for vid in video_ids:
        info = get_live_video_info(vid)
        if info:
            # 取得影片標題 (中文名稱)
            title = info["snippet"].get("title", "無標題")
            video_url = f"https://www.youtube.com/watch?v={vid}"
            # 輸出格式： 影片標題,影片網址
            live_results.append(f"{title},{video_url}")
            print(f"找到直播：{title} - {video_url}")

def main():
    for channel_name, url in CHANNELS.items():
        process_channel(channel_name, url)

    # 寫入結果到 live_streams.txt，若無直播則清空檔案內容
    with open("live_streams.txt", "w", encoding="utf-8") as f:
        for line in live_results:
            f.write(line + "\n")
    print("更新完成。")

if __name__ == "__main__":
    main()
