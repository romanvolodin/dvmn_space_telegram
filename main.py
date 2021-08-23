import argparse
import os
import time

from glob import glob
from random import choice
from urllib.parse import unquote, urlsplit

import requests
import telegram
from environs import Env


def parse_arguments(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--image-dir",
        help="A path to images folder",
        default="./images",
    )
    return parser.parse_args()


def save_image_from_url(url, save_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, "wb") as image:
        image.write(response.content)


def save_images(image_urls, save_path, filename):
    saved_images = []
    for index, image_url in enumerate(image_urls):
        ext = get_file_ext_from_url(image_url)
        image_path = f"{save_path}/{filename}_{index:03d}{ext}"
        save_image_from_url(image_url, image_path)
        saved_images.append(image_path)
    return saved_images


def get_file_ext_from_url(url):
    path = unquote(urlsplit(url).path)
    return os.path.splitext(path)[-1]


if __name__ == "__main__":
    args = parse_arguments(
        "The script allows you to upload images to a Telegram channel."
    )
    image_dir = args.image_dir

    env = Env()
    env.read_env()

    tg_bot_token = env.str("TG_BOT_TOKEN")
    tg_channel_id = env.int("TG_CHANNEL_ID")
    posting_interval = env.int("POSTING_INTERVAL")

    if not os.path.exists(image_dir):
        exit(f"'{image_dir}' dir does not exist.")

    image_paths = glob(f"{image_dir}/**/**.*", recursive=True)
    if not image_paths:
        exit(f"Can't find any images in {image_dir} dir")

    bot = telegram.Bot(token=tg_bot_token)
    while True:
        image_path = choice(image_paths)
        with open(image_path, "rb") as image:
            bot.send_photo(chat_id=tg_channel_id, photo=image)
        time.sleep(posting_interval)
