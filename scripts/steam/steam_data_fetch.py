import os
import time
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
# success == true, type == game인 것만 수집하고 true 반환, 그 외 false
# 여기서 true를 반환한 appid만을 이용하여 fetch_app_news, fetch_app_players의 데이터를 수집하게 됨
def fetch_app_details(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # success == true, type == game일 때만 처리함
        if data[str(appid)]["success"] and data[str(appid)]["data"]["type"] == "game":
            # 데이터 저장
            with open(os.path.join(DETAILS_DIR, f"app_{appid}_details.json"), "w") as f:
                json.dump(data, f, indent=4)
            logging.info(f"Details for appid {appid} saved successfully.")
            return True  # 게임인 경우 True 반환
        else:
            logging.info(f"Appid {appid} is not a game or not successful.")
            return False  # 게임이 아니면 False 반환
    except Exception as e:
        logging.error(f"Failed to fetch details for appid {appid}: {e}")
        return False


# 특정 앱의 리뷰 관련 메타데이터 수집
def fetch_app_reviewmeta(appid):
    # 리뷰 관련 데이터 가져오기 위한 URL
    url = f"https://store.steampowered.com/appreviews/{appid}?json=1&language=all&review_type=all&purchase_type=all&playtime_filter_min=0&playtime_filter_max=0&playtime_type=all&filter_offtopic_activity=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # 요청이 실패하면 예외 발생
        data = response.json()  # JSON 데이터 그대로 파싱

        # JSON 데이터를 그대로 저장
        with open(os.path.join(REVIEW_DIR, f"app_{appid}_reviewmeta.json"), "w") as f:
            json.dump(data, f, indent=4)  # 원시 JSON 데이터를 파일에 저장

        logging.info(f"Review data for appid {appid} saved successfully.")
        return True  # 성공적으로 저장된 경우 True 반환

    except Exception as e:
        logging.error(f"Failed to fetch review data for appid {appid}: {e}")
        return False  # 예외가 발생한 경우 False 반환


def main():
    # 전체 앱 목록 가져오기
    app_list = fetch_app_list()
    # time.sleep(1)

    # 20개 이상의 게임 데이터를 수집할 때까지 반복
    # (fetch_app_details에서 true를 반환하는 appid만 20개 수집)
    collected_games = 0
    index = 0

    while collected_games < 20 and index < len(app_list):
        app = app_list[index]
        appid = app["appid"]
        logging.info(f"Fetching data for app {appid} - {app['name']}")

        # fetch_app_details에서 필터링된 appid만 news, players에 전달
        if fetch_app_details(appid):
            fetch_app_news(appid)
            # time.sleep(1)

            fetch_app_players(appid)
            # time.sleep(1)

            fetch_app_reviewmeta(appid)
            # time.sleep(1)

            collected_games += 1

        index += 1

    logging.info(f"Collected {collected_games} game data.")

if __name__ == "__main__":
    main()
