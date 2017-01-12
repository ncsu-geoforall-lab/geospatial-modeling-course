#!/usr/bin/python

"""

Create a new testing directory::

    mkdir test_documentation
    cd  test_documentation

Create a simlink to the data directory::

    ln -s ../mea582/grass/data data

Generate the test script::

    ./doc2tests.py < .../terrain_analysis.html > test_terrain_analysis.sh
    chmod u+x test_terrain_analysis.sh

In GRASS GIS session::

    ./test_terrain_analysis.sh

Do the cleanup using something like::

    d.mon stop=cairo
    rm *png
    g.remove type=raster,vector patter=* -f
"""

import sys
import re
import fileinput

code_start = re.compile(r'<pre><code>')
code_end = re.compile(r'</code></pre>')

file_content_start = re.compile(r'<pre data-filename=.*>')
file_content_end = re.compile(r'</pre>')
file_name_capture = re.compile(r'<pre data-filename="(.*?)">')

html_comment_start = re.compile(r'\s*<!--')
html_comment_end = re.compile(r'-->')

in_code = False
in_file_content = False
in_html_comment = False
in_code = False

ignored_lines = [
    re.compile(r'grass7.'),
    re.compile(r'cd'),
    re.compile(r'cd.*'),
    #re.compile(r'\s*d\.mon'),
    #re.compile(r'\s*d\.out.file')
]

line_count = 0

common_replacements = [
    (re.compile('&gt;'), '>'),
    (re.compile('&lt;'), '<'),
    (re.compile('&amp;'), '&'),
]

# allow also uppper case tags for now
text_replacemets = [
    (re.compile(r'<p>', re.IGNORECASE), ''),
    (re.compile(r'</p>', re.IGNORECASE), ''),
    (re.compile(r'<br>', re.IGNORECASE), ''),
    (re.compile(r'<div>', re.IGNORECASE), ''),
    (re.compile(r'</div>', re.IGNORECASE), ''),
    (re.compile(r'<a href="([^"]+)">[^<]+</a>', re.IGNORECASE), r'\1'),
    (re.compile(r'^\s+\n$', re.IGNORECASE), '\n'),
]

text_replacemets.extend(common_replacements)

file_path_extraction = re.compile(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', re.IGNORECASE)
file_from_url_extraction = re.compile(r'<a href="([^"]+)/([^"/]+)"[^>]*>([^<]+)</a>', re.IGNORECASE)
download_attribute_presence = re.compile(r'<a href="([^"]+)"[^>]* download[^>]*>([^<]+)</a>', re.IGNORECASE)

code_replacemets = [
    (re.compile('d.mon wx.'), 'd.mon cairo'),
    (re.compile('d.out.file (.+)(.png|)'),
     r'# save the currently rendered image (generated replacement of d.out.file)\ncp map.png \1.png'),
]

code_replacemets.extend(common_replacements)

d_command = re.compile('d\..+ .+')

code_for_beginning = r"""#!/usr/bin/env bash

# Test script generated from documentation

# bash settings suitable for testing (generated code)
# fail on first error
set -e
# print commands before executing
set -o xtrace

# start monitor to render images (generated code)
d.mon cairo
"""

code_for_end = r"""
# end monitor (generated code)
d.mon stop=cairo
"""

replaced_files = []

sys.stdout.write(code_for_beginning)

previous_code_line = None

for line in fileinput.input():
    line_count += 1  # lines are numbered from one

    file_path_match = file_path_extraction.search(line)
    if file_path_match:
        path = file_path_match.group(1)
        name = file_path_match.group(2)
        if not name in replaced_files and not path.startswith('http'):
            print "### >>>", name , path, "### ###"
            replaced_files.append(name)
            code_replacemets.append(
                (re.compile('=' + name), '=' + path))
            code_replacemets.append(
                (re.compile('="' + name + '"'), '="' + path + '"'))
        elif path.startswith('http'):
            print "### ###", path, "### ###"
            if download_attribute_presence.search(line):
                print "### ###", line, "### ###"
                sys.stdout.write(
                    '# download the linked file (generated code)\n'
                    '#wget "%s"\n' % path
                )
                if path.endswith('.zip'):
                    match = file_from_url_extraction.search(line)
                    name = match.group(2)
                    sys.stdout.write(
                    '# uncompress the downloaded file (generated code)\n'
                    'unzip "%s"\n' % name
                )

    if html_comment_start.search(line) and not html_comment_end.search(line):
        in_html_comment = True
    elif html_comment_end.search(line):
        in_html_comment = False
        continue
    # TODO: skip the other parsing if in comment and not end of comment
    elif file_content_start.search(line):
        in_file_content = True
        tmp_file = open(file_name_capture.search(line).group(1), 'w')
        continue
    elif in_file_content and file_content_end.search(line):
        in_file_content = False
        tmp_file.close()
        continue
    elif code_start.search(line):
        in_code = True
        continue
    elif in_code and code_end.search(line):
        in_code = False
        if d_command.search(previous_code_line):
            # line number refers to the original file, not the new one
            sys.stdout.write(
                '# save the currently rendered image (generated code)\n'
                'cp map.png image_line_%d.png' % line_count
            )
        continue

    if in_code:
        line = re.sub('<!--.*-->', '', line)
        skip_line = False
        for ignored_line in ignored_lines:
            if ignored_line.search(line):
                skip_line = True
        if not skip_line:
            #sys.stdout.write("line %d: %s" % (line_count, line)) # debug
            for regexp, replacement in code_replacemets:
                line = regexp.sub(replacement, line)
            sys.stdout.write(line)
        previous_code_line = line
    elif in_html_comment:
        continue
    elif in_file_content:
        tmp_file.write(line)
    else:
        for regexp, replacement in text_replacemets:
            line = regexp.sub(replacement, line)
        if line == '\n':
            sys.stdout.write(line)
        else:
            sys.stdout.write("# %s" % line)

sys.stdout.write(code_for_end)
