import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pytchat

load_dotenv(verbose=True)

api_service_name = "youtube"
api_version = "v3"
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# YouTube Data API v3 클라이언트 빌드
youtube = build(api_service_name, api_version, developerKey=YOUTUBE_API_KEY)

# 채널 ID를 기반으로 채널 정보를 가져옵니다.
channel_id = "UCCzUftO8KOVkV4wQG1vkUvg"
# search_response = (
#     youtube.search()
#     .list(
#         part="snippet",
#         channelId=channel_id,
#         eventType="completed",
#         type="video",
#         order="date",
#         maxResults=1,
#     )
#     .execute()
# )
# video_info = search_response["items"]
# video_ids = [
#     item["id"]["videoId"]
#     for item in video_info
#     if "id" in item and "videoId" in item["id"]
# ]
# video_id = video_ids[0]
video_id = "oxZk5n-eoaQ"

chat = pytchat.create(video_id=video_id)
while chat.is_alive():
    for c in chat.get().items:
        print(c.author.isChatSponsor)
        print(c.author.name)
        print(c.author.type)
        print(c.timestamp)
        print(c.elapsedTime)
        print(c.datetime)
        print(c.message)
        print(c.amountValue)
        print(c.currency)

        exit()
