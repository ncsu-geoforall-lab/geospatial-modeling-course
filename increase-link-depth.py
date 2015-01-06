#!/usr/bin/python

import sys
import fileinput
import re

link_element = re.compile(r'link.+href="(.+)"')
a_element = re.compile(r'a.+href="(.+)"')
img_element = re.compile(r'img.+src="(.+)"')

protocols = ['http://', 'https://', 'ftp://']

def is_absolute(line):
    for protocol in protocols:
        if protocol in line:
            return True
    return False

for line in fileinput.input():
    # ignore header
    if link_element.search(line) or a_element.search(line) and not is_absolute(line):
        line = line.replace('href="', 'href="../')
    if img_element.search(line) and not is_absolute(line):
        line = line.replace('src="', 'src="../')
    sys.stdout.write(line)
