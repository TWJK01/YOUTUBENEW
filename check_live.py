#!/usr/bin/env python
import requests
import re
import json
import os

# 設定你的 YouTube Data API key
API_KEY = os.environ.get("YOUTUBE_API_KEY", "YOUR_API_KEY")

# 要查詢的頻道名稱與對應 /streams 網址
CHANNELS = {
    "台灣地震監視": "https://www.youtube.com/@台灣地震監視/streams",
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
    "中天亞洲台": "https://www.youtube.com/@中天亞洲台CtiAsia/streams",
    "CTI+ | 中天2台": "https://www.youtube.com/@中天2台ctiplusnews/streams",	
    "TVBS NEWS": "https://www.youtube.com/@TVBSNEWS01/streams",
    "寰宇新聞": "https://www.youtube.com/@globalnewstw/streams",
    "新唐人亞太電視台": "https://www.youtube.com/@NTDAPTV/streams",
    "中天財經頻道": "https://www.youtube.com/@中天財經頻道CtiFinance/streams",	
    "東森財經股市": "https://www.youtube.com/@57ETFN/streams",	
    "寰宇財經新聞": "https://www.youtube.com/@globalmoneytv/streams",
    "非凡電視": "https://www.youtube.com/@ustv/streams",
    "非凡商業台": "https://www.youtube.com/@ustvbiz/streams",	
    "運通財經台": "https://www.youtube.com/@EFTV01/streams",
    "全球財經台2": "https://www.youtube.com/@全球財經台2/streams",	
    "AI主播倪珍Nikki 播新聞": "https://www.youtube.com/@NOWnews-sp2di/streams",
    "POP Radio聯播網": "https://www.youtube.com/@917POPRadio/streams",	
    "鳳凰衛視PhoenixTV": "https://www.youtube.com/@phoenixtvhk/streams",
    "鳳凰資訊 PhoenixTVNews": "https://www.youtube.com/@phoenixtvnews7060/streams",	
    "CCTV中文": "https://www.youtube.com/@LiveNow24H/streams",
    "MIT台灣誌": "https://www.youtube.com/@ctvmit/streams",
    "大陸尋奇": "https://www.youtube.com/@ctvchinatv/streams",	
    "八大電視娛樂百分百": "https://www.youtube.com/@GTV100ENTERTAINMENT/streams",
    "中視經典綜藝": "https://www.youtube.com/@ctvent_classic/streams",
    "華視綜藝頻道": "https://www.youtube.com/@CTSSHOW/streams",
    "綜藝大熱門": "https://www.youtube.com/@HotDoorNight/streams",
    "綜藝玩很大": "https://www.youtube.com/@Mr.Player/streams",	
    "11點熱吵店": "https://www.youtube.com/@chopchopshow/streams",
    "飢餓遊戲": "https://www.youtube.com/@HungerGames123/streams",	
    "豬哥會社": "https://www.youtube.com/@FTV_ZhuGeClub/streams",	
    "東森綜合台": "https://www.youtube.com/@中天娛樂CtiEntertainment/streams",
    "中天娛樂頻道": "https://www.youtube.com/@ettv32/streams",	
    "WeTV 綜藝經典": "https://www.youtube.com/@WeTV-ClassicVariety/streams",	
    "57怪奇物語": "https://www.youtube.com/@57StrangerThings/streams",
    "台灣啟示錄": "https://www.youtube.com/@ebcapocalypse/streams",
    "非凡大探索": "https://www.youtube.com/@ustvfoody/streams",
    "BIF相信未來 官方頻道": "https://www.youtube.com/@BelieveinfutureTV/streams",	
    "少康戰情室": "https://www.youtube.com/@tvbssituationroom/streams",
    "文茜的世界周報": "https://www.youtube.com/@tvbssisysworldnews/streams",    
    "台視時光機": "https://www.youtube.com/@TTVClassic/streams",
    "中視經典戲劇": "https://www.youtube.com/@ctvdrama_classic/streams",
    "華視戲劇頻道": "https://www.youtube.com/@cts_drama/streams",
    "民視戲劇館": "https://www.youtube.com/@FTVDRAMA/streams",
    "三立電視 SET TV": "https://www.youtube.com/@SETTV/streams",
    "三立華劇 SET Drama": "https://www.youtube.com/@SETdrama/streams",
    "終極系列": "https://www.youtube.com/@KOONERETURN/streams",
    "TVBS劇在一起": "https://www.youtube.com/@tvbsdrama/streams",
    "TVBS戲劇-女兵日記 女力報到": "https://www.youtube.com/@tvbs-1587/streams",	
    "八大劇樂部": "https://www.youtube.com/@gtv-drama/streams",
    "龍華電視": "https://www.youtube.com/@ltv_tw/streams",	
    "愛爾達綜合台": "https://www.youtube.com/@ELTAWORLD/streams",
    "百纳经典独播剧场": "https://www.youtube.com/@BainationTVSeriesOfficial/streams",	
    "芒果TV青春剧场": "https://www.youtube.com/@MangoTVDramaOfficial/streams",		
    "CCTV电视剧": "https://www.youtube.com/@CCTVDrama/streams",	
    "SMG上海电视台官方频道": "https://www.youtube.com/@SMG-Official/streams",
    "SMG上海东方卫视欢乐频道": "https://www.youtube.com/@SMG-Comedy/streams",
    "中国东方卫视官方频道": "https://www.youtube.com/@SMGDragonTV/streams",	
    "TVBS 優選頻道": "https://www.youtube.com/@tvbschannel/streams",
    "壹電視NEXT TV": "https://www.youtube.com/@%E5%A3%B9%E9%9B%BB%E8%A6%96NEXTTV/streams",
    "民視讚夯": "https://www.youtube.com/@FTV_Forum/streams",
    "94要客訴": "https://www.youtube.com/@94politics/streams",	
    "大新聞大爆卦": "https://www.youtube.com/@大新聞大爆卦HotNewsTalk/streams",	
    "新聞大白話": "https://www.youtube.com/@tvbstalk/streams",	
    "中時新聞網": "https://www.youtube.com/@ChinaTimes/streams",
    "前進新台灣": "https://www.youtube.com/@SETTaiwanGo/streams",	
    "YOYOTV": "https://www.youtube.com/@yoyotvebc/streams",	
    "momokids親子台": "https://www.youtube.com/@momokidsYT/streams",
    "Bebefinn 繁體中文 - 兒歌": "https://www.youtube.com/@Bebefinn繁體中文/streams",
    "寶貝多米-兒歌童謠-卡通動畫-經典故事": "https://www.youtube.com/@Domikids_CN/streams",
    "會說話的湯姆貓家族": "https://www.youtube.com/@TalkingFriendsCN/streams",	
    "碰碰狐 鯊魚寶寶": "https://www.youtube.com/@Pinkfong繁體中文/streams",
    "碰碰狐 Pinkfong Baby Shark 儿歌·故事": "https://www.youtube.com/@Pinkfong简体中文/streams",	
    "寶寶巴士": "https://www.youtube.com/@BabyBusTC/streams",
    "Miliki Family - 繁體中文 - 兒歌": "https://www.youtube.com/@MilikiFamily_Chinese/streams",	
    "貝樂虎-幼兒動畫-早教启蒙": "https://www.youtube.com/@BarryTiger_Education_CN/streams",	
    "貝樂虎兒歌-童謠歌曲": "https://www.youtube.com/@barrytiger_kidssongs/streams",
    "貝樂虎-兒歌童謠-卡通動畫-經典故事": "https://www.youtube.com/@barrytiger_zh/streams",
    "小猪佩奇": "https://www.youtube.com/@PeppaPigChineseOfficial/streams",
    "神奇鸡仔": "https://www.youtube.com/@como_cn/streams",
    "朱妮托尼 - 动画儿歌": "https://www.youtube.com/@JunyTonyCN/streams",	
    "Muse木棉花-TW": "https://www.youtube.com/@MuseTW/streams",
    "Muse木棉花-闔家歡": "https://www.youtube.com/@Muse_Family/streams",
    "回歸線娛樂": "https://www.youtube.com/@tropicsanime/streams",
    "緯來體育台": "https://www.youtube.com/@vlsports/streams",
    "HOP Sports": "https://www.youtube.com/@HOPSports/streams",
    "DAZN 台灣": "https://www.youtube.com/@DAZNTaiwan/streams",	
    "動滋Sports": "https://www.youtube.com/@Sport_sa_taiwan/streams",
    "WWE": "https://www.youtube.com/@WWE/streams",
    "momo購物一台": "https://www.youtube.com/@momoch4812/streams",
    "momo購物二台": "https://www.youtube.com/@momoch3571/streams",
    "ViVa TV美好家庭購物": "https://www.youtube.com/@ViVaTVtw/streams",	
    "Live東森購物台": "https://www.youtube.com/@HotsaleTV/streams",		
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
