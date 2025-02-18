#!/usr/bin/env python
import requests
import re
import json
import os

# 設定你的 YouTube Data API key
API_KEY = os.environ.get("YOUTUBE_API_KEY", "YOUR_API_KEY")

# 要查詢的頻道名稱與對應 /streams 網址
CHANNELS = {
    "台視新聞": "https://www.youtube.com/@TTV_NEWS/streams",
    "中視新聞": "https://www.youtube.com/@chinatvnews/streams",
    "中視新聞 HD": "https://www.youtube.com/@twctvnews/streams",
    "華視新聞": "https://www.youtube.com/@CtsTw/streams",
    "民視新聞網": "https://www.youtube.com/@FTV_News/streams",
    "公視": "https://www.youtube.com/@ptslivestream/streams",
    "公視新聞網": "https://www.youtube.com/@PNNPTS/streams",
    "公視台語台": "https://www.youtube.com/@ptstaigitai/streams",
    "大愛電視": "https://www.youtube.com/@DaAiVideo/streams",
    "鏡新聞": "https://www.youtube.com/@mnews-tw/streams",
    "東森新聞": "https://www.youtube.com/@newsebc/streams",
    "三立iNEWS": "https://www.youtube.com/@setinews/streams",
    "三立LIVE新聞": "https://www.youtube.com/@setnews/streams",
    "中天新聞CtiNews": "https://www.youtube.com/@中天新聞CtiNews/streams",
    "中天電視CtiTv": "https://www.youtube.com/@中天電視CtiTv/streams",
    "TVBS NEWS": "https://www.youtube.com/@TVBSNEWS01/streams",
    "寰宇新聞": "https://www.youtube.com/@globalnewstw/streams",
    "新唐人亞太電視台": "https://www.youtube.com/@NTDAPTV/streams",
    "TVBS 優選頻道": "https://www.youtube.com/@tvbschannel/streams",
    "少康戰情室": "https://www.youtube.com/@tvbssituationroom/streams",
    "文茜的世界周報": "https://www.youtube.com/@tvbssisysworldnews/streams",
    "民視讚夯": "https://www.youtube.com/@FTV_Forum/streams",
    "寰宇財經新聞": "https://www.youtube.com/@globalmoneytv/streams",
    "台視時光機": "https://www.youtube.com/@TTVClassic/streams",
    "中視經典戲劇": "https://www.youtube.com/@ctvdrama_classic/streams",
    "中視經典綜藝": "https://www.youtube.com/@ctvent_classic/streams",
    "華視戲劇頻道": "https://www.youtube.com/@cts_drama/streams",
    "華視綜藝頻道": "https://www.youtube.com/@CTSSHOW/streams",
    "民視戲劇館": "https://www.youtube.com/@FTVDRAMA/streams",
    "三立華劇 SET Drama": "https://www.youtube.com/@SETdrama/streams",
    "TVBS劇在一起": "https://www.youtube.com/@tvbsdrama/streams",
    "11點熱吵店": "https://www.youtube.com/@chopchopshow/streams",
    "國會頻道": "https://www.youtube.com/@parliamentarytv/streams"
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
