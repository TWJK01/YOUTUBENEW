from googleapiclient.discovery import build
import datetime

# 設定 API 金鑰
api_key = 'YOUTUBE_API_KEY'

# 建立 YouTube API 客戶端
youtube = build('youtube', 'v3', developerKey=api_key)

# 指定要查詢的頻道 ID
channel_ids = ['UC5l1Yto5oOIgRXlI4p4VKbw', 'UC5nwNW4KdC0SzrhF9BXEYOQ', 'UCnZDTHNQ77SqXOF-hKmLoXA']

# 開啟文字檔以寫入直播資訊
with open('live_streams.txt', 'w', encoding='utf-8') as file:
    for channel_id in channel_ids:
        # 呼叫 API 獲取頻道的直播資訊
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            eventType='live',
            type='video',
            publishedAfter=(datetime.datetime.now() - datetime.timedelta(hours=2)).isoformat() + 'Z'
        )
        response = request.execute()

        # 檢查是否有直播
        if response['items']:
            for item in response['items']:
                title = item['snippet']['title']
                video_id = item['id']['videoId']
                url = f'https://www.youtube.com/watch?v={video_id}'
                file.write(f'{title},{url}\n')
