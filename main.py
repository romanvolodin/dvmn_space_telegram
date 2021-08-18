import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from environs import Env


IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
NASA_API_URL = "https://api.nasa.gov/planetary/apod"


def save_image_from_url(url, save_path):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) "
            "Gecko/20100101 Firefox/88.0"
        )
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with open(save_path, "wb") as image:
        image.write(response.content)


def fetch_spacex_latest_launch_images():
    SPACEX_API_URL = "https://api.spacexdata.com/v4/launches/latest"
    response = requests.get(SPACEX_API_URL)
    response.raise_for_status()
    return response.json()["links"]["flickr"]["original"]


def save_images(image_urls, save_path):
    saved_images = []
    for index, image_url in enumerate(image_urls):
        ext = get_file_ext_from_url(image_url)
        image_path = f"{save_path}/{index}{ext}"
        save_image_from_url(image_url, image_path)
        saved_images.append(image_path)
    return saved_images


def fetch_random_nasa_apod_images(api_key, count=10):
    params = {
        "api_key": api_key,
        "count": count,
    }
    image_urls = []
    while len(image_urls) < count:
        response = requests.get(NASA_API_URL, params=params)
        response.raise_for_status()
        for apod in response.json():
            if apod["media_type"] == "image":
                image_urls.append(apod["url"])
    return image_urls[:count]


def get_file_ext_from_url(url):
    path = urlparse(url).path
    file_name = os.path.split(path)[-1]
    return os.path.splitext(file_name)[-1]


if __name__ == "__main__":
    env = Env()
    env.read_env()

    nasa_api_key = env.str("NASA_API_KEY")

    try:
        Path("images").mkdir(exist_ok=True)
    except PermissionError as err:
        exit(err)

    nasa_apod_image_urls = fetch_random_nasa_apod_images(nasa_api_key)
    save_images(nasa_apod_image_urls, "images")
