#!/usr/bin/env python

# builds pages from source

from __future__ import print_function

import os
import sys
import shutil
import argparse
import re


def error_message(*objs):
    print("ERROR: ", *objs, file=sys.stderr)

def main():
    directories = ['css', 'js', 'lib', 'plugin']
    
    parser = argparse.ArgumentParser(
        description='Copies the common files for all presentations to one directory')
    parser.add_argument('--src-dir', dest='common_srcdir', action='store',
                        help='Directory with common files to copy from')
    parser.add_argument('--dst-dir', dest='common_dstdir', action='store',
                        required=True,
                        help='Directory to copy common files to')

    args = parser.parse_args()
    srcdir = args.common_srcdir
    dstdir = args.common_dstdir

    if os.path.abspath(dstdir) != os.getcwd():
        for directory in directories:
            if srcdir:
                directory = os.path.join(srcdir, directory)
            destination = os.path.join(dstdir, directory)
            if os.path.exists(destination):
                shutil.rmtree(destination)
            shutil.copytree(directory, destination)

    return 0


if __name__ == '__main__':
    sys.exit(main())
