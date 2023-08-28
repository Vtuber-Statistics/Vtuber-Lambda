import os
from dotenv import load_dotenv

from dotenv import load_dotenv
from googleapiclient.discovery import build

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(verbose=True)

vtuber_name_infos = [
    ["TokinoSora", "토키노 소라"],
    ["Robocosan", "로보코 씨"],
    ["AZKi", "AZKi"],
    ["SakuraMiko", "사쿠라 미코"],
    ["HoshimachiSuisei", "호시마치 스이세이"],
    ["YozoraMel", "요조라 멜"],
    ["AkiRosenthal", "아키 로젠탈"],
    ["AkaiHaato", "아카이 하아토"],
    ["NatsuiroMatsuri", "나츠이로 마츠리"],
    ["MinatoAqua", "미나토 아쿠아"],
    ["MurasakiShion", "무라사키 시온"],
    ["NakiriAyame", "나키리 아야메"],
    ["YuzukiChoco", "유즈키 초코"],
    ["OozoraSubaru", "오오조라 스바루"],
    ["ShirakamiFubuki", "시라카미 후부키"],
    ["OokamiMio", "오오카미 미오"],
    ["NekomataOkayu", "네코마타 오카유"],
    ["InugamiKorone", "이누가미 코로네"],
    ["usadapekora", "우사다 페코라"],
    ["ShiranuiFlare", "시라누이 후레아"],
    ["ShiroganeNoel", "시로가네 노엘"],
    ["HoushouMarine", "호쇼 마린"],
    ["AmaneKanata", "아마네 카나타"],
    ["TsunomakiWatame", "츠노마키 와타메"],
    ["TokoyamiTowa", "토코야미 토와"],
    ["HimemoriLuna", "히메모리 루나"],
    ["KiryuCoco", "키류 코코"],
    ["YukihanaLamy", "유키하나 라미"],
    ["MomosuzuNene", "모모스즈 네네"],
    ["ShishiroBotan", "시시로 보탄"],
    ["OmaruPolka", "오마루 폴카"],
    ["LaplusDarknesss", "라플러스 다크니스"],
    ["TakaneLui", "타카네 루이"],
    ["HakuiKoyori", "하쿠이 코요리"],
    ["SakamataChloe", "사카마타 클로에"],
    ["kazamairoha", "카자마 이로하"],
]


# YouTube Data API v3 클라이언트 빌드
def get_youtube_data_api():
    api_service_name = "youtube"
    api_version = "v3"
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    youtube_data_api = build(
        api_service_name, api_version, developerKey=YOUTUBE_API_KEY
    )
    return youtube_data_api


# PostgreSQL 연결
def get_session():
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    dbname = os.getenv("DBNAME")

    db_connection_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(db_connection_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
