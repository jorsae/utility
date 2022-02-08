import hashlib
import re

def main():
    print('main')


# Matches filename to filefilter using regex
def file_match(filename, filefilter):
    try:
        s = re.search(filefilter, filename)
        return False if s is None else True
    except Exception as e:
        print(e)

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