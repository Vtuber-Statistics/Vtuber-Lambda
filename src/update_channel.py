from model import Channel
from utils import vtuber_name_infos, get_youtube_data_api, get_session


# 버튜버 채널 정보 업데이트
def update_channel():
    for youtube_user_name, vtuber_name in vtuber_name_infos:
        youtube_api_channel_id = get_youtube_api_channel_id(youtube_user_name)

        youtube_channel_data = get_youtube_channel_data(
            vtuber_name, youtube_api_channel_id
        )

        upsert_channel_data(youtube_api_channel_id, youtube_channel_data)


# 유튜브 유저 이름으로 채널 ID를 검색
def get_youtube_api_channel_id(youtube_user_name):
    youtube_data_api = get_youtube_data_api()

    search_response = (
        youtube_data_api.search()
        .list(part="id", q=youtube_user_name, type="channel", maxResults=1)
        .execute()
    )
    youtube_api_channel_id = search_response["items"][0]["id"]["channelId"]

    return youtube_api_channel_id


# 채널 ID로 채널 정보를 검색
def get_youtube_channel_data(vtuber_name, youtube_api_channel_id):
    youtube_data_api = get_youtube_data_api()

    channel_response = (
        youtube_data_api.channels()
        .list(id=youtube_api_channel_id, part="snippet,statistics", maxResults=1)
        .execute()
    )
    channel_info = channel_response["items"][0]["snippet"]
    channel_statistics = channel_response["items"][0]["statistics"]

    channel_data = {
        "vtuber_name": vtuber_name,
        "group": "hololive",  # 추후 수정
        "country": channel_info["country"],
        "channel_name": channel_info["title"],
        "custom_url": channel_info["customUrl"],
        "thumbnail_url": channel_info["thumbnails"]["medium"]["url"],
        "created_at": channel_info["publishedAt"],
        "subscriber_count": channel_statistics["subscriberCount"],
        "total_view_count": channel_statistics["viewCount"],
        "video_count": channel_statistics["videoCount"],
        "youtube_api_channel_id": youtube_api_channel_id,
    }
    return channel_data


# 채널 DB Upsert
def upsert_channel_data(youtube_api_channel_id, youtube_channel_data):
    try:
        session = get_session()
        # youtube_api_channel_id와 매칭되는 channel이 있는지 확인
        # 존재하면 업데이트 없으면 추가
        existing_channel = (
            session.query(Channel)
            .filter_by(youtube_api_channel_id=youtube_api_channel_id)
            .first()
        )

        if existing_channel:
            # 업데이트
            for key, value in youtube_channel_data.items():
                setattr(existing_channel, key, value)
        else:
            # 추가
            new_channel = Channel(**youtube_channel_data)
            session.add(new_channel)

        session.commit()
        print("Success update vtuber channel info")

    except Exception as e:
        session.rollback()
        print(f"Error: {str(e)}")

    finally:
        session.close()
