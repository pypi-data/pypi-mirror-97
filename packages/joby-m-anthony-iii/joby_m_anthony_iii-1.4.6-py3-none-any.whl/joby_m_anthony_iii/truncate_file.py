from collections import deque
from itertools import islice

def truncate(filename, lines):
    with open(filename, 'r+') as f:
        blackhole = deque((),0).extend
        file_iterator = iter(f.readline, '')
        blackhole(islice(file_iterator, lines))
        f.truncate(f.tell())