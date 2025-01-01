import requests
import logging
import pytz
from datetime import datetime
from twitch_fetch_config import Config

CLIENT_ID = Config.TWC_CLIENT_ID
ACCESS_TOKEN = Config.TWC_ACCESS_TOKEN

KST = pytz.timezone('Asia/Seoul')

DATA_TYPE = 'top_categories'
Config.setup_s3_logging(bucket_name=Config.S3_BUCKET_NAME, data_type=DATA_TYPE)

def create_headers():
    return {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }


def save_data_to_s3(data, page_num):
    date_str = datetime.now(KST).strftime('%Y-%m-%d')
    hour_str = datetime.now(KST).strftime('%H')
    file_name = f"data/raw/twitch/{DATA_TYPE}/{date_str}/{hour_str}/fetch_{DATA_TYPE}_{page_num}.json"
    Config.upload_to_s3(data, file_name)
    logging.info(f"Streams data for page {page_num} uploaded to S3 with key: {file_name}")


def fetch_streams(base_url, headers, params, max_pages=2):
    streams = []
    pages_fetched = 0

    while pages_fetched < max_pages:
        logging.info(f"Sending request to Twitch API with params: {params}")
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            logging.info(f"Received successful response: {response.status_code}")
            data = response.json()

            streams.extend(data.get('data', []))
            pages_fetched += 1

            save_data_to_s3(data, pages_fetched)

            if 'pagination' in data and 'cursor' in data['pagination']:
                next_cursor = data['pagination']['cursor']
                params['after'] = next_cursor
                logging.info(f"Next cursor: {next_cursor}")
            else:
                logging.info("No more pages to fetch.")
                break
        else:
            logging.error(f"Error: {response.status_code}, Message: {response.text}")
            break

    return streams


def main():
    headers = create_headers()
    base_url = "https://api.twitch.tv/helix/games/top"
    params = {}

    streams_data = fetch_streams(base_url, headers, params, 2)
    logging.info(f"Fetched {len(streams_data)} streams in total.")

if __name__ == "__main__":
    main()