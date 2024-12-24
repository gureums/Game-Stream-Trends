import os
import time
import json
import logging
import requests
from datetime import datetime

# 데이터를 저장할 디렉토리 설정 및 생성
RAW_DATA_DIR = "data/raw/steam"

os.makedirs(RAW_DATA_DIR, exist_ok=True)

# 로그 디렉토리 설정 및 생성
LOG_DIR = os.path.join("logs", "steam")
os.makedirs(LOG_DIR, exist_ok=True)

# 로그 파일명: steam_data_fetch_날짜_일시.log
log_filename = os.path.join(LOG_DIR, f"steam_app_list_fetch_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

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

# total_app_list를 청크로 나눔 (appid 1000개씩)
def chunk_apps(app_list, chunk_size=1000):
    for i in range(0, len(app_list), chunk_size):
        yield app_list[i:i + chunk_size]

# 나눈 청크를 json으로 저장
def save_chunks_to_files(app_list, chunk_size=1000):
    chunked_app_list = list(chunk_apps(app_list, chunk_size))

    for idx, chunk in enumerate(chunked_app_list):
        chunk_file = os.path.join(RAW_DATA_DIR, f"app_list_chunk_{idx + 1}.json")

        with open(chunk_file, "w") as f:
            json.dump(chunk, f, indent=4)
        logging.info(f"Chunk {idx + 1} saved to {chunk_file}")

def main():
    # 전체 앱 목록 가져오기
    app_list = fetch_app_list()
    
    if app_list:
        save_chunks_to_files(app_list)
    else:
        logging.error("No app list data found. Exiting.")

if __name__ == "__main__":
    main()