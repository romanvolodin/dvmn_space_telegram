from datetime import datetime
from pathlib import Path

import requests
from environs import Env

from image_download import parse_arguments, save_images


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


if __name__ == "__main__":
    args = parse_arguments(
        "The script allows you to download images from NASA API."
    )
    image_dir = args.image_dir

    env = Env()
    env.read_env()
    nasa_api_key = env.str("NASA_API_KEY")

    try:
        Path(image_dir).mkdir(parents=True, exist_ok=True)
    except PermissionError as err:
        exit(err)
    
    try:
        nasa_apod_image_urls = fetch_random_NASA_APOD_images(nasa_api_key)
        nasa_epic_image_urls = fetch_NASA_EPIC_images(nasa_api_key)
    except requests.exceptions.HTTPError as err:
        exit(err)

    saved_apod_images = save_images(
        nasa_apod_image_urls, image_dir, "nasa_apod"
    )
    if saved_apod_images:
        print(len(saved_apod_images), "APOD image(s) saved.")
    
    saved_epic_images = save_images(
        nasa_epic_image_urls, image_dir, "nasa_epic"
    )
    if saved_epic_images:
        print(len(saved_epic_images), "EPIC image(s) saved.")
