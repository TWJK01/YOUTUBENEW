import requests
import time

# 設定要監控的 YouTube 頻道的 URL
channels = [
    ("中天新聞CtiNews", "https://www.youtube.com/@中天新聞CtiNews/streams"),
    ("TVBS", "https://www.youtube.com/@tvbschannel/streams"),
    ("ChopChopShow", "https://www.youtube.com/@chopchopshow/streams")
]

# 定義爬取並檢查直播狀態的函式
def check_live_status():
    live_streams = []
    for channel_name, channel_url in channels:
        response = requests.get(channel_url)
        if 'LIVE' in response.text or '直播中' in response.text:  # 檢查頁面中是否有直播標識
            live_streams.append(f'{channel_name},{channel_url}')
    return live_streams

# 保存有直播的資訊到文件
def save_to_file(live_streams):
    with open('live_streams.txt', 'w', encoding='utf-8') as file:
        for stream in live_streams:
            file.write(stream + '\n')

# 主程式
def main():
    while True:
        live_streams = check_live_status()
        save_to_file(live_streams)
        time.sleep(7200)  # 每兩小時更新一次

if __name__ == '__main__':
    main()
