import argparse
import hashlib
import re
import os
import pytest

folder_searched = []
"""
    Arguments:
        root: root directory
        recursive: whether the search is recursive or not
        filetype: filter out files based on filetype
        file: filter out files based on filename
        replace: pattern in filename, that we replace
        pattern: pattern for the new filename for the file
        hash: recovery file will store checksum of the file

        recover: parses recovery file and undo everything that's been done
"""

"""
    TODO:
        Add CHECKS for argument parser
"""

def main():
    print('main')
    args = parse_arguments()
    print(f'{args}')

    files = get_files(args.root, args.recursive, args.filename, args.filetype)
    print(files)
    # def get_new_filename(old_filepath, replace_pattern, pattern, index):
    # def change_filename(old_filepath, new_filepath):
    for file in files:
        new_name = get_new_filename(file, args.find, args.replace, 0)
        print(f'{new_name=}')
        change_filename(file, new_name)

    #path = os.path.abspath('/home/sandrathefox')

    #files = get_files(path, True, None, ['.jpg'])
    #print(f'{files=}')

    # a = get_new_filename('a/lama til en ku.mp3', ' ', '?', 0)
    # print(a)
    # files = get_files('test/test_renamer_data', True, None, ['.jpg', '.mp3'])
    # print(f'{files=}')
    #ft = check_filetype('test/test_renamer_data/folder/var.mp3', ['.mp3'])
    #print(ft)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', '-r', type=str, help='Root directory to start search')
    parser.add_argument('--recursive', '-R', action='store_true', help='File search is recursive')
    parser.add_argument('--filename', '-f', type=str, default='.+' help='Search filter based on filename')
    parser.add_argument('--filetype', '-F', type=str, default="*", help='Search filter based on filetype')
    parser.add_argument('--find', '-fi', type=str, help='Search pattern in filename we replace')
    parser.add_argument('--replace', '-rep', type=str, help='Pattern for new filename')
    
    parser.add_argument('--hash', '-H', action='store_true', help='Recovery file stores checksum')
    parser.add_argument('--recover', type=str, help='Recover from recovery file')

    return clean_arguments(args)

def clean_arguments(args):
    if args.recover:
        print(f'Recovery mode: {args.recover}')
        print('TODO: write recovery mode')
        os.kill()
    
    if args.filetype:
        args.filetype = args.filetype.split()
    
    return args

# Gets all files that matches filename & filetypes
def get_files(root, recursive, filename, filetypes):
    files = []
    folder_searched.append(root)

    for file in os.listdir(root):
        filepath = f'{root}/{file}'
        if os.path.isdir(filepath):
            if recursive is False:
                continue
            if filepath not in folder_searched:
                files.extend(get_files(f'{filepath}', recursive, filename, filetypes))
        else:
            if check_filetype(filepath, filetypes):
                if file_match(filepath, filename):
                    files.append(filepath)
    return files

# Checks if filename is in filepath
def file_match(filepath, filename):
    if filename is None:
        return True
    try:
        s = re.search(filename, filepath)
        return False if s is None else True
    except Exception as e:
        print(e)
        return False

# Checks the filepath's filetype is in filetypes
def check_filetype(filepath, filetypes):
    filetype = os.path.splitext(filepath)[1]
    if filetypes == ['*']:
        return True
    return filetype in filetypes

def get_new_filename(old_filepath, replace_pattern, pattern, index):
    extension = os.path.splitext(old_filepath)[1]
    filename = os.path.basename(old_filepath)
    filename = filename[0:-len(extension)]
    path = os.path.dirname(old_filepath)
    print(f'{filename=}, {extension=}')
    
    pattern = filename_increment(pattern, index)
    new_filename = re.sub(replace_pattern, pattern, filename)

    print(f'{new_filename=}')
    return f'{path}/{new_filename}{extension}'

# Replaces ? in args.pattern and replaces it with incremental numbers, 0-padded for each ?
def filename_increment(filename, index):
    digits = filename.count('?')
    if digits <= 0:
        return filename

    loc = filename.find('?')
    padding = digits - len(str(index))
    index_num = index
    if padding > 0:
        index_num = f'{"0" * padding}{index}'

    filename = f'{filename[:loc]}{index_num}{filename[loc:]}'
    filename = filename.replace('?', '')
    return filename

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