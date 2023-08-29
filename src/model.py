from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 버튜버 채널 정보
class Channel(Base):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vtuber_name = Column(String(20), nullable=False)
    group = Column(String(20), nullable=False)
    country = Column(String(10), nullable=False)
    channel_name = Column(String(50), nullable=False)
    custom_url = Column(String(50), nullable=False)
    thumbnail_url = Column(String(255), nullable=False)
    subscriber_count = Column(Integer, nullable=False)
    total_view_count = Column(Integer, nullable=False)
    video_count = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    youtube_api_channel_id = Column(String(50), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "vtuber_name", "channel_name", "custom_url", "youtube_api_channel_id"
        ),
    )


# 종료된 라이브 유튜브 영상 정보
class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    video_url = Column(String(255), nullable=False)
    thumbnail_url = Column(String(255), nullable=False)
    is_live = Column(Boolean, nullable=False)
    view_count = Column(Integer, nullable=False)
    like_count = Column(Integer, nullable=False)
    comment_count = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    youtube_api_video_id = Column(String(50), nullable=False)

    channel_id = Column(Integer, ForeignKey("channel.id"), nullable=False)
    channel = relationship("Channel")

    __table_args__ = (UniqueConstraint("video_url", "youtube_api_video_id"),)
