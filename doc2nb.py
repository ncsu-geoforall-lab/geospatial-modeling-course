#!/usr/bin/python

"""

"""

import nbformat as nbf
from nbformat import v4 as nb
import sys
import fileinput
import argparse
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import shlex
import re
import keyword

ignored_lines = [
    # re.compile(r'grass70'),
    re.compile(r'cd'),
    re.compile(r'cd.*'),
    # re.compile(r'\s*d\.mon'),
    # re.compile(r'\s*d\.out.file')
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
#    (re.compile('d.mon wx.'), 'd.mon cairo'),
#    (re.compile('d.out.file (.+)(.png|)'),
#     r'# save the currently rendered image (generated replacement of d.out.file)\ncp map.png \1.png'),
]

#code_replacemets.extend(common_replacements)

d_command = re.compile('d\..+ .+')


class Module(object):
    def __init__(self):
        self.name = None
        self.options = []  # as list to preserve order
        self.flags = ''
        self.long_flags = []
        self.first_option = None
        self.original_string = None

    def uses_option(self, name):
        return name in [key for key, value in self.options]

    # TODO: implement AND and OR relation, now only OR
    def uses_options(self, names):
        keys = [key for key, value in self.options]
        for name in names:
            if name in keys:
                return True
        return False


def string_to_module(string):
    module = Module()
    try:
        tokens = shlex.split(string)
    except ValueError as error:
        raise ValueError("Cannot parse using shell rules (%s): %s" % (error, string))
    module.name = tokens[0]
    module.original_string = string
    for i, token in enumerate(tokens[1:]):
        match = re.search("^([a-z_0-9]+)=(.*)", token)
        if match:
            key = match.group(1)
            value = match.group(2)
            module.options.append((key, value))
            continue
        match = re.search("^-([a-zA-Z0-9]+)", token)
        if match:
            # flag or flags
            flag = match.group(1)
            module.flags += flag
            continue
        match = re.search("^--([a-zA-Z0-9_]+)", token)
        if match:
            flag = match.group(1)
            module.long_flags.append(flag)
            continue
        if not module.options:
            module.first_option = token
    return module


def module_to_python(module):
    first_option_usable = False
    if module.first_option:
        if module.name in ['r.mapcalc']:
            first_option_usable = True
        else:
            # this is just guessing, only safe way is the fallback
            if module.uses_options(('output', 'out')):
                # TODO: do not modify function input
                module.options.insert(0, ('input', module.first_option))
            elif module.name == 'g.region':
                module.options.insert(0, ('region', module.first_option))
            elif module.name == 'd.legend':
                module.options.insert(0, ('raster', module.first_option))
            elif module.name == 'r.stats':  # r.stats has optional output
                module.options.insert(0, ('input', module.first_option))
            elif (module.name.startswith(('d.', 'r.', 'v.')) and
                  module.name not in ['d.out.file']):
                # TODO: do not modify function input
                module.options.insert(0, ('map', module.first_option))
            #elif module.name.startswith('d.'):
            #    # TODO: do not modify function input
            #    module.options.insert(0, ('map', module.first_option))
            #elif module.name.startswith('r.'):
            #    # TODO: do not modify function input
            #    module.options.insert(0, ('input', module.first_option))
            else:
                return "# execute manually the following or its equivalent:\n# %s" % module.original_string
    if first_option_usable:
        # TODO: support r3.mapcalc
        value = module.first_option
        quote = '"'
        if '"' in value:
            quote = "'"
        elif "'" in value:
            quote = '"'
        string = "gs.mapcalc(%s%s%s" % (quote, value, quote)
    elif module.name in ['r.info', 'r.univar', 'v.univar'] or (module.name == 'v.info' and 'c' not in module.flags) or (module.name == 'g.region' and ('p' in module.flags or 'g' in module.flags)):
        if 'g' not in module.flags:
            # TODO: do not modify function input
            module.flags += 'g'
        string = "gs.parse_command('%s'" % module.name
    elif module.name in ['r.category', 'r.report', 'v.info'] or (module.name == 'r.stats' and not module.uses_option('output')):
        string = "print gs.read_command('%s'" % module.name
    else:
        string = "gs.run_command('%s'" % module.name
    
    for key, value in module.options:
        # TODO: customize preferred quote
        quote = '"'
        if '"' in value:
            quote = "'"
        elif "'" in value:
            quote = '"'
        if key in keyword.kwlist:
            key += '_'
        string += ", %s=%s%s%s" % (key, quote, value, quote)

    if module.flags:
        string += ", flags='%s'" % module.flags

    for flag in module.long_flags:
        string += ", %s=True" % (flag)
    string += ')'
    return string

GRASS_START_CODE = """\
import os
import sys
import subprocess
from IPython.display import Image

# create GRASS GIS runtime environment
gisbase = subprocess.check_output(["{grass}", "--config", "path"]).strip()
os.environ['GISBASE'] = gisbase
sys.path.append(os.path.join(gisbase, "etc", "python"))

# do GRASS GIS imports
import grass.script as gs
import grass.script.setup as gsetup

# set GRASS GIS session data
rcfile = gsetup.init(gisbase, "{gisdbase}", "{location}", "{mapset}")
"""

