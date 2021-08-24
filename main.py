import os
import time
from glob import glob
from random import choice

import telegram
from environs import Env

from image_download import parse_arguments


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
