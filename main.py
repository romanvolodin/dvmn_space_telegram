from pathlib import Path
import requests


IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"


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


def save_spacex_latest_launch_images(save_path):
    saved_images = []
    image_urls = fetch_spacex_latest_launch_images()
    if not image_urls:
        return
    for index, image_url in enumerate(image_urls):
        image_path = f"{save_path}/{index}.jpg"
        save_image_from_url(image_url, image_path)
        saved_images.append(image_path)
    return saved_images


if __name__ == "__main__":
    try:
        Path("images").mkdir(exist_ok=True)
    except PermissionError as err:
        exit(err)

    save_spacex_latest_launch_images("images")