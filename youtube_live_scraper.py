import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# 設定 YouTube Data API Key
API_KEY = os.getenv("YOUTUBE_API_KEY")  # GitHub Actions 環境變數
CHANNEL_URLS = {
    "中天新聞CtiNews": "https://www.youtube.com/@中天新聞CtiNews/streams",
    "TVBS": "https://www.youtube.com/@tvbschannel/streams",
    "ChopChopShow": "https://www.youtube.com/@chopchopshow/streams"
}

# 文字檔存放路徑
OUTPUT_FILE = "live_streams.txt"


def get_live_streams_selenium():
    """使用 Selenium 爬取 YouTube 頻道的直播連結"""
    options = Options()
    options.add_argument("--headless")  # 無頭模式，避免開啟瀏覽器
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    live_streams = []
    for name, url in CHANNEL_URLS.items():
        driver.get(url)
        time.sleep(3)  # 等待頁面加載

        soup = BeautifulSoup(driver.page_source, "html.parser")
        videos = soup.select("a#video-title[href*='watch']")  # 抓取所有影片連結
        
        for video in videos:
            video_url = "https://www.youtube.com" + video["href"]
            live_streams.append(f"{name},{video_url}")

    driver.quit()
    return live_streams


def save_to_file(live_streams):
    """儲存直播網址到文件"""
    if live_streams:
        with open("live_streams.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(live_streams) + "\n")
        print("已更新 live_streams.txt")
    else:
        print("沒有正在直播的頻道，建立空白檔案")
        with open("live_streams.txt", "w", encoding="utf-8") as f:


def main():
    live_streams = get_live_streams_selenium()
    save_to_file(live_streams)


if __name__ == "__main__":
    main()




