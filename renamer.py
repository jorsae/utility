import argparse
import hashlib
import re
import sys
import os
import pytest
import json

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
    
    TODO:
        Add CHECKS for argument parser
"""

class FileChange():
    def __init__(self, filepath, old_filepath, checksum):
        self.filepath = filepath
        self.old_filepath = old_filepath
        self.checksum = checksum
    
    def __str__(self):
        return f'{self.filepath} - {self.old_filepath} | {self.checksum}'

    def to_dict(self):
        return { 'filepath': self.filepath, 'old_filepath': self.old_filepath, 'checksum': self.checksum }
    
    # Creates a json file to restore changes made
    @staticmethod
    def create_recovery_file(args, file_changes):
        if len(file_changes) <= 0:
            print('No changes made')
            return

        save_data = {
            'root': args.root,
            'recursive': args.recursive,
            'filename': args.filename,
            'filetype': ' '.join(args.filetype),
            'find': args.find,
            'replace': args.replace,
            'file_changes': [obj.to_dict() for obj in file_changes]
        }
        try:
            json_data = json.dumps(save_data, ensure_ascii=False, indent=4)
            with open('recovery.json', 'w') as f:
                f.write(json_data)
        except Exception as e:
            print(e)

def main():
    args = parse_arguments()

    print(f'Running renamer.py with')
    print(f'{args}')
    print(f'Fetching files..')
    files = get_files(args.root, args.recursive, args.filename, args.filetype)
    print(f'Found {len(files)} files')
    
    changes = []
    for filename in files:
        new_name = get_new_filename(filename, args.find, args.replace, 0)
        change = change_filename(filename, new_name, args.hash)
        if change:
            changes.append(change)
    print(f'Made: {len(changes)} changes')
    print(f'Creating recovery file..')
    FileChange.create_recovery_file(args, changes)
    print(f'Finished')

def recover(recovery_file):
    print(f'Recover from file: {recovery_file}')
    print('Parsing recovery file')
    
    file_changes = parse_recovery_file(recovery_file)
    print(f'Found {len(file_changes)} file changes')

    for fc in file_changes:
        changes = change_filename(fc.filepath, fc.old_filepath, True)
        print(changes)

# Parses a recovery file
def parse_recovery_file(recovery_file):
    try:
        with open(recovery_file) as f:
            data = json.loads(f.read())
        
        file_changes = []
        file_changes_data = data.get("file_changes")
        for fc in file_changes_data:
            file_changes.append(FileChange(fc['filepath'], fc['old_filepath'], fc['checksum']))
        return file_changes
    except Exception as e:
        print(e)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', '-r', default='.', type=str, help='Root directory to start search')
    parser.add_argument('--recursive', '-R', action='store_true', help='File search is recursive')
    parser.add_argument('--filename', '-f', type=str, default='.+', help='Search filter based on filename')
    parser.add_argument('--filetype', '-F', type=str, default="*", help='Search filter based on filetype')
    parser.add_argument('--find', '-fi', type=str, help='Search pattern in filename we replace')
    parser.add_argument('--replace', '-rep', type=str, help='Pattern for new filename')
    
    parser.add_argument('--hash', '-H', action='store_false', default=True, help='Recovery file stores checksum')
    parser.add_argument('--recover', type=str, help='Recover from recovery file')

    args = parser.parse_args()
    return clean_arguments(args)

def clean_arguments(args):
    if args.recover:
        recover(args.recover)
        sys.exit()
    
    if is_arg_empty(args.root) or is_arg_empty(args.find) or is_arg_empty(args.replace):
        print(f'root, find and replace is required.\nExiting..')
        sys.exit()

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
    
    pattern = filename_increment(pattern, index)
    new_filename = re.sub(replace_pattern, pattern, filename)

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
def change_filename(old_filepath, new_filepath, hash):
    if old_filepath == new_filepath:
        return
    try:
        os.rename(old_filepath, new_filepath)
        checksum = None
        if hash:
            checksum = get_hash(new_filepath)
        
        return FileChange(new_filepath, old_filepath, checksum)
    except OSError as oe:
        print(oe)
        return False
    except Exception as e:
        print(e)
        return False

# Gets checksum from a file
def get_hash(filename):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def is_arg_empty(value):
    if value is None or value == '':
        return True
    return False

if __name__ == '__main__':
    main()