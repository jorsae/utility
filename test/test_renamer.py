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
        open(f'{main_folder}test1.txt', 'w').close()
    
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