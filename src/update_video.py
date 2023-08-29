from model import Channel, Video
from utils import get_youtube_data_api, get_session
from sqlalchemy.sql import func


# 버튜버 채널 정보 업데이트
def update_video():
    channel_id_info = get_all_channel_id_info()
    for channel_id, youtube_api_channel_id in channel_id_info:
        live_video_infos = get_youtube_live_video_infos(
            channel_id, youtube_api_channel_id
        )

        print(live_video_infos)
        print(len(live_video_infos))

        return


# 모든 채널 정보(채널 ID, 유튜브 채널 ID) 반환
def get_all_channel_id_info():
    try:
        session = get_session()
        channel_id_info = (
            session.query(Channel)
            .with_entities(Channel.id, Channel.youtube_api_channel_id)
            .all()
        )

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        session.close()

    return channel_id_info


# channel_id와 매칭되는 채널의 마지막 방송 시간을 반환
def get_last_video_published_time(channel_id):
    try:
        session = get_session()
        last_video_published_time = (
            session.query(func.max(Video.created_at))
            .filter(Video.channel_id == channel_id)
            .scalar()
        )

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        session.close()

    return (
        "2000-01-01T00:00:00Z"
        if last_video_published_time is None
        else last_video_published_time
    )


# 영상 정보 추출
def get_filtered_video_info(video_info):
    youtube_api_video_id = video_info["id"]["videoId"]
    snippet = video_info["snippet"]
    filtered_video_info = {
        "title": snippet["title"],
        "video_url": snippet["title"],
        "thumbnail_url": snippet["thumbnails"]["high"],
        "created_at": snippet["publishTime"],
        "youtube_api_video_id": youtube_api_video_id,
    }

    return filtered_video_info


# 유튜브 채널 ID와 시간 기준으로 유튜브 비디오들의 정보를 반환
def get_youtube_live_video_infos(channel_id, youtube_channel_id):
    youtube_data_api = get_youtube_data_api()

    last_video_published_time = get_last_video_published_time(channel_id)
    print(last_video_published_time)

    video_infos = []
    next_page_token = None

    # youtube data api v3가 최대 50개의 데이터만 반환하기에 모든 데이터가
    # 반환될 때 까지 요청을 진행함
    # -> next_page_token의 존재 여부로 확인 가능
    while True:
        search_response = (
            youtube_data_api.search()
            .list(
                part="snippet",
                channelId=youtube_channel_id,
                eventType="completed",
                type="video",
                order="date",
                publishedAfter=last_video_published_time,
                # publishedAfter="2023-08-27T14:17:06Z",
                maxResults=50,
                pageToken=next_page_token,
            )
            .execute()
        )
        video_infos.extend(search_response["items"])

        next_page_token = search_response.get("nextPageToken")
        if not next_page_token:
            break

    filtered_video_infos = [
        get_filtered_video_info(video_info) for video_info in video_infos
    ]

    return filtered_video_infos


# 유튜브 채널 ID로 채 검색
# def get_youtube_channel_data(vtuber_name, youtube_api_channel_id):
#     youtube_data_api = get_youtube_data_api()

#     channel_response = (
#         youtube_data_api.channels()
#         .list(id=youtube_api_channel_id, part="snippet,statistics", maxResults=1)
#         .execute()
#     )
#     channel_info = channel_response["items"][0]["snippet"]
#     channel_statistics = channel_response["items"][0]["statistics"]

#     channel_data = {
#         "vtuber_name": vtuber_name,
#         "group": "hololive",  # 추후 수정
#         "country": channel_info["country"],
#         "channel_name": channel_info["title"],
#         "custom_url": channel_info["customUrl"],
#         "thumbnail_url": channel_info["thumbnails"]["medium"]["url"],
#         "created_at": channel_info["publishedAt"],
#         "subscriber_count": channel_statistics["subscriberCount"],
#         "total_view_count": channel_statistics["viewCount"],
#         "video_count": channel_statistics["videoCount"],
#         "youtube_api_channel_id": youtube_api_channel_id,
#     }
#     return channel_data
