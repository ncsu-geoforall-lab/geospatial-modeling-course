#!/usr/bin/python

import sys
import re

argc = len(sys.argv)

page_title = sys.argv[1]
directory = sys.argv[2]
files = sys.argv[3:]

heading = re.compile(r'<[Hh]..*>(.+)</[Hh].>|<[Pp]><[Bb]>Topic: (.+)</[Bb]></[Pp]>')

entries = []

for name in files:
    with open(name, 'r') as f:
        for line in f:
            match = heading.search(line)
            if match:
                if match.group(1):
                    title = match.group(1)
                else:
                    title = match.group(2)
                # TODO: handle with and without /, now only with /
                if name.startswith(directory):
                    name = name[len(directory):]
                entries.append((name, title))
                break

sys.stdout.write('<h2>{t}</h2>\n\n'.format(t=page_title))

sys.stdout.write('<ul>\n')
for (filename, title) in entries:
    sys.stdout.write('    <li><a href="{f}">{t}</a></li>\n'.format(f=filename, t=title))
sys.stdout.write('</ul>\n')
