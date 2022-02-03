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