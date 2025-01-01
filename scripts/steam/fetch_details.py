import time
import logging
import requests
import pytz
from datetime import datetime
from steam_fetch_config import Config

KST = pytz.timezone('Asia/Seoul')

DATA_TYPE = "details"
Config.setup_s3_logging(bucket_name=Config.S3_BUCKET_NAME, data_type=DATA_TYPE)

def fetch_app_details(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        logging.info(f"Details for appid {appid} fetched successfully.")
        return appid, data
    except Exception as e:
        logging.error(f"Failed to fetch details for appid {appid}: {e}")
        return appid, None


def collect_all_details(appids, delay=3):
    details = {}
    for appid in appids:
        appid, data = fetch_app_details(appid)
        if data:
            details[appid] = data
        time.sleep(delay)

    return details

def main():
    try:
        appids = Config.download_from_s3('data/raw/steam/app-list/appids.json')
        if not appids:
            logging.error("No appids available to fetch details.")
            return

        combined_details = collect_all_details(appids)

        if combined_details:
            date_str = datetime.now(KST).strftime('%Y-%m-%d')
            filename = f'data/raw/steam/{DATA_TYPE}/{date_str}/combined_{DATA_TYPE}.json'
            Config.upload_to_s3(combined_details, filename)
            logging.info("Combined details data uploaded successfully.")
        else:
            logging.error("No details data collected to upload.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
