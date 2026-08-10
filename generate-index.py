#!/usr/bin/env python3

import re
import sys

argc = len(sys.argv)

# ./generate-index.py title_of_the_page opening_text closing_text \
#     truncate_directory main_list_type [nested_list_type] files...

# truncate_directory removed directory from file names

page_title = sys.argv[1]
start_html = sys.argv[2]
end_html = sys.argv[3]
directory = sys.argv[4]
list_type = sys.argv[5]
sublist_type = sys.argv[6]
if sublist_type in ["ol", "ul"]:
    subheadings = True
    files = sys.argv[7:]
else:
    subheadings = False
    files = sys.argv[6:]

heading = re.compile(r"<[Hh]..*>(.+)</[Hh].>")
heading_num = re.compile(r"<[Hh](.).*>.+</[Hh].>")
heading_subtopic = re.compile(r'<[Hh]..*class=".*subtopic.*".*>(.+)</[Hh].>')

entries = []
subentries = {}

# reads headings (main title and subheadings) from the linked files

for name in files:
    with open(name, "r") as f:
        title = None
        title_num = None
        for line in f:
            match = heading.search(line)
            if match and not title:
                title = match.group(1)
                # TODO: handle with and without /, now only with /
                name = name.removeprefix(directory)
                entries.append((name, title))
                if not subheadings:
                    break
                match = heading_num.search(line)
                if match:
                    title_num = int(match.group(1))
            elif match and subheadings and heading_subtopic.search(line):
                # a subtopic is identified as heading one level lower
                # than the title of the page which has the given class
                subheading = match.group(1)
                match = heading_num.search(line)
                if match:
                    num = int(match.group(1))
                    if title_num - num == -1:
                        if name not in subentries:
                            subentries[name] = []
                        subentries[name].append(subheading)

# writes out the list

sys.stdout.write(f"<h2>{page_title}</h2>\n\n")

sys.stdout.write(start_html)
sys.stdout.write(f"<{list_type}>\n")
for filename, title in entries:
    sys.stdout.write(f'    <li><a href="{filename}">{title}</a></li>\n')
    # write the sublist
    if subheadings and filename in subentries:
        sys.stdout.write(f"<{sublist_type}>\n")
        for subheading in subentries[filename]:
            sys.stdout.write(f"    <li>{subheading}</li>\n")
            sys.stdout.write("</li>\n")
        sys.stdout.write(f"</{sublist_type}>\n")
    sys.stdout.write("</li>\n")
sys.stdout.write(f"</{list_type}>\n")

sys.stdout.write(end_html)
