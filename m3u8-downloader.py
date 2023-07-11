import requests

# Download m3u8 file.
# Run this script
# ffmpeg -i all.ts output.mp3

def download(url):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(f'all.ts', 'a+b') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

with open('track.m3u8', 'r') as f:
    for line in f.readlines():
        line = line.strip()
        if line.startswith('https:'):
            download(line)