GRASS_SETTINGS_CODE = """\
# default font displays
os.environ['GRASS_FONT'] = 'sans'
# overwrite existing maps
os.environ['GRASS_OVERWRITE'] = '1'
gs.set_raise_on_error(True)
gs.set_capture_stderr(True)
"""

GRASS_START_DISPLAY_CODE = """\
# set display modules to render into a file (named map.png by default)
os.environ['GRASS_RENDER_IMMEDIATE'] = 'cairo'
os.environ['GRASS_RENDER_FILE_READ'] = 'TRUE'
os.environ['GRASS_LEGEND_FILE'] = 'legend.txt'
"""
# gs.run_command('d.mon', start='cairo')

def start_of_grass_session(string, grass, gisdbase, location, mapset):
    return [
        GRASS_START_CODE.strip().format(
            grass=grass, gisdbase=gisdbase, location=location, mapset=mapset),
        GRASS_SETTINGS_CODE.strip(),
        GRASS_START_DISPLAY_CODE.strip(),
        ]


def bash_to_python(string):
    output = []
    prev_line = ''
    d_command_present = False
    last_command = None
    for line in string.splitlines():
        if line:
            if line.endswith('\\'):
                prev_line += line + "\n"
                continue
            elif prev_line:
                line = prev_line + line
                prev_line = ''
            module = string_to_module(line)
            # TODO: potentially split to cells when d.out.file
            if module.name == 'd.out.file':
                output.append('Image(filename="map.png")')
            else:
                output.append(module_to_python(module))
                if module.name.startswith('d.'):
                    d_command_present = True
            last_command = module.name
        else:
            output.append("\n")
    if d_command_present and last_command != 'd.out.file':
        output.append('Image(filename="map.png")')
    return ["\n".join(output)]


class DocumentationDocument(object):
    pass

