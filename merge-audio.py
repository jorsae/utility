import subprocess
import sys
from datetime import datetime
import os

files = os.listdir()
files.remove(sys.argv[0])

index = 0
fileconcat = ''
filterconcat = ''
for file in files:
    fileconcat += f'-i {file} '
    filterconcat += f'[{index}:a]'
    index += 1
fileconcat = fileconcat[:-1]
filterconcat += f'concat=n={len(files)}:v=0:a=1[outa]'

sys_string = f"ffmpeg {fileconcat} -filter_complex {filterconcat} -map [outa] {str(datetime.now()).replace(':', '-').replace(' ', '')}.m4a"
subprocess.call(sys_string.split(' '))