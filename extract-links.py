#!/usr/bin/python

import sys
import re

argc = len(sys.argv)

link_pattern = sys.argv[1]
files = sys.argv[2:]

# match any a even if the text part in on different line
link = re.compile(r'<a href="({l})">'.format(l=link_pattern))

entries = []

for name in files:
    with open(name, 'r') as f:
        for line in f:
            match = link.search(line)
            if match:
                entries.append(match.group(1))

# remove anchor part
entries = [entry.split('#')[0] for entry in entries]

# only unique entries, preserved only the first one
previous = None
unique_entries = []
for entry in entries:
    if entry not in unique_entries:
        unique_entries.append(entry)

# print in one line
sys.stdout.write(' '.join(unique_entries))
