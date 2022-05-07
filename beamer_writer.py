#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import string
import random
import re
import sys

from pathlib import Path

from mdfig import mdfig as mf

import const
import latex_writer

frame_opened = False

class TwoPanes:
    def __init__(self):
        self.status = 0
        self.w1 = 0
        self.w2 = 0
        self.type1 = 't'
        self.type2 = 't'

    def set_options(self, s):
        m = re.match('([0-9\.]+),([0-9\.]+),([tf]{2})', s)
        if m:
            self.w1 = m.group(1)
            self.w2 = m.group(2)
            t1 = list(m.group(3))[0]
            t2 = list(m.group(3))[1]
            if t1 == 't':
                self.type1 = 't'
            elif t1 == 'f':
                self.type1 = 'T'
            else:
                print('Warning: Unknown option pane type. Falling back to the default: ' + t1, file=sys.stderr)
            if t2 == 't':
                self.type2 = 't'
            elif t2 == 'f':
                self.type2 = 'T'
            else:
                print('Warning: Unknown option pane type. Falling back to the default: ' + t1, file=sys.stderr)
            
        else:
            print('Error: Unknown option for two panes: ' + s, file=sys.stderr)
            exit(1)

    def activate(self):
        self.status = 1

    def active(self):
        if self.status == 0:
            return False
        return True

    def get_h3_open(self):
        if self.status != 1:
            return ''
        s = '\\begin{columns}[t]\n\\begin{column}[' + self.type1 + ']{' + self.w1 + '\\textwidth}\n'
        self.status = 2
        return s
        
    def get_h3_close(self):
        if self.status != 3:
            return ''
        s = '\\end{column}\n\\end{columns}\n'
        self.status = 0
        return s
        
    def get_hr(self):
        if self.status != 2:
            return ''
        s = '\\end{column}\n\\begin{column}[' + self.type2 + ']{' + self.w2 + '\\textwidth}\n'
        self.status = 3
        return s

def render(doctree, config):
    global frame_opened
    buf = ''
    file = ''
    twopanes = TwoPanes()

    r_file = config['beamer.template']
    r_path = Path(r_file)
    a_file = config['root'] + '/' + config['beamer.template']
    a_path = Path(a_file)
    if r_path.exists():
        file = r_file
    elif a_path.exists():
        file = a_file
    else:
        print('Error: wrong template path in config:beamer.template: {}'.format(file), file=sys.stderr)
        exit(1)
        
    with codecs.open(file, 'r', 'utf_8') as f:
        buf = f.read()

    header = ''
    if 'title' in config:
        header = header + '\\title{' + config['title'] + '}\n'
    if 'subtitle' in config:
        header = header + '\\subtitle{' + config['subtitle'] + '}\n'
    if 'author' in config:
        header = header + '\\author{' + config['author'] + '}\n'
    if 'date' in config:
        header = header + '\\date{' + config['date'] + '}\n'
    if 'beamer.theme' in config:
        buf = buf.replace('<% document_theme %>', config['beamer.theme'])

    buf = buf.replace('<% header %>', header)

    body = ''
    idx = 0
    for di in doctree.body:
        if di.type == const.HEADER1:
            body = body + output_beamer_header1(di, twopanes, config)
        elif di.type == const.HEADER2:
            body = body + output_beamer_header2(di, twopanes)
        elif di.type == const.HEADER3:
            fragile = find_code_block(idx + 1, doctree.body)
            s = di.content
            m = re.match('^(.+) *{2panes: *(.+)}', s)
            if m:
                di.content = m.group(1)
                twopanes.set_options(m.group(2))
                twopanes.activate()
            body = body + output_beamer_header3(di, fragile, twopanes, config)
        elif di.type == const.HEADER4:
            body = body + output_beamer_header4(di)
        elif di.type == const.PARAGRAPH:
            body = body + latex_writer.output_latex_paragraph(di, config)
        elif di.type == const.CODE:
            body = body + output_beamer_code(di)
        elif di.type == const.ITEMIZE:
            body = body + latex_writer.output_latex_itemize(di, config)
        elif di.type == const.ENUM:
            body = body + latex_writer.output_latex_enumerate(di, config)
        elif di.type == const.TABLE:
            body = body + latex_writer.output_latex_table_color(di)
        elif di.type == const.QUOTE:
            body = body + output_beamer_quote(di, config)
        elif di.type == const.HR:
            body = body + output_beamer_hr(di, twopanes)
        elif di.type == const.SPECIAL:
            body = body + output_beamer_special(di)
        else:
            print('Warning: Unknown DocItem: ' + str(di.type), file=sys.stderr)
        idx = idx + 1

    if frame_opened:
        body = body + '\\end{frame}\n\n'
        frame_opened = False

    buf = buf.replace('<% document_body %>', body)
    doctree.result = buf

