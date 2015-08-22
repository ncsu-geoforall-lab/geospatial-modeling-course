#!/usr/bin/python

import sys
import fileinput
import re

block_start = re.compile(r'^\s*<pre><code>\s*$')

for line in fileinput.input():
    # ignore header
    line = re.sub(r'<em class="module">([^<]*)</em>',
                  r'<em class="module"><a href="https://grass.osgeo.org/grass70/manuals/\1.html">\1</a></em>',
                  line)
    if block_start.search(line):
        line = line.rstrip(' \t\n')
        sys.stdout.write(line)
    else:
        sys.stdout.write(line)
