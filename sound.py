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

    whyp = is_whyp(url)
    if whyp:
        filename = get_filename_whyp(req)
        filename = filename.replace("/", "")
        audio_url = get_audio_url_whyp(req)
    else:
        filename = get_filename(req)
        filename = filename.replace("/", "")
        audio_url = get_audio_url(req)
    download(f"{filename}.m4a", audio_url, whyp)
    print("\nDownload completed")


def download(filename, audio_url, whyp):
    headers = None
    if whyp:
        print(f"Downloading: {filename} (whyp)")
        headers = {"referer": "https://www.whyp.it"}
    else:
        print(f"Downloading: {filename}")
        headers = None

    with open(filename, "wb") as f:
        response = requests.get(audio_url, headers=headers, stream=True)
        total_length = response.headers.get("content-length")

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ("=" * done, " " * (50 - done)))
                sys.stdout.flush()


def get_filename(req):
    url_split = req.url.split("/")
    return url_split[len(url_split) - 1]


def get_filename_whyp(req):
    html = bs4.BeautifulSoup(req.text, "lxml")
    return f"{str(html.title)[7:-15]}"


def get_audio_url(req):
    m4a_url = re.search("m4a.+", req.text).group()
    return m4a_url.replace("m4a: ", "").replace('"', "").replace("\r", "")


def get_audio_url_whyp(req):
    regex = ',"https:.+mp3'
    id = re.search(regex, req.text).group()[37:]
    return f"https://cdn.whyp.it/{id}"


def is_whyp(url):
    if "whyp.it" in url:
        return True
    return False


if __name__ == "__main__":
    main()
