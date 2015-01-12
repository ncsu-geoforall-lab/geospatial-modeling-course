#!/usr/bin/python

import sys
import re

argc = len(sys.argv)

link_pattern = sys.argv[1]
files = sys.argv[2:]

link = re.compile(r'<a href="({l})">.+</a>'.format(l=link_pattern))

entries = []

for name in files:
    with open(name, 'r') as f:
        for line in f:
            match = link.search(line)
            if match:
                sys.stdout.write(match.group(1) + ' ')
