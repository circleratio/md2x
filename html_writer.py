#import codecs
import re
import sys

import const

def render(doctree, config):
    doctree.result = []
    if config['html.compose_html'] == 'true':
        doctree.result.append('<html>\n<head>\n')
        doctree.result.append(config['html.header'].format(config['title']))
        doctree.result.append('</head>\n<body>\n<h1>{}</h1>\n'.format(config['title']))
    for di in doctree.body:
        if di.type == const.HEADER1:
            doctree.result.append(output_html_header1(di))
        elif di.type == const.HEADER2:
            doctree.result.append(output_html_header2(di))
        elif di.type == const.HEADER3:
            doctree.result.append(output_html_header3(di))
        elif di.type == const.HEADER4:
            doctree.result.append(output_html_header4(di))
        elif di.type == const.PARAGRAPH:
            doctree.result.append(output_html_paragraph(di))
        elif di.type == const.CODE:
            doctree.result.append(output_html_code(di))
        elif di.type == const.ITEMIZE:
            doctree.result.append(output_html_itemize(di))
        elif di.type == const.ENUM:
            doctree.result.append(output_html_enumerate(di))
        elif di.type == const.TABLE:
            doctree.result.append(output_html_table(di))
        else:
            print('Warning: Unknown DocItem: ' + str(di.type), file=sys.stderr)
    if config['html.compose_html'] == 'true':
        doctree.result.append(config['html.footer'])
        doctree.result.append('</body>\n</html>\n')

def output_html_header1(di):
    return('<h2>' + di.content + '</h1>\n')
    
def output_html_header2(di):
    return('<h3>' + di.content + '</h2>\n')
    
def output_html_header3(di):
    return('<h4>' + di.content + '</h3>\n')
    
def output_html_header4(di):
    return('<h5>' + di.content + '</h4>\n')
    
def output_html_code(di):
    buf = ''
    buf += '<pre>\n'
    for l in di.content:
        buf +=  l + '\n'
    buf += '</pre>\n'
    return(buf)

def output_html_itemize(di):
    #depth_prev = 0
    depth = 0
    tab_prev = 0
    tab = 0
    step = 0
    buf = ''
    
    # find step
    for l in di.content:
        m = re.match(r'^( *)[\*\-] *', l)
        if m:
            tab = len(m.group(1))
            if tab > 0:
                step = tab
                break

    buf += '<ul>\n'
    for l in di.content:
        m = re.match(r'^( *)[\*\-] *', l)
        if m:
            tab = len(m.group(1))
            if tab > 0 and step > 0:
                tab = tab // step
            l = re.sub(r'^ *[\*\-] *', '', l)
            if tab > tab_prev:
                for i in range(tab - tab_prev):
                    buf += '<ul>\n'
                    depth = depth + 1
            elif tab_prev > tab:
                for i in range(tab_prev - tab):
                    buf += '</ul>\n'
                    depth = depth - 1
        buf += '<li>' + l + '</li>\n'
#        depth_prev = depth
        tab_prev = tab
    for i in (range(depth + 1)):
        buf += '</ul>\n'
    return(buf)

def output_html_enumerate(di):
    #depth_prev = 0
    depth = 0
    tab_prev = 0
    tab = 0
    step = 0
    buf = ''
    
    # find step
    for l in di.content:
        m = re.match(r'^( *)[0-9]+\. *', l)
        if m:
            tab = len(m.group(1))
            if tab > 0:
                step = tab
                break

    buf += '<ol>\n'
    for l in di.content:
        m = re.match(r'^( *)[0-9]+\. *', l)
        if m:
            tab = len(m.group(1))
            if tab > 0 and step > 0:
                tab = tab // step
            l = re.sub(r'^( *)[0-9]+\. *', '', l)
            if tab > tab_prev:
                for i in range(tab - tab_prev):
                    buf += '<ol>\n'
                    depth = depth + 1
            elif tab_prev > tab:
                for i in range(tab_prev - tab):
                    buf += '</ol>\n'
                    depth = depth - 1
        buf += '<li>' + l + '</li>\n'
        #depth_prev = depth
        tab_prev = tab
    for i in (range(depth + 1)):
        buf += '</ol>\n'
    return(buf)

def output_html_paragraph(di):
    text = di.content

    # special link (ISBN)
    m = re.search(r'\[([^]]+)\]\(([0-9X]+)\)', text)
    if m:
        text = re.sub(r'\[([^]]+)\]\(([0-9X]+)\)', '\\1<sup><a href="https://www.amazon.co.jp/gp/product/\\2">*</a></sup>', text)

    # ordinary link
    m = re.search(r'\[([^]]+)\]\(([^)]+)\)', text)
    if m:
        text = re.sub(r'\[([^]]+)\]\(([^)]+)\)', '<a href="\\2">\\1</a>', text)

    return('<p>\n' + text + '\n</p>\n')

def strip_vertical_bar(s):
    s = re.sub('^\| *', '', s)
    s = re.sub(' *\|$', '', s)
    s = re.sub(' *\| *', '|', s)
    return(s.split('|'))

def output_html_table(di):
    buf = ''

    if len(di.content) < 3:
        print('Error: invalid tabular format.', file=sys.stderr)
        exit(1)
        
    header = strip_vertical_bar(di.content[0])
    
    fmt = strip_vertical_bar(re.sub('-+', '-', di.content[1]))
    align = []
    for s in fmt:
        if s == ':-':
            align.append('left')
        elif s == '-:':
            align.append('right')
        elif s == ':-:':
            align.append('center')
        else:
            align.append('left') # default

    print(align)
    buf += '<table>\n'
    buf += '<tr><th>' + '</th><th>'.join(header) + '</th></tr>\n'
    for l in di.content[2:]:
        l = strip_vertical_bar(l)
        buf += '<tr>\n'
        i = 0
        for item in l:
            buf += '<td align="{}">{}</td>'.format(align[i], item)
            i += 1
        buf += '</tr>\n'
    buf += '</table>'
    return(buf)
