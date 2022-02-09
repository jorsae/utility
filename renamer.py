import hashlib
import re
import os

def main():
    print('main')


# Matches filename to filefilter using regex
def file_match(filename, filefilter):
    try:
        s = re.search(filefilter, filename)
        return False if s is None else True
    except Exception as e:
        print(e)

def change_filename(old_filepath, new_filepath):
    try:
        os.rename(old_filepath, new_filepath)
        return True
    except OSError as oe:
        print(oe)
        return False
    except Exception as e:
        print(e)
        return False

# Gets checksum from a file
def get_hash(file):
    sha256 = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

if __name__ == '__main__':
    main()