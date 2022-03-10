import hashlib
import re
import os
import pytest

folder_searched = []


def main():
    print('main')
    #path = os.path.abspath('/home/sandrathefox')

    #files = get_files(path, True, None, ['.jpg'])
    #print(f'{files=}')

    files = get_files('test/test_renamer_data', True, None, ['.jpg', '.mp3'])
    print(f'{files=}')
    #ft = check_filetype('test/test_renamer_data/folder/var.mp3', ['.mp3'])
    #print(ft)
    

# Gets all files that matches filefilter
def get_files(root, recursive, filefilter, filetype):
    print(f'{root=} | {len(os.listdir(root))}')
    files = []
    folder_searched.append(root)

    for file in os.listdir(root):
        filepath = f'{root}/{file}'
        print(f'file: {filepath}')

        #print(f'{folder_searched=}')
        #print(f'{filepath=}')
        if os.path.isdir(filepath):
            print(f'isdir: {filepath}')
            if recursive is False:
                continue
            if filepath not in folder_searched:
                print(f'extend: {filepath}')
                files.extend(get_files(f'{filepath}', recursive, filefilter, filetype))
            else:
                print(f'in f_searched: {filepath}')
                print(f'{folder_searched=}')
        else:
            #print(f'not dir: {filepath}')
            if check_filetype(filepath, filetype):
                if file_match(filepath, filefilter):
                    #print(f'added: {filepath}')
                    files.append(filepath)
    return files


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

# TODO: Probably not needed. Can just use os.path.abspath
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