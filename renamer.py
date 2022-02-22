import hashlib
import re
import os

folder_searched = []


def main():
    print('main')
    print(check_folder('/test'))
    path = '/test'
    # root = f'{os.getcwd()}{path}' # Ensure it's absolute path
    # get_files(root, True, None, '.*')

# Gets all files that matches filefilter
def get_files(root, recursive, filefilter, filetype):
    print(f'{root=}')
    files = []
    folder_searched.append(root)

    for file in os.listdir(root):
        filepath = f'{root}{file}'

        if os.path.isdir(filepath):
            if recursive is False:
                continue
            if filepath not in folder_searched:
                print(f'extend: {filepath}')
                files.extend(get_files(root, recursive, filefilter, filetype))
        else:
            print(f'{filepath=}')
            if check_filetype(filepath, filetype):
                pass


# Matches filename to filefilter using regex
def file_match(filename, filefilter):
    if filefilter is None:
        return True
    try:
        s = re.search(filefilter, filename)
        return False if s is None else True
    except Exception as e:
        print(e)
        return False

# Checks the folder input from user input
def check_folder(folder):
    if folder.startswith('/') is False:
        folder = f'/{folder}'
    
    if folder.startswith(os.getcwd()) is False:
        return f'{os.getcwd()}{folder}'
    return folder

# Checks the file extension to the filetype filter
def check_filetype(filepath, filetypes):
    filetype = os.path.splitext(filepath)[1]
    if filetypes == ['*']:
        return True
    return filetype in filetypes

# Changes filename
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