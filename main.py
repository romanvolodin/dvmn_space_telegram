import os
import time
from datetime import datetime
from glob import glob
from pathlib import Path
from random import choice
from urllib.parse import urlparse

import requests
import telegram
from environs import Env


def save_image_from_url(url, save_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, "wb") as image:
        image.write(response.content)


def fetch_spacex_latest_launch_images():
    response = requests.get("https://api.spacexdata.com/v4/launches/latest")
    response.raise_for_status()
    return response.json()["links"]["flickr"]["original"]


def save_images(image_urls, save_path, filename):
    saved_images = []
    for index, image_url in enumerate(image_urls):
        ext = get_file_ext_from_url(image_url)
        image_path = f"{save_path}/{filename}_{index:03d}{ext}"
        save_image_from_url(image_url, image_path)
        saved_images.append(image_path)
    return saved_images


def fetch_random_NASA_APOD_images(api_key, count=10):
    image_urls = []
    while len(image_urls) < count:
        response = requests.get(
            "https://api.nasa.gov/planetary/apod",
            params={"api_key": api_key, "count": count},
        )
        response.raise_for_status()
        for apod in response.json():
            if apod["media_type"] == "image":
                image_urls.append(apod["url"])
    return image_urls[:count]


def fetch_NASA_EPIC_images(api_key):
    image_urls = []
    response = requests.get(
        "https://api.nasa.gov/EPIC/api/natural/images",
        params={"api_key": api_key},
    )
    response.raise_for_status()
    for image_metadata in response.json():
        image_name = image_metadata["image"]
        image_datetime = datetime.fromisoformat(image_metadata["date"])
        image_date = image_datetime.strftime("%Y/%m/%d")
        image_urls.append(
            (f"https://api.nasa.gov/EPIC/archive/natural/{image_date}"
            f"/png/{image_name}.png?api_key={api_key}")
        )
    return image_urls


def get_file_ext_from_url(url):
    path = urlparse(url).path
    file_name = os.path.split(path)[-1]
    return os.path.splitext(file_name)[-1]


if __name__ == "__main__":
    env = Env()
    env.read_env()

    nasa_api_key = env.str("NASA_API_KEY")
    tg_bot_token = env.str("TG_BOT_TOKEN")
    tg_channel_id = env.int("TG_CHANNEL_ID")

    nasa_apod_image_path = "images/nasa/apod"
    nasa_epic_image_path = "images/nasa/epic"
    spacex_image_path = "images/spacex"

    try:
        Path(nasa_apod_image_path).mkdir(parents=True, exist_ok=True)
        Path(nasa_epic_image_path).mkdir(parents=True, exist_ok=True)
        Path(spacex_image_path).mkdir(parents=True, exist_ok=True)
    except PermissionError as err:
        exit(err)

    try:
        nasa_apod_image_urls = fetch_random_NASA_APOD_images(nasa_api_key)
        nasa_epic_image_urls = fetch_NASA_EPIC_images(nasa_api_key)
        spacex_image_urls = fetch_spacex_latest_launch_images()
    except requests.exceptions.HTTPError as err:
        exit(err)
    save_images(nasa_apod_image_urls, nasa_apod_image_path, "apod")
    save_images(nasa_epic_image_urls, nasa_epic_image_path, "epic")
    save_images(spacex_image_urls, spacex_image_path, "spacex")

    bot = telegram.Bot(token=tg_bot_token)

    image_dir = "images"
    image_paths = glob(f"{image_dir}/**/**.*", recursive=True)
    while True:
        image_path = choice(image_paths)
        with open(image_path, "rb") as image:
            bot.send_photo(chat_id=tg_channel_id, photo=image)
        time.sleep(5)
