import re
import sys

import bs4
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

    filename = get_filename(req)
    audio_url = get_audio_url(req)
    download(filename, audio_url)


def download(filename, url):
    print("Downloading")

    url = f"https://cdn.whyp.it/{url}"
    headers = {"referer": "https://www.whyp.it"}
    audio = requests.get(url, headers=headers)
    with open(f"{filename}.m4a", "wb") as f:
        f.write(audio.content)


def get_filename(r):
    html = bs4.BeautifulSoup(r.text, "lxml")
    return f"{str(html.title)[7:-15]}"


def get_audio_url(r):
    regex = ',"https:.+mp3'
    id = re.search(regex, r.text).group()[37:]
    return id


if __name__ == "__main__":
    main()
