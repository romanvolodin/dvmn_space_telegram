from pathlib import Path

import requests

from image_download import parse_arguments, save_images


def fetch_spacex_latest_launch_image_urls():
    response = requests.get("https://api.spacexdata.com/v4/launches/latest")
    response.raise_for_status()
    return response.json()["links"]["flickr"]["original"]


if __name__ == "__main__":
    args = parse_arguments(
        "The script allows you to download images from SpaceX API."
    )
    image_dir = args.image_dir

    try:
        Path(image_dir).mkdir(parents=True, exist_ok=True)
    except PermissionError as err:
        exit(err)
    
    try:
        spacex_image_urls = fetch_spacex_latest_launch_image_urls()
    except requests.exceptions.HTTPError as err:
        exit(err)

    saved_images = save_images(spacex_image_urls, image_dir, "spacex")
    if saved_images:
        print(len(saved_images), "image(s) saved.")
