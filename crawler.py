import requests
from bs4 import BeautifulSoup

# 頻道列表
channels = [
    {"name": "中天新聞CtiNews", "url": "https://www.youtube.com/@中天新聞CtiNews/streams"},
    {"name": "TVBS頻道", "url": "https://www.youtube.com/@tvbschannel/streams"},
    {"name": "Chop Chop Show", "url": "https://www.youtube.com/@chopchopshow/streams"}
]

def check_live_stream(channel):
    try:
        response = requests.get(channel["url"])
        response.raise_for_status()
    except Exception as e:
        print(f"無法存取 {channel['name']} 的頁面: {e}")
        return False

    soup = BeautifulSoup(response.text, 'html.parser')
    # 簡單檢查頁面中是否包含 "LIVE" 的文字
    live_indicator = soup.find(string=lambda text: text and "LIVE" in text.upper())
    return live_indicator is not None

def main():
    live_streams = []
    for channel in channels:
        if check_live_stream(channel):
            live_streams.append(f"{channel['name']},{channel['url']}")
            print(f"{channel['name']} 正在直播")
        else:
            print(f"{channel['name']} 沒有直播")
    
    # 僅當有直播時才寫入檔案
    if live_streams:
        with open("live_streams.txt", "w", encoding="utf-8") as f:
            for stream in live_streams:
                f.write(stream + "\n")
    else:
        # 沒有直播則清空檔案
        open("live_streams.txt", "w", encoding="utf-8").close()

if __name__ == "__main__":
    main()
