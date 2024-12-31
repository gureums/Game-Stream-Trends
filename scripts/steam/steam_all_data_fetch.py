import os
import json
import logging
import requests
from datetime import datetime

# 데이터를 저장할 디렉토리 설정 및 생성
RAW_DATA_DIR = "data/raw/steam"

NEWS_DIR = os.path.join(RAW_DATA_DIR, "news")
PLAYERS_DIR = os.path.join(RAW_DATA_DIR, "players")
DETAILS_DIR = os.path.join(RAW_DATA_DIR, "details")
REVIEW_DIR = os.path.join(RAW_DATA_DIR, "reviewmeta")

os.makedirs(NEWS_DIR, exist_ok=True)
os.makedirs(PLAYERS_DIR, exist_ok=True)
os.makedirs(DETAILS_DIR, exist_ok=True)
os.makedirs(REVIEW_DIR, exist_ok=True)

# 로그 디렉토리 설정 및 생성
log_dir = os.path.join("logs", "steam")
os.makedirs(log_dir, exist_ok=True)

# 로그 파일명: steam_data_fetch_날짜_일시.log
log_filename = os.path.join(log_dir, f"steam_data_fetch_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# 로깅 설정
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# 전체 앱 목록 수집
# game과 그 외의 app이 섞여 있으나 모두 다 수집함
def fetch_app_list():
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        with open(os.path.join(RAW_DATA_DIR, "app_list.json"), "w") as f:
            json.dump(data["applist"]["apps"], f, indent=4)

        logging.info("Complete app list saved successfully.")
        return data["applist"]["apps"]
    except Exception as e:
        logging.error(f"Failed to fetch app list: {e}")
        return []


# 특정 앱의 뉴스 정보 수집
def fetch_app_news(appid):
    url = f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v2?appid={appid}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        with open(os.path.join(NEWS_DIR, f"app_{appid}_news.json"), "w") as f:
            json.dump(data, f, indent=4)

        logging.info(f"News for appid {appid} saved successfully.")
    except Exception as e:
        logging.error(f"Failed to fetch news for appid {appid}: {e}")


# 특정 앱의 동시 접속자 수 수집
def fetch_app_players(appid):
    url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        with open(os.path.join(PLAYERS_DIR, f"app_{appid}_players.json"), "w") as f:
            json.dump(data, f, indent=4)

        logging.info(f"Player count for appid {appid} saved successfully.")
    except Exception as e:
        logging.error(f"Failed to fetch players for appid {appid}: {e}")


# 특정 앱의 상세 정보 수집
# success, type이 무엇이든 간에 모든 앱에 대해 수집하도록 수정
# 후에 Transform 할 때 success = True, type = game인 appid만 사용하게 될 듯
def fetch_app_details(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        with open(os.path.join(DETAILS_DIR, f"app_{appid}_details.json"), "w") as f:
            json.dump(data, f, indent=4)

        logging.info(f"Details for appid {appid} saved successfully.")
        return True
    except Exception as e:
        logging.error(f"Failed to fetch details for appid {appid}: {e}")
        return False


# 특정 앱의 리뷰 관련 메타데이터 수집
def fetch_app_reviewmeta(appid):
    # 리뷰 관련 데이터 가져오기 위한 URL
    url = f"https://store.steampowered.com/appreviews/{appid}?json=1&language=all&review_type=all&purchase_type=all&playtime_filter_min=0&playtime_filter_max=0&playtime_type=all&filter_offtopic_activity=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        with open(os.path.join(REVIEW_DIR, f"app_{appid}_reviewmeta.json"), "w") as f:
            json.dump(data, f, indent=4)

        logging.info(f"Review data for appid {appid} saved successfully.")
        return True
    except Exception as e:
        logging.error(f"Failed to fetch review data for appid {appid}: {e}")
        return False


def main():
    app_list = fetch_app_list()

    # 각 appid에 대한 details, news, players, review metadata 수집
    for app in app_list:
        appid = app["appid"]
        logging.info(f"Fetching data for app {appid} - {app['name']}")

        fetch_app_details(appid)
        fetch_app_news(appid)
        fetch_app_players(appid)
        fetch_app_reviewmeta(appid)

    logging.info(f"Collected data for {len(app_list)} games.")

if __name__ == "__main__":
    main()