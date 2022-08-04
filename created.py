from PIL import Image
import glob
import os

def get_date_taken(path):
    return Image.open(path)._getexif()[36867].replace(':', '_').split()[0]

for file in glob.glob('*.jpg'):
    ext = os.path.splitext(file)[1]
    name = get_date_taken(file)
    os.rename(file, f'{name}{ext}')