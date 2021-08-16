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


if __name__ == "__main__":
    try:
        Path("images").mkdir(exist_ok=True)
    except PermissionError as err:
        exit(err)

    try:
        hubble_image = save_image_from_url(IMAGE_URL, "images/hubble.jpeg")
    except requests.exceptions.HTTPError as err:
        exit(err)