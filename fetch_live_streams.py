import requests
import os

API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNELS = {
    "中天新聞": "UCpu3bemTQwAU8PqM4kJdoEQ",   # 替換成中天新聞的頻道ID
    "TVBS": "UC5nwNW4KdC0SzrhF9BXEYOQ",          # 替換成TVBS的頻道ID
    "11點熱吵店": "UCnZDTHNQ77SqXOF-hKmLoXA"  # 替換成ChopChopShow的頻道ID
}

def get_live_streams(channel_id):
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&eventType=live&type=video&key={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]  # 返回第一个直播视频的信息
    return None

def main():
    live_streams = []
    for name, channel_id in CHANNELS.items():
        stream = get_live_streams(channel_id)
        if stream:
            title = stream['snippet']['title']
            video_id = stream['id']['videoId']
            url = f'https://www.youtube.com/watch?v={video_id}'
            live_streams.append(f'{name},{url}')
    
    if live_streams:
        with open('live_streams.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(live_streams))

if __name__ == '__main__':
    main()
