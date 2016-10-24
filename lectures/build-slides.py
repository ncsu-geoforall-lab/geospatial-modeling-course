#!/usr/bin/env python

# builds pages from source

from __future__ import print_function

import os
import sys
import shutil
import argparse
import re



def ensure_dir(directory):
    """Create all directories in the given path if needed."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def silent_rmtree(filename):
    """Remove the file but do nothing if file does not exist."""
    try:
        shutil.rmtree(filename)
    except OSError as e:
        # errno.ENOENT is "No such file or directory"
        # re-raise if a different error occured
        if e.errno != errno.ENOENT:
            raise

generated_file_info = "<!-- This is a generated file. Do not edit. -->\n"

def error_message(*objs):
    print("ERROR: ", *objs, file=sys.stderr)

def main():

    directories = ['img', 'audio', 'video', 'animations', 'maps', 'data']

    parser = argparse.ArgumentParser(
        description='Creates one page from several files with individual slides and add header and footer.')
    parser.add_argument('files', metavar='slides.html',
                        type=str, nargs='+',
                        help='Files to be concatenated')
    parser.add_argument('--outdir', dest='outdir', action='store',
                        help='Output directory (current working directory by default)')
    parser.add_argument('--outfile', dest='outfile', action='store',
                        help='Output directory', default='index.html')
    parser.add_argument('--title', dest='title', action='store',
                        help='Title of the presentation')
    parser.add_argument('--meta-description', dest='meta_description', action='store',
                        help='Description of the material')
    parser.add_argument('--meta-author', dest='meta_author', action='store',
                        help='Author of the material')
    parser.add_argument('--skip-copy-dirs', dest='skip_copy', action='store_true',
                        help='Do not copy usualy used directories (%s), works only if the directories are in the current working directory' % ', '.join(directories))

    args = parser.parse_args()
    outdir = args.outdir
    outfile = args.outfile
    files = args.files

    title = args.title
    meta_description = args.meta_description
    meta_author = args.meta_author

    # not used
    # enable replacing of path in header?
    css_to_replace = r"['\"]css/"
    js_to_replace = r"['\"]js/"
    lib_to_replace = r"['\"]lib/"

    if not outdir:
        outdir = os.getcwd()

    ensure_dir(outdir)
    outfile = os.path.join(outdir, outfile)

    head = 'head.html'
    foot = 'foot.html'
    if not os.path.exists(head):
        error_message("%s not found" % head)
        return 1
    if not os.path.exists(foot):
        error_message("%s not found" % foot)
        return 1

    with open(outfile, 'w') as outfile:
        with open(head) as infile:
                for line in infile:
                    if title:
                        line = re.sub(r"<title>.*</title>", "<title>" + title + "</title>", line)
                    if meta_description:
                        line = re.sub(r'<meta name="description" content=".*">', r'<meta name="description" content="' + meta_description + '">', line)
                    if meta_author:
                        line = re.sub(r'<meta name="author" content=".*">', r'<meta name="author" content="' + meta_author + '">', line)
                    outfile.write(line)
                    # just to be sure place the comment after doctype and html element
                    # perhaps not needed since we anyway expect HTML5 aware browsers
                    if re.match(r"\s*<html.*>\s*", line):
                        outfile.write(generated_file_info)
        for fname in files:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
            outfile.write(generated_file_info)
        with open(foot) as infile:
                for line in infile:
                    outfile.write(line)

    if not args.skip_copy and os.path.abspath(outdir) != os.getcwd():
        for directory in directories:
            if os.path.exists(directory):
                destination = os.path.join(outdir, directory)
                if os.path.exists(destination):
                    shutil.rmtree(destination)
                shutil.copytree(directory, destination)

    return 0


if __name__ == '__main__':
    sys.exit(main())
