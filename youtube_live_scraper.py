import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from googleapiclient.discovery import build

# 設定 YouTube Data API Key
YOUTUBE_API_KEY = "你的 YouTube Data API Key"
CHANNELS = [
    "中天新聞CtiNews",  # 請填入 @ 頻道名稱
    "tvbschannel",
    "chopchopshow"
]

def get_driver():
    """初始化 Selenium WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 無頭模式
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_live_videos(channel_name):
    """使用 YouTube Data API 查詢頻道的直播影片"""
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet",
        channelId=get_channel_id(channel_name),
        eventType="live",
        type="video"
    )
    response = request.execute()

    live_streams = []
    for item in response.get("items", []):
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        live_streams.append(f"{title},{url}")

    return live_streams

def get_channel_id(channel_name):
    """根據 @頻道名稱 取得頻道 ID"""
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet",
        q=channel_name,
        type="channel"
    )
    response = request.execute()
    
    for item in response.get("items", []):
        return item["id"]["channelId"]
    return None

def scrape_live_streams(channel_name):
    """使用 Selenium 爬取 @頻道名稱/streams 頁面的直播影片"""
    driver = get_driver()
    url = f"https://www.youtube.com/@{channel_name}/streams"
    driver.get(url)
    time.sleep(5)  # 等待載入
    
    live_streams = []
    elements = driver.find_elements("xpath", '//a[@id="video-title"]')
    
    for element in elements:
        title = element.get_attribute("title")
        link = element.get_attribute("href")
        if "LIVE" in title or "直播" in title:  # 確保是直播
            live_streams.append(f"{title},{link}")

    driver.quit()
    return live_streams

def save_to_file(live_streams):
    """儲存直播網址到 live_streams.txt"""
    if live_streams:
        with open("live_streams.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(live_streams) + "\n")
        print("✅ 已更新 live_streams.txt")
    else:
        print("⚠️ 沒有正在直播的頻道，清空檔案")
        with open("live_streams.txt", "w", encoding="utf-8") as f:
            f.write("")

def main():
    all_live_streams = []
    
    for channel in CHANNELS:
        print(f"📡 正在抓取 {channel} 的直播...")
        api_results = get_live_videos(channel)
        scrape_results = scrape_live_streams(channel)
        all_live_streams.extend(api_results + scrape_results)
    
    save_to_file(all_live_streams)

if __name__ == "__main__":
    main()