# TODO: it would be probably better to first split document into
# blocks/cells of code and text and than convert each of the items
# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self, grass, gisdbase, location, mapset):
        HTMLParser.__init__(self)
        self.pre_opened = False
        self.code_opened = False
        self.close_pre = False
        self.close_code = False
        self.handle_pre_start = False
        self.handle_pre_end = False
        
        self.in_pre = False
        self.in_code = False
        self.in_code_block = False
        self.in_precode = False

        self.pre_data_run_no = False
        self.pre_to_file = None

        self.in_file_content = False
        self.in_html_comment = False

        self.nb = nb.new_notebook()
        self.nb['metadata']['kernelspec'] = {
            "display_name": "Python 2",
            "language": "python",
            "name": "python2"
        }

        self.data = ''
        # used to carry hyperlink data
        self.link_url = None

        self.download_files = []

        # to be refactored to a writer class
        self.grass = grass
        self.gisdbase = gisdbase
        self.location = location
        self.mapset = mapset

    def flush_text(self):
        # process text
        cell = self.data.strip()
        if cell:
            self.nb['cells'].append(nb.new_markdown_cell(cell))
            self.data = ''

    def add_file_downloads(self):
        cell = "# a proper directory is already set, download files\nimport urllib\n"
        for file in self.download_files:
            name = file.split('/')[-1]
            cell += 'urllib.urlretrieve("%s", "%s")\n' % (file, name)
        cell = cell.strip()
        download_text_index = None
        for i, existing_cell in enumerate(self.nb['cells']):
            if existing_cell.source.startswith("Download all text files"):
                download_text_index = i
                break
        if download_text_index is None:
            # TODO: better guess than 2?
            self.nb['cells'].insert(2, nb.new_code_cell(cell))
        else:
            # insert before
            self.nb['cells'].insert(download_text_index, nb.new_code_cell(cell))
            if not self.nb['cells'][download_text_index - 1].source:
                del self.nb['cells'][download_text_index - 1]

    def finish_session(self):
        code = "# end the GRASS session\nos.remove(rcfile)"
        self.nb['cells'].append(nb.new_code_cell(code))

    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag:", tag, attrs
        code_block_started = False
        if tag == 'pre':
            self.pre_opened = True
            self.handle_pre_start = True
            self.in_pre = True
            for key, value in attrs:
                if key == 'data-run' and value == 'no':
                    self.pre_data_run_no = True
                    break
                if key == 'data-filename':
                    self.pre_to_file = value
            if self.pre_to_file:
                self.handle_pre_start = False
                self.pre_opened = False
                self.in_code_block = True
                code_block_started = True
        if tag == 'code':
            self.code_opened = True
            self.in_code = True
            if self.in_pre:
                self.code_opened = False
                self.in_precode = True
                if not self.pre_data_run_no:
                    self.in_code_block = True
                    code_block_started = True
                    self.handle_pre_start = False

        if code_block_started:
            self.flush_text()

        if not self.in_code_block:
            if tag != 'pre' and self.handle_pre_start:
                self.data += "```"#START"
                self.handle_pre_start = False
                self.handle_pre_end = True
            if re.search("^h(\d)$", tag):
                # TODO: check std heading syntax
                nchars = int(tag[1])
                self.data += '#' * nchars + " "
            elif tag == 'li':
                if self.data[-1] != "\n":
                    self.data += "\n"
                self.data += '* '
            elif tag == 'em':
                # TODO: more robust test
                # TODO: list to module
                # if 'class' in attrs and 'module' in attrs['class']:
                self.data += '_'
            elif tag == 'a':
                self.data += '['
                # possibly just store last tag attrs
                for key, value in attrs:
                    if key == 'href':
                        self.link_url = value
                        break
            elif tag == 'code':
                self.data += '`'
            #elif tag == 'blockquote':
            #    self.data += '\n\n\t'


    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag

        code_block_ended = False
        if tag == 'pre':
            self.in_pre = False
            if self.in_code_block and self.in_codepre:
                code_block_ended = True
            self.pre_data_run_no = False
            if self.pre_to_file:
                code_block_ended = True
        if tag == 'code':
            self.in_code = False
            if self.in_code_block and self.in_precode:
                code_block_ended = True

        #if tag == 'blockquote':
        #    self.data += "\n\n"
        if tag == 'em':
             self.data += '_'
        elif tag == 'a':
            # TODO: URLs need adding http://ncsu-geoforall-lab.github.io/geospatial-modeling-course/grass/ if relative
            self.data += '](%s)' % self.link_url
            if self.link_url.startswith('data/'):
                self.download_files.append("http://ncsu-geoforall-lab.github.io/geospatial-modeling-course/grass/" + self.link_url)
            self.link_url = None
        elif tag == 'pre' and self.handle_pre_end:
            self.data += '```'#END'
            self.handle_pre_end = False
        elif tag == 'code' and not self.in_code_block:
            self.data += '`'

        if code_block_ended:
            cell = ''
            self.in_code_block = False
            self.in_precode = False
            self.in_codepre = False
            if self.pre_to_file:
                # process pre content as file
                cell = "%%%%file %s\n%s" % (self.pre_to_file, self.data.strip())
                self.nb['cells'].append(nb.new_code_cell(cell))
                self.data = ''
                self.pre_to_file = None
                return
            for line in self.data.splitlines():
                line = re.sub('<!--.*-->', '', line)
                skip_line = False
                for ignored_line in ignored_lines:
                    if ignored_line.search(line):
                        skip_line = True
                if not skip_line:
                    #sys.stdout.write("line %d: %s" % (line_count, line)) # debug
                    for regexp, replacement in code_replacemets:
                        line = regexp.sub(replacement, line)
                    if line:
                        cell += line + "\n"
                previous_code_line = line
            if re.search('^grass.?.?$', cell):
                cells = start_of_grass_session(
                    cell, self.grass, self.gisdbase, self.location, self.mapset)
            else:
                cells = bash_to_python(cell.strip())
            #print cell
            for cell in cells:
                self.nb['cells'].append(nb.new_code_cell(cell))
            self.data = ''

    def handle_data(self, data):
        #print "Encountered some data  :", data
        if not self.in_code_block and self.handle_pre_start:
            self.data += "```"#DATA>>>" + data + "<<<"
            self.handle_pre_start = False
            self.handle_pre_end = True
        self.data += data

    def handle_entityref(self, name):
        if not self.in_code_block and self.handle_pre_start:
            self.data += "```ENTITY"
            self.handle_pre_start = False
            self.handle_pre_end = True
        if name == 'ndash':
            self.data += "--"
        else:
            c = unichr(name2codepoint[name])
            #print "Named ent:", c
            self.data += c

    def handle_comment(self, data):
        #print "Encountered some data  :", data
        if self.in_code_block and data.strip().startswith('d.erase'):
            self.data += data

# instantiate the parser and fed it some HTML


def main():
    parser = argparse.ArgumentParser(description='Convert HTML documentation to Jupyter Notebook.')
    parser.add_argument('files', metavar='FILE', nargs='+',
                        help='Files to convert')
    # TODO: allow no provided
    # TODO: allow mapset as full path
    parser.add_argument('--grass', dest='grass', default='grass',
                        help='GRASS GIS executable')
    parser.add_argument('--gisdbase', dest='gisdbase', required=True,
                        help='GRASS GIS Database')
    parser.add_argument('--location', dest='location', required=True,
                        help='GRASS GIS Location')
    parser.add_argument('--mapset', dest='mapset', required=True,
                        help='GRASS GIS Mapset')
    args = parser.parse_args()
    input_ = args.files[0]
    output = args.files[1]

    parser = MyHTMLParser(args.grass, gisdbase=args.gisdbase, location=args.location, mapset=args.mapset)
    parser.feed(open(input_).read())
    parser.flush_text()
    parser.add_file_downloads()
    parser.finish_session()

    with open(output, 'w') as f:
        nbf.write(parser.nb, f)


if __name__ == '__main__':
    main()
