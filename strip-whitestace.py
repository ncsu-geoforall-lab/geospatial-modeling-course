#!/usr/bin/python

import sys
import fileinput
import re

block_start = re.compile(r'^\s*<pre><code>\s*$')

for line in fileinput.input():
    # ignore header
    if block_start.search(line):
        line = line.rstrip(' \t\n')
        sys.stdout.write(line)
    else:
        sys.stdout.write(line)