def output_beamer_hr(di, twopanes):
    if twopanes.active:
        s = twopanes.get_hr()
    else:
        s = '\\rule[1mm]{7.5cm}{0.5mm}\\\\\n'
    return s
    
def find_code_block(idx, body):
    fragile = False
    while idx < len(body):
        type = body[idx].type
        if type == const.CODE:
            # print('found code.')
            fragile = True
            break
        elif type == const.HEADER1 or type == const.HEADER2 or type == const.HEADER3 or type == const.HEADER4:
            break
        idx += 1
    return fragile
    
def output_beamer_header1(di, twopanes, config):
    global frame_opened
    buf = ''
    if frame_opened:
        buf += twopanes.get_h3_close()
        buf = '\\end{frame}\n}\n'
        frame_opened = False
    if di.content == 'title':
        buf += '{\n'
        if 'beamer.bg_titlepage' in config:
            buf += '\\usebackgroundtemplate{\\includegraphics[width=\\paperwidth]{' + config['beamer.bg_titlepage'] + '}}\n'
        buf += '\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n'
        buf += '}\n'
    elif di.content == 'end':
        buf += '{\n'
        if 'beamer.bg_endpage' in config:
            buf += '\\usebackgroundtemplate{\\includegraphics[width=\\paperwidth]{' + config['beamer.bg_endpage'] + '}}\n'
        buf += '\\begin{frame}[plain, t]\n\\endpage\n\\end{frame}\n'
        buf += '}\n'
    elif di.content == 'toc':
        buf += '{\n'
        if 'beamer.bg_toc' in config:
            buf += '\\usebackgroundtemplate{\\includegraphics[width=\\paperwidth]{' + config['beamer.bg_toc'] + '}}\n'
        buf += '\\begin{frame}{目次}\n\\tableofcontents\n\\end{frame}\n'
        buf += '}\n'
    else:
        buf += '\\section{' + di.content + '}\n'
        buf += '{\n'
        if 'beamer.bg_toc' in config:
            buf += '\\usebackgroundtemplate{\\includegraphics[width=\\paperwidth]{' + config['beamer.bg_toc'] + '}}\n'
        buf += '\\begin{frame}{目次}\n\\tableofcontents[currentsection]\n\\end{frame}\n'
        buf += '}\n'
    return(buf)
    
def output_beamer_header2(di, twopanes):
    global frame_opened
    buf = ''
    if frame_opened:
        buf += twopanes.get_h3_close()
        buf = '\\end{frame}\n}\n'
        frame_opened = False
        
    buf += '\\subsection{' + di.content + '}\n'
    return(buf)
    
def output_beamer_header3(di, fragile, twopanes, config):
    global frame_opened
    buf = ''
    
    if frame_opened:
        buf += twopanes.get_h3_close()
        buf += '\\end{frame}\n}\n'

    buf += '{\n'
    if 'beamer.bg' in config:
        buf += '\\usebackgroundtemplate{\\includegraphics[width=\\paperwidth]{' + config['beamer.bg'] + '}}\n'
    if fragile:
        buf += '\\begin{frame}[t, fragile]\n\\frametitle{' + di.content + '}\n'
    else:
        buf += '\\begin{frame}[t]\n\\frametitle{' + di.content + '}\n'

    buf += twopanes.get_h3_open()

    frame_opened = True
    return(buf)
    
