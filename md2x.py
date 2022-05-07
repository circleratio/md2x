#!/usr/bin/python
# -*- coding: utf-8 -*-

CONFIG_FILE = 'config.json'

import argparse
import codecs
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

import html_writer
import latex_writer
import text_writer
import journal_writer
import beamer_writer
import const
import util

class DocTree:
    def __init__(self, frontmatter, body):
        self.options = {
            'title':'',
            'author':'',
            'date':'',
        }
        
        self.get_options(frontmatter)
        if args.verbose:
            self.print_options()
        
        self.body = parse_body(body)
        self.result = []
        
    def get_options(self, fm):
        for l in fm:
            r = r'(?P<key>^[^:]+): *(?P<value>.*)'
            m = re.search(r, l)
            self.options.update({m.group('key') : m.group('value')})
            config.update({m.group('key') : m.group('value')})
        if self.options['date'] == 'today':
            dobj = dt.datetime.today()
            self.options['date'] = '{}.{}.{}'.format(dobj.year, dobj.month, dobj.day)
            config.update({'date' : '{}.{}.{}'.format(dobj.year, dobj.month, dobj.day)})
            
    def print_options(self):
        for key, value in self.options.items():
            print('{}={}'.format(key, value), file=sys.stderr)

    def write(self, path):
        with codecs.open(path, 'w', 'utf_8') as f:
            f.write(''.join(self.result))
                
    def print(self):
        for l in self.result:
            print(l)
            
class DocItem:
    def __init__(self, type, content):
        i = 0
        self.type = type
        self.content = []
        if type == const.HEADER1 or type == const.HEADER2 or type == const.HEADER3 or type == const.HEADER4:
            if args.verbose:
                print(str(type) + ':' + content, file=sys.stderr)
            self.content = content
        elif type == const.PARAGRAPH:
            if args.verbose:
                print(str(type) + ':' + content, file=sys.stderr)
            self.content = content
        elif type == const.CODE:
            self.content = content
        elif type == const.ITEMIZE:
            self.content = content
        elif type == const.ENUM:
            self.content = content
        elif type == const.SPECIAL:
            self.content = content
        elif type == const.TABLE:
            self.content = content
        elif type == const.QUOTE:
            self.content = content
        elif type == const.HR:
            self.content = content
        else:
            print(str(type) + ':' + 'not supported yet', file=sys.stderr)

def parse_markdown(list):
    frontmatter = []
    body = []
    if re.match(r'^---', list[0]):
        if args.verbose:
            print("A frontmatter found.", file=sys.stderr)
        i = 1
        while i < len(list):
            if re.match(r'^---', list[i]):
                break
            i += 1

            if i == len(list):
                print("Error: Invalid frontmatter.", file=sys.stderr)
                quit()
            else:
                frontmatter = list[1:i]
                body = list[i + 1:]
    else:
        if args.verbose:
            print("A frontmatter not found.", file=sys.stderr)
        body = list
             
    doctree = DocTree(frontmatter, body)

    return doctree

def parse_body(content):
    buf = []
    str = ''
    children = []
    i = 0
    
    while content[i] == '':
        i += 1
        
    while i < len(content):
        if (re.match('^```\\S+', content[i])):
            buf.append(content[i])
            if args.verbose:
                print('special: ' + content[i], file=sys.stderr)
            i += 1
            while not re.match('^```', content[i]):
                buf.append(content[i])
                if args.verbose:
                    print('special: ' + content[i], file=sys.stderr)
                i += 1
            children.append(DocItem(const.SPECIAL, buf))
            buf = []
            i += 1
            continue
        
        if (re.match('^```', content[i])):
            buf.append(content[i])
            if args.verbose:
                print('code: ' + content[i], file=sys.stderr)
            i += 1
            while not re.match('^```', content[i]):
                buf.append(content[i])
                if args.verbose:
                    print('code: ' + content[i], file=sys.stderr)
                i += 1
            children.append(DocItem(const.CODE, buf[1:]))
            buf = []
            i += 1
            continue
                
        m = re.match('^([\* ]{3})|([- ]{3})', content[i])
        if m:
            children.append(DocItem(const.HR, ''))
            i += 1
            continue
        
        m = re.match('^#$', content[i])
        if m:
            children.append(DocItem(const.HEADER1, ''))
            i += 1
            continue

        m = re.match('^# +(.*)', content[i])
        if m:
            children.append(DocItem(const.HEADER1, m.group(1)))
            i += 1
            continue
            
        m = re.match('^## +(.*)', content[i])
        if m:
            children.append(DocItem(const.HEADER2, m.group(1)))
            i += 1
            continue
            
        m = re.match('^### +(.*)', content[i])
        if m:
            children.append(DocItem(const.HEADER3, m.group(1)))
            i += 1
            continue
            
        m = re.match('^#### +(.*)', content[i])
        if m:
            children.append(DocItem(const.HEADER4, m.group(1)))
            i += 1
            continue

        if (re.match('^ *[\*\-]', content[i])):
            while i < len(content) and re.match('^ *[\*\-]', content[i]):
                buf.append(content[i])
                if args.verbose:
                    print('itemize: ' + content[i], file=sys.stderr)
                i += 1
            children.append(DocItem(const.ITEMIZE, buf))
            buf = []
            continue

        if (re.match('^ *[0-9]+\.', content[i])):
            while i < len(content) and re.match('^ *[0-9]+\.', content[i]):
                buf.append(content[i])
                if args.verbose:
                    print('enum: ' + content[i], file=sys.stderr)
                i += 1
            children.append(DocItem(const.ENUM, buf))
            buf = []
            continue

        if (re.match('^> .*', content[i])):
            while i < len(content) and re.match('^> .*', content[i]):
                buf.append(content[i])
                if args.verbose:
                    print('quote: ' + content[i], file=sys.stderr)
                i += 1
            children.append(DocItem(const.QUOTE, buf))
            buf = []
            continue

        if (re.match('^\|.*', content[i])):
            while i < len(content) and re.match('^\|.*', content[i]):
                buf.append(content[i])
                if args.verbose:
                    print('table: ' + content[i], file=sys.stderr)
                i += 1
            children.append(DocItem(const.TABLE, buf))
            buf = []
            continue

        delimiter = r'(^```)|(^ *\*)|(^ *[0-9]+\.)|(^> .*)|(^\|.*)'
        while i < len(content) and (content[i] != '' and not re.match(delimiter, content[i])):
            str = str + content[i]
            i += 1
        if str != '':
            children.append(DocItem(const.PARAGRAPH, str))
        str = ''
            
        if i < len(content) and re.match(delimiter, content[i]):
            if args.verbose:
                print('<break*>', file=sys.stderr)
            continue
        
        if i < len(content) and content[i] == '':
            if args.verbose:
                print('<break>', file=sys.stderr)
            i += 1
            continue
        
    return children                        

