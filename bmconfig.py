#!/usr/bin/python

import os
import sys
from pathlib import Path

def get_template_dir():
    home = os.path.expanduser('~')
    path = Path(home + '/.md2x/beamer-skeleton')
    if path.exists():
        return str(path)
    
    root = os.path.dirname(__file__).replace(os.sep, '/')
    path = Path(root + '/beamer-skeleton')
    if path.exists():
        print(path.name)
        return str(path)
    
    print('No template directory. Aborted.', file=sys.stderr)
    exit(1)

def copy_templates(template_dir, dirs):
    for a in dirs:
        p = Path(a)
        if not p.exists():
            p.mkdir()
        else:
            print(f'The directory already exists: {a}')

        with open(template_dir + '/Makefile', encoding='shift_jis') as fi:
            str = fi.read()
            str = str.replace('{slide_skeleton}', a)
            with open(a + '/Makefile', 'w', encoding='shift_jis') as fo:
                fo.write(str)

        with open(template_dir + '/config.json', encoding='utf-8') as fi:
            str = fi.read()
            with open(a + '/config.json', 'w', encoding='utf-8') as fo:
                fo.write(str)

        with open(template_dir + '/slide-skeleton.md', encoding='utf-8') as fi:
            str = fi.read()
            with open(a + '/' + a + '.md', 'w', encoding='utf-8') as fo:
                fo.write(str)

def main():
    copy_templates(get_template_dir(), sys.argv[1:])
    return 0

if __name__ == '__main__':
    sys.exit(main())
