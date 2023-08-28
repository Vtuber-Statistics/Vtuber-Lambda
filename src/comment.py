import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv(verbose=True)

api_service_name = "youtube"
api_version = "v3"
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# YouTube Data API v3 클라이언트 빌드
youtube = build(api_service_name, api_version, developerKey=YOUTUBE_API_KEY)

# 영상 ID를 통해 댓글 검색
video_id = "2SGrrdQWDxA"
response = (
    youtube.commentThreads()
    .list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        order="time",
        maxResults=10,
    )
    .execute()
)

for item in response.get("items", []):
    comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
    time = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
    print(f"댓글: {comment}:")
    print(f"시간: {time}:")
