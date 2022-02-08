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