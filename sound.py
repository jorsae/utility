import re
import sys

import requests


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <url>")
        sys.exit()

    url = sys.argv[1]
    req = requests.get(url)
    if req.status_code != 200:
        print("Oops")
        sys.exit()

    m4a_url = re.search("m4a.+", req.text).group()
    m4a_url = m4a_url.replace("m4a: ", "").replace('"', "").replace("\r", "")
    filename = get_filename(url)
    download(filename, m4a_url)


def get_filename(url):
    url_split = url.split("/")
    return url_split[len(url_split) - 1]


def download(filename, url):
    print(f"Downloading {url}")
    audio = requests.get(url)
    with open(f"{filename}.m4a", "wb") as f:
        f.write(audio.content)


if __name__ == "__main__":
    main()
