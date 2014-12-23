#!/usr/bin/python

import sys
import fileinput
import re

link_element = re.compile(r'link.+href="(.+)"')
a_element = re.compile(r'a.+href="(.+)"')

for line in fileinput.input():
    # ignore header
    if link_element.search(line) or a_element.search(line):
        line = line.replace('href="', 'href="../')

    sys.stdout.write(line)