def parse_arg():
    parser = argparse.ArgumentParser(
        prog='md2x.py',
        usage='md2x [options] [inputFile]',
        description='Convert Markdown files to another format.',
        epilog='end',
        add_help=True)
    
    parser.add_argument('-v', '--verbose',
                        help='Enable vervose mode.',
                        action='store_true')
    parser.add_argument('--text',
                        help='Output a text file.',
                        action='store_true')
    parser.add_argument('--html',
                        help='Output a HTML file.',
                        action='store_true')
    parser.add_argument('--journal',
                        help='Output a journal file.',
                        action='store_true')
    parser.add_argument('--latex',
                        help='Output a LaTeX file.',
                        action='store_true')
    parser.add_argument('--beamer',
                        help='Output a Beamer/LaTeX file.',
                        action='store_true')
    parser.add_argument('--cflags',
                        help='Compile flags.',
                        default='')
    parser.add_argument('-o', '--output',
                        help='Output file.',
                        default='')
    parser.add_argument('inputFile', help='Input files', nargs='*')
    
    args = parser.parse_args()
    
    return args

def print_arg(args):
    print('inputFile: ' + str(args.inputFile), file=sys.stderr)
    print('verbose: ' + str(args.verbose), file=sys.stderr)
    print('html: ' + str(args.html), file=sys.stderr)
    print('journal: ' + str(args.journal), file=sys.stderr)
    print('latex: ' + str(args.latex), file=sys.stderr)
    print('beamer: ' + str(args.beamer), file=sys.stderr)
    print('output: ' + args.output, file=sys.stderr)
    print('cflags: ' + args.cflags, file=sys.stderr)

def make_filename(pathname, suffix, args):
    if args.output != '':
        return args.output
    
    path = Path(pathname)
    return (path.parent.joinpath(path.stem + suffix))

#
# main
#
args = parse_arg()
if args.verbose:
    print_arg(args)

# system config file
root = os.path.dirname(__file__).replace(os.sep, '/')
path = Path(root + '/' + CONFIG_FILE)
if path.exists():
    if args.verbose:
        print('System config file: {}'.format(path.resolve()), file=sys.stderr)
    js = open(path, 'r', encoding='utf-8')
    config = json.load(js)
    config['root'] = root
else:
    print('Error: System config file is not found.', file=sys.stderr)
    exit(1)

# user config file
home = os.path.expanduser('~')
path = Path(home + '/.md2x/' + CONFIG_FILE)
if path.exists():
    if args.verbose:
        print('User config file: {}'.format(path.resolve()), file=sys.stderr)
    js = open(path, 'r', encoding='utf-8')
    config_user = json.load(js)
    config.update(config_user)

# config file in working directory
path = Path(CONFIG_FILE)
if path.exists():
    if args.verbose:
        print('Config file in work directory: {}'.format(path.resolve()), file=sys.stderr)
    js = open(path, 'r', encoding='utf-8')
    config_work = json.load(js)
    config.update(config_work)

if 'clipart_path' in config:
    config['clipart_path'] = config['clipart_path'] + ';' + 'clipart'
else:
    config['clipart_path'] = 'clipart'

if len(args.inputFile) == 0:
    md_text_list = sys.stdin.readlines()
    md_text_list = [line.rstrip() for line in md_text_list]
    doctree = parse_markdown(md_text_list)
    html_writer.render(doctree, config)
    doctree.print()
    exit(0)
    
for file in args.inputFile:
    path = Path(file)
    md_text_list = []
    if path.exists():
        with codecs.open(file, 'r', 'utf_8') as f:
            rawlist = f.readlines()
            md_text_list = [s.rstrip() for s in rawlist]
            md_text_list = util.preprocess(md_text_list, args.cflags, config)
       
        doctree = parse_markdown(md_text_list)
        if args.text:
            text_writer.render(doctree, config)
            doctree.write(make_filename(path, '.txt', args))
        if args.html:
            html_writer.render(doctree, config)
            doctree.write(make_filename(path, '.html', args))
        if args.journal:
            journal_writer.render(doctree, config)
            doctree.write(make_filename(path, '.html', args))
        if args.latex:
            latex_writer.render(doctree, config)
            doctree.write(make_filename(path, '.tex', args))
        if args.beamer:
            beamer_writer.render(doctree, config)
            doctree.write(make_filename(path, '.tex', args))
    else:
        print("File doesn't exist: " + file, file=sys.stderr)
