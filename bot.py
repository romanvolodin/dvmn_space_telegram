import time
from random import choice

import telegram


def send_images_to_telegram(bot_token, chat_id, image_paths, interval=10):
    bot = telegram.Bot(token=bot_token)
    while True:
        image_path = choice(image_paths)
        with open(image_path, "rb") as image:
            bot.send_photo(chat_id=chat_id, photo=image)
        time.sleep(interval)
