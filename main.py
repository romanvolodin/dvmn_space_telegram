import os
from glob import glob


from environs import Env

from bot import send_images_to_telegram
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

    send_images_to_telegram(
        tg_bot_token, tg_channel_id, image_paths, posting_interval
    )