def output_beamer_header4(di):
    return('\\paragraph{' + di.content + '}\n')
    
def output_beamer_code(di):
    buf = ''
    
    buf += '\\begin{lstlisting}\n'
    for l in di.content:
        buf += l + '\n'
    buf += '\\end{lstlisting}\n'
    return(buf)

def parse_opt(opts, str):
    list = re.split(',\s*', str)
    for s in list:
        m = re.match('(.*)\s*=\s*(.*)', s)
        if m:
            k = m.group(1)
            v = m.group(2)
            if k == 'w':
                v = float(v) * 297
            if k == 'h':
                v = float(v) * 210
            opts.update({k:v})

def output_beamer_special(di):
    buf = ''
    tmpfile = ''

    # make a unique filename in the work directory
    dat = string.digits + string.ascii_lowercase + string.ascii_uppercase
    while True:
        tmpfile = 'out/' + ''.join([random.choice(dat) for i in range(10)]) + '.pdf'
        if not Path(tmpfile).exists():
            break

    m = re.match('^```(.+)', di.content[0])
    if not m:
        print('Unknown special code: ' + m.group(1), file=sys.stderr)
        return ''
    
    cmd = m.group(1)
    opt = ''
    m = re.match(r'(.*){(.+)}', cmd)
    if m:
        cmd = m.group(1)
        opt = m.group(2)
    
    if cmd == 'tmpl:stepup':
        args = []
        opts = {
            'w': 260,
            'h': 100,
        }
        parse_opt(opts, opt)
        for s in di.content[1:]:
            args.append(re.sub('^ *\* *', '', s))
        size = [0, 0, opts['w'], opts['h']]
        mf.generatePDFFigure(1, size, args, tmpfile)
        buf += '\\begin{center}\n\\includegraphics'
        buf += '[width=\\textwidth]'
        buf += '{' + tmpfile + '}\n'
        buf += '\\end{center}\n'
    elif cmd == 'tmpl:desc':
        args = []
        opts = {
            'w': 260,
            'h': 100,
        }
        parse_opt(opts, opt)
        for s in di.content[1:]:
            m = re.match('^(.*):(.*)', s)
            if m:
                args.append([m.group(1), m.group(2)])
        size = [0, 0, opts['w'], opts['h']]
        mf.generatePDFFigure(2, size, args, tmpfile)
        buf += '\\begin{center}\n\\includegraphics'
        buf += '[width=\\textwidth]'
        buf += '{' + tmpfile + '}\n'
        buf += '\\end{center}\n'
    else:
        print('Unknown special code: ' + m.group(1), file=sys.stderr)
    
        buf += '\\begin{lstlisting}\n'
        for l in di.content[1:]:
            print(f'special:{l}')
            buf += l + '\n'
            buf += '\\end{lstlisting}\n'
    return(buf)

def output_beamer_quote(di, config):
    if 'beamer.quote.width' in config:
        wd = config['beamer.quote.width']
    else:
        wd = '0.85' 

    s = di.content[0]
    m = re.match('^> *{(.*)}',s)
    if m:
        opts = m.group(1).split(',')
        for opt in opts:
            opt = opt.strip()
            m2 = re.match('(.*) *= *(.*)', opt)
            if m2:
                arg = m2.group(1)
                val = m2.group(2)
                # print('arg:{}, val:{}'.format(arg, val))
                if arg == 'w':
                    wd = val
                else:
                    print('Invalid option in quote: ' + opt, file=sys.stderr)
            else:
                print('Invalid option in quote: ' + opt, file=sys.stderr)
        quote_list = di.content[1:]
    else:
        # print('no match')
        quote_list = di.content
    
    buf = ''
    buf += '\\begin{centering}'
    buf += '\\begin{beamercolorbox}[wd=' + wd + '\paperwidth, sep=2pt, rounded=true, shadow=true]{QuoteBox}\n'
    for l in quote_list:
        l = l.replace('> ', '')
        buf += l + '\\par\n'
    buf += '\\end{beamercolorbox}'
    buf += '\\end{centering}\n'
    return(buf)
