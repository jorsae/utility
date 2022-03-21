import pytest
import os
import sys
sys.path.append('.')
import renamer

@pytest.mark.parametrize("filename, filefilter, expected", [
    ('a', 'a', True),
    ('d¨1', '¨', True),
    ('d¨1', '¨1', True),
    ('3t32feqwgq32', '32feqq', False),
    ('abc', 'abcd', False),
    ('abcd', '', True),
    ('abcd', None, True),
    ('', None, True),
])
def test_file_match(filename, filefilter, expected):
    assert(renamer.file_match(filename, filefilter)) == expected

@pytest.mark.parametrize("filename, filefilter, expected", [
    ('a', r'\w', True),
    ('d¨1', r'\d', True),
    ('d¨1', r'¨1{d, 2}', False),
    ('3t32feqwgq32', '32feqq', False),
    ('abc', 'abcd', False),
    ('saongoaiemg,2.353ni2n36o..', '.+', True),
    ('saongoaiemg.+,2.353ni2n36o..', r'\.\+', True),
])
def test_file_match_regex(filename, filefilter, expected):
    assert(renamer.file_match(filename, filefilter)) == expected


@pytest.fixture
def create_files_get_hash():
    main_folder = 'test/test_renamer_data/'

    if not os.path.exists(f'{main_folder}test1.txt'):
        with open(f'{main_folder}test1.txt', 'w'): pass
    
    if not os.path.exists(f'{main_folder}test2.txt'):
        open(f'{main_folder}test2.txt', 'w').write('safasgaeht<')

    yield

    os.remove(f'{main_folder}test1.txt')
    os.remove(f'{main_folder}test2.txt')

def test_get_hash(create_files_get_hash):
    main_folder = 'test/test_renamer_data/'
    assert(renamer.get_hash(f'{main_folder}test1.txt') == 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
    assert(renamer.get_hash(f'{main_folder}test2.txt') == '02622b86c2f672e95809b6f51d214afe6276710a9a8fc1ba1e4e5f17ec061c5b')

@pytest.fixture
def create_file_change_filename():
    main_folder = 'test/test_renamer_data/'

    if not os.path.exists(f'{main_folder}start.txt'):
        open(f'{main_folder}start.txt', 'w').close()
    yield

    os.remove(f'{main_folder}end.txt')

def test_change_filename(create_file_change_filename):
    main_folder = 'test/test_renamer_data/'

    changed = renamer.change_filename(f'{main_folder}start.txt', f'{main_folder}end.txt')
    assert(changed) == True

@pytest.mark.parametrize("filepath, filetypes, expected", [
    ('/a/bin/a.txt', ['*'], True),
    ('/a/bin/a.txt', ['.png', '.pdf', '.txt'], True),
    ('/a/bin/a.txt', ['.png', '.pdf'], False),
    ('/a/bin/a.madethisshitup', ['.png', '.pdf'], False),
    (r'/a\asds\das\da\sd\asd\a.da/bin/a.madethisshitup', ['.png', '.madethisshitup'], True),
    (r'/a\asds\das\da\sd\asd\a.da/bin/a.mp3', ['.png', '.mp3'], True),
])
def test_check_filetype(filepath, filetypes, expected):
    assert(renamer.check_filetype(filepath, filetypes)) == expected

@pytest.fixture
def create_files_get_files():
    main_folder = 'test/test_renamer_data/'

    def create_file(path):
        if not os.path.exists(f'{main_folder}{path}'):
            with open(f'{main_folder}{path}', 'w'): pass
    
    def create_folder(path):
        if not os.path.exists(f'{main_folder}{path}'):
            os.mkdir(f'{main_folder}{path}')
    
    def delete_file(path):
        if os.path.exists(f'{main_folder}{path}'):
            os.remove(f'{main_folder}{path}')

    def delete_folder(path):
        if not os.path.exists(f'{main_folder}{path}'):
            os.rmdir(f'{main_folder}{path}')
    
    create_file('foo.txt')
    create_file('foo.jpg')
    create_folder('folder')
    create_file('folder/bar.txt')
    create_file('folder/var.mp3')

    yield
    
    delete_file('foo.txt')
    delete_file('foo.jpg')
    delete_file('folder/bar.txt')
    delete_file('folder/var.mp3')
    delete_folder('folder')

@pytest.mark.parametrize("recursive, filefilter, filetype, expected", [
    (False, None, ['*'], ['test/test_renamer_data/foo.txt', 'test/test_renamer_data/foo.jpg']),
    (False, None, ['.jpg'], ['test/test_renamer_data/foo.jpg']),
    (True, None, ['.txt'], ['test/test_renamer_data/foo.txt', 'test/test_renamer_data/folder/bar.txt']),
    (False, None, ['.jpg', '.mp3'], ['test/test_renamer_data/foo.jpg']),
    (True, None, ['.jpg', '.mp3'], ['test/test_renamer_data/foo.jpg', 'test/test_renamer_data/folder/var.mp3']),

    (True, 'foo', ['*'], ['test/test_renamer_data/foo.txt', 'test/test_renamer_data/foo.jpg']),
    (True, 'foo', ['*'], ['test/test_renamer_data/foo.txt', 'test/test_renamer_data/foo.jpg']),

])  

def test_get_files(recursive, filefilter, filetype, expected, create_files_get_files):
    root = os.path.abspath('test/test_renamer_data')
    files = renamer.get_files('test/test_renamer_data', recursive, filefilter, filetype)
    assert(files) == expected
    renamer.folder_searched.clear()

@pytest.mark.parametrize("old_filepath, replace_pattern, pattern, index, expected", [
    ('/a/lama til en ku.mp3', ' ', '?', 0, '/a/lama?til?en?ku.mp3'),
])  
def test_get_new_filename(old_filepath, replace_pattern, pattern, index, expected):
    assert(renamer.get_new_filename(old_filepath, replace_pattern, pattern, index)) == expected