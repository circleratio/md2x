import re
import sys
import datetime as dt

import const
import html_writer

p_counter = 1
p_in_section_counter = 1
frag = ''
id_base = ''
file_base = ''

def render(doctree, config):
    global id_base
    global file_base
    doctree.result = []
    
    m = re.match(r'([0-9]+)[./]([0-9]+)[./]([0-9]+)', config['date'])
    if m:
        year = int(m.group(1))
        month = int(m.group(2))
        day = int(m.group(3))
        period = 'e'
        if day > 10:
            period = 'm'
        if day > 20:
            period = 'l'
        dateobj = dt.date(year, month, day)
        dow = ['月', '火', '水', '木', '金', '<span class="saturday">土</span>', '<span class="sunday">日</span>'][dateobj.weekday()]
        id_base = 'd{:04}{:02}{:02}'.format(year, month, day)
        file_base = '{:04}{:02}{}.html'.format(year, month, period)
        # print(id_base)
        # print(file_base)
        
    else:
        print("Error: Invalid data format in frontmatter: {}".format(config['date']))
        exit(1)
    
    doctree.result.append('<h2><a id="{}">{}年{}月{}日({})</h2>\n'.format(id_base, year, month, day, dow))
    for di in doctree.body:
        if di.type == const.HEADER1:
            doctree.result.append(output_journal_header1(di))
        elif di.type == const.HEADER2:
            doctree.result.append(output_journal_header2(di))
        elif di.type == const.HEADER3:
            doctree.result.append(output_journal_header3(di))
        elif di.type == const.HEADER4:
            doctree.result.append(output_journal_header4(di))
        elif di.type == const.PARAGRAPH:
            doctree.result.append(output_journal_paragraph(di))
        elif di.type == const.CODE:
            doctree.result.append(output_journal_code(di))
        elif di.type == const.ITEMIZE:
            doctree.result.append(output_journal_itemize(di))
        elif di.type == const.ENUM:
            doctree.result.append(output_journal_enumerate(di))
        else:
            print('Warning: Unknown DocItem: ' + str(di.type), file=sys.stderr)

def parse_flag(str):
    m = re.search('{(.*)}', str)
    if m:
        return(m.group(1))
    return ''
    
def output_journal_header1(di):
    global p_in_section_counter
    global flag
    
    p_in_section_counter = 1
    flag = parse_flag(di.content)
    return ''
    
def output_journal_header2(di):
    global flag
    flag = parse_flag(di.content)
    return ''
    
def output_journal_header3(di):
    global flag
    flag = parse_flag(di.content)
    return ''
    
def output_journal_header4(di):
    global flag
    flag = parse_flag(di.content)
    return ''
    
def output_journal_code(di):
    buf = '<pre>\n'
    for l in di.content:
        buf += l + '\n'
    buf += '</pre>\n'
    return (buf)

def output_journal_itemize(di):
    return(html_writer.output_html_itemize(di))

def output_journal_enumerate(di):
    return(html_writer.output_html_enumerate(di))

def output_journal_paragraph(di):
    global p_counter
    global p_in_section_counter
    buf = ''

    if flag == 's':
        return ''

    text = di.content
    
    # special link (ISBN)
    m = re.search(r'\[([^]]+)\]\(([0-9X]+)\)', text)
    if m:
        text = re.sub(r'\[([^]]+)\]\(([0-9X]+)\)', '\\1<sup><a href="https://www.amazon.co.jp/gp/product/\\2">*</a></sup>', text)

    # ordinary link
    m = re.search(r'\[([^]]+)\]\(([^)]+)\)', text)
    if m:
        text = re.sub(r'\[([^]]+)\]\(([^)]+)\)', '<a href="\\2">\\1</a>', text)

    if p_in_section_counter == 1:
        buf += '<p><a id="{}-{}" href="{}#{}-{}">◆</a>{}</p>\n'.format(id_base, p_counter, file_base, id_base, p_counter, text)
    else:
        buf += '<p>{}</p>\n'.format(text)
    p_counter = p_counter + 1
    p_in_section_counter = p_in_section_counter + 1
    return(buf)
