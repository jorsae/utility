import subprocess
import sys
from datetime import datetime
import os

files = os.listdir()
files.remove(sys.argv[0])

i = 0
fileconcat = []
filterconcat = ''
for file in files:
    fileconcat.append('-i')
    fileconcat.append(file)
    filterconcat += f'[{i}:a]'
    i += 1
filterconcat += f'concat=n={len(files)}:v=0:a=1[outa]'
sys_string = f"ffmpeg -filter_complex {filterconcat} -map [outa] output_{str(datetime.now()).replace(':', '-').replace(' ', '')}.m4a"

process_call = sys_string.split(' ')
index = 1
for fconcat in fileconcat:
    process_call.insert(index, fconcat)
    index += 1

print(process_call)
subprocess.call(process_call)