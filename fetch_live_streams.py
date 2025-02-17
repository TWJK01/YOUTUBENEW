import requests
import time

API_KEY = '您的API金鑰'
CHANNEL_IDS = {
    '中天新聞': 'UCpu3bemTQwAU8PqM4kJdoEQ',
    'TVBS新聞': 'UCL0_NxCvkcXwZHpvqgMZY-A',
    '11點熱吵店': 'UCnZDTHNQ77SqXOF-hKmLoXA'  # 請替換為實際的頻道ID
}
OUTPUT_FILE = 'live_streams.txt'
CHECK_INTERVAL = 2 * 60 * 60  # 兩小時（以秒為單位）

def get_live_streams():
    live_streams = []
    for name, channel_id in CHANNEL_IDS.items():
        url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&type=video&eventType=live&key={API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'items' in data:
                for item in data['items']:
                    title = item['snippet']['title']
                    video_id = item['id']['videoId']
                    video_url = f'https://www.youtube.com/watch?v={video_id}'
                    live_streams.append(f'{title},{video_url}')
        else:
            print(f'Failed to fetch data for channel: {name}')
    return live_streams

while True:
    live_streams = get_live_streams()
    if live_streams:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(live_streams))
    time.sleep(CHECK_INTERVAL)
