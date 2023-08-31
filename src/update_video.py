from model import Channel, Video
from utils import get_youtube_data_api, get_session, get_formatted_datetime
from sqlalchemy.sql import func


# 버튜버 채널 정보 업데이트
def insert_all_live_video():
    channel_id_info = get_all_channel_id_info()
    for channel_id, youtube_api_channel_id in channel_id_info:
        new_live_video_infos = get_new_youtube_live_video_infos(
            channel_id, youtube_api_channel_id
        )

        all_youtube_video_data = get_all_youtube_video_data(new_live_video_infos)

        for youtube_video_data in all_youtube_video_data:
            update_video_data(youtube_video_data)

        print(f"channel_id: {channel_id}")
        print(f"total_count: {len(all_youtube_video_data)}")
        print("Success update vtuber video info\n")


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
        else get_formatted_datetime(last_video_published_time)
    )


# 영상 정보 추출
def get_filtered_video_info(video_info, channel_id):
    youtube_api_video_id = video_info["id"]["videoId"]
    snippet = video_info["snippet"]
    filtered_video_info = {
        "title": snippet["title"],
        "video_url": snippet["title"],
        "thumbnail_url": snippet["thumbnails"]["high"]["url"],
        "created_at": snippet["publishTime"],
        "youtube_api_video_id": youtube_api_video_id,
        "channel_id": channel_id,
    }

    return filtered_video_info


# 최근에 업로드된 유튜브 라이브 영상들의 정보를 반환
# 처음으로 저장하는 것이라면 전부 저장함
def get_new_youtube_live_video_infos(channel_id, youtube_channel_id):
    youtube_data_api = get_youtube_data_api()

    last_video_published_time = get_last_video_published_time(channel_id)

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
        get_filtered_video_info(video_info, channel_id) for video_info in video_infos
    ]

    return filtered_video_infos


def get_all_youtube_video_data(video_infos):
    youtube_data_api = get_youtube_data_api()

    all_video_data = []
    try:
        for i in range(len(video_infos) - 1, -1, -1):
            video_info = video_infos[i]
            search_response = (
                youtube_data_api.videos()
                .list(part="statistics", id=video_info["youtube_api_video_id"])
                .execute()
            )
            video_statistics = search_response["items"][0]["statistics"]
            video_info["is_live"] = True
            video_info["view_count"] = video_statistics["viewCount"]
            video_info["like_count"] = video_statistics["likeCount"]
            video_info["comment_count"] = (
                video_statistics["commentCount"]
                if "commentCount" in video_statistics
                else 0
            )

            all_video_data.append(video_info)

    except Exception as e:
        print(f"Error: {str(e)}")
        print(video_statistics)

    return all_video_data


# Video DB Update
def update_video_data(youtube_video_data):
    try:
        session = get_session()

        new_video = Video(**youtube_video_data)
        session.add(new_video)

        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error: {str(e)}")

    finally:
        session.close()
