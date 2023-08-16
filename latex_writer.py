import codecs
import re
import sys

from pathlib import Path

import const
import util

def render(doctree, config):
    doctree.result = []
    file = ''
    
    r_file = config['latex.template']
    r_path = Path(r_file)
    a_file = config['root'] + '/' + config['latex.template']
    a_path = Path(a_file)
    if r_path.exists():
        file = r_file
    elif a_path.exists():
        file = a_file
    else:
        print('Error: wrong template path in config:latex.template: {}'.format(file), file=sys.stderr)
        exit(1)
        
    with codecs.open(file, 'r', 'utf_8') as f:
        buf = f.read()

    header = ''
    if 'title' in config:
        header += '\\title{' + config['title'] + '}\n'
    if 'subtitle' in config:
        header += '\\subtitle{' + config['subtitle'] + '}\n'
    if 'author' in config:
        header += '\\author{' + config['author'] + '}\n'
    if 'date' in config:
        header += '\\date{' + config['date'] + '}\n'
    buf = buf.replace('<% header %>', header)
    
    if 'latex.footer.right' in config:
        buf = buf.replace('<% footer_right %>', config['latex.footer.right'])
    else:
        buf = buf.replace('<% footer_right %>', '')
    if 'latex.footer.left' in config:
        buf = buf.replace('<% footer_left %>', config['latex.footer.left'])
    else:
        buf = buf.replace('<% footer_right %>', '')
    
    body = ''
    for di in doctree.body:
        if di.type == const.HEADER1:
            body += output_latex_header1(di)
        elif di.type == const.HEADER2:
            body += output_latex_header2(di)
        elif di.type == const.HEADER3:
            body += output_latex_header3(di)
        elif di.type == const.HEADER4:
            body += output_latex_header4(di)
        elif di.type == const.PARAGRAPH:
            body += output_latex_paragraph(di, config)
        elif di.type == const.CODE:
            body += output_latex_code(di)
        elif di.type == const.ITEMIZE:
            body += output_latex_itemize(di, config)
        elif di.type == const.ENUM:
            body += output_latex_enumerate(di, config)
        elif di.type == const.TABLE:
            body += output_latex_table(di)
        else:
            print('Warning: Unknown DocItem: ' + str(di.type), file=sys.stderr)
    buf = buf.replace('<% document_body %>', body)
    doctree.result = buf

def output_latex_header1(di):
    if di.content == 'toc':
        return('\\tableofcontents')
    elif di.content == 'newpage':
        return('\\newpage')
    return('\\section{' + di.content + '}\n')
    
def output_latex_header2(di):
    return('\\subsection{' + di.content + '}\n')
    
def output_latex_header3(di):
    return('\\subsubsection{' + di.content + '}\n')
    
def output_latex_header4(di):
    return('\\paragraph{' + di.content + '}\n')
    
def output_latex_code(di):
    buf = ''
    buf += '\\begin{lstlisting}[basicstyle=\\ttfamily\\footnotesize, frame=single]\n'
    for l in di.content:
        l = l.replace('\\', '\\{backslash}')
        buf += l + '\n'
    buf = buf + '\\end{lstlisting}\n'
    return(buf)

def output_latex_itemize(di, config):
    buf = ''
    opt = ''

    m = re.match(r'^\* *{ *([a-z]+) *}', di.content[0])
    if m:
        fmt = m.group(1)
        arg = di.content[1:]
        m = re.match(r'^\* *{ *([a-z]+) *}{ *([a-z0-9=, \.]+) *}', di.content[0])
        if m:
            opt = m.group(2)
    else:
        fmt = 'regular'
        arg = di.content

    res = parse_itemize(arg, config)
    if fmt == 'regular':
        buf += latex_itemize_regular(res, config)
    elif fmt == 'table':
        buf += latex_itemize_table(res, opt, config)

    return(buf)

def parse_itemize(content, config):
    step = 0
    depth = 0
    tab_prev = 0
    tab = 0
    
    # find the step size
    for l in content:
        m = re.match(r'^( *)[\*\-] *', l)
        if m:
            tab = len(m.group(1))
            if tab > 0:
                step = tab
                break
    
    result = []
    for l in content:
        m = re.match(r'^( *)[\*\-] *', l)
        if m:
            tab = len(m.group(1))
            if tab > 0 and step > 0:
                tab = tab // step
            l = re.sub(r'^ *[\*\-] *', '', l)
            if tab > tab_prev:
                for i in range(tab - tab_prev):
                    depth += 1
            elif tab_prev > tab:
                for i in range(tab_prev - tab):
                    depth -= 1
        result.append([depth, format_text(l, config)])
        
        tab_prev = tab

    return result

def latex_itemize_regular(items, config):
    prev_depth = 0
    buf = '\\begin{itemize}\n'

    for l in items:
        depth = l[0]
        s = l[1]
        if depth > prev_depth:
            buf += '\\begin{itemize}\n'
        if depth < prev_depth:
            for i in range(prev_depth - depth):
                buf +=  '\\end{itemize}\n'
        buf += '\item ' + s + '\n'
        prev_depth = depth
        
    for i in (range(depth + 1)):
        buf += '\\end{itemize}\n'

    return buf

def latex_itemize_table(items, opt, config):
    prev_depth = 0
    w1 = '0.4'
    w2 = '0.6'
    vspace_top = '1.5mm'
    vspace_bottom = '0.5mm'
    buf = ''
    
    m = re.match(r'^([0-9\.]+), *([0-9\.]+)', opt)
    if m:
        w1 = m.group(1)
        w2 = m.group(2)

    # buf += '\\vspace{' + vspace_top + '}\n'
    buf += '\\begin{table}\n'
    buf += '\\centering\n'
    buf += '\\begin{tabular}{|c|l|}\n'

    for l in items:
        depth = l[0]
        s = l[1]
        if depth == 0:
            if prev_depth != 0:
                buf += '\\end{itemize}\n'
                buf += '\\vspace{' + vspace_bottom + '}\n'
                buf += '\\end{minipage} \\\\ \n'
            buf += '\\hline\n'
            buf += '\\begin{minipage}{' + w1 + '\\textwidth}\n'
            buf += s + '\n'
            buf += '\\end{minipage} &\n'
        else:
            if prev_depth == 0:
                buf += '\\begin{minipage}{' + w2 + '\\textwidth}\n'
                buf += '\\vspace{' + vspace_top + '}\n'
                buf += '\\begin{itemize}\n'
            buf += '\\item ' + s + '\n'
        prev_depth = depth
        
    buf += '\\end{itemize}\n'
    buf += '\\vspace{' + vspace_bottom + '}\n'
    buf += '\\end{minipage} \\\\ \n'
    buf += '\\hline\n'
    buf += '\\end{tabular}\n'
    buf += '\\end{table}\n'

    return buf

def output_latex_enumerate(di, config):
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

    buf += '\\begin{enumerate}\n'
    for l in di.content:
        m = re.match(r'^( *)[0-9]+\. *', l)
        if m:
            tab = len(m.group(1))
            if tab > 0 and step > 0:
                tab = tab // step
            l = re.sub(r'^( *)[0-9]+\. *', '', l)
            if tab > tab_prev:
                for i in range(tab - tab_prev):
                    buf += '\\begin{enumerate}\n'
                    depth = depth + 1
            elif tab_prev > tab:
                for i in range(tab_prev - tab):
                    buf += '\\end{enumerate}\n'
                    depth -= 1
        buf += '\item ' + format_text(l, config) + '\n'
        tab_prev = tab
    for i in (range(depth + 1)):
        buf += '\\end{enumerate}\n'
    return(buf)

def generate_latex_option(str):
    result_type = 0
    rel_w = ''
    rel_h = ''
    rel_s = ''
    abs_w = ''
    abs_x = ''
    abs_y = ''
    
    for s in re.split(', *', str):
        m = re.match('([a-z]+) *= *([0-9\\.]+)$', s)
        if m:
            key = m.group(1)
            val = m.group(2)
            if key == 'width':
                rel_w = f'width={val}\\textwidth'
                abs_w = f'{val}\\textwidth'
            elif key == 'w':
                rel_w = f'width={val}\\textwidth'
                abs_w = f'{val}\\textwidth'
            elif key == 'height':
                rel_h = f'height={val}\\textheight'
            elif key == 'h':
                rel_h = f'height={val}\\textheight'
            elif key == 's':
                rel_s = f'scale={val}'
            elif key == 'x':
                abs_x = val
                result_type = 1
            elif key == 'y':
                abs_y = val
                result_type = 1
            else:
                print('Warning: unknown option for graphics:' + s, file=sys.stderr)

    if result_type == 0:
        res = []
        if rel_w != '':
            res.append(rel_w)
        if rel_h != '':
            res.append(rel_h)
        if rel_s != '':
            res.append(rel_w)
        res_rel = ','.join(res)
        res_abs = ''

    if result_type == 1:
        res_abs = '{' + abs_w + '}(' + abs_x + 'pt,' + abs_y + 'pt)'
        res_rel = 'width=\\textwidth'

    return [result_type, res_rel, res_abs]

def format_text(text, config):
    text = escape_latex_directive(text)
    
    m = re.search(r'\*\*([^\*]+)\*\*', text)
    if m:
        text = re.sub(r'\*\*([^\*]+)\*\*', '\\\\textgt{\\1}', text)
        
    m = re.search(r'__([^_]+)__', text)
    if m:
        text = re.sub(r'__([^_]+)__', '\\\\textgt{\\1}', text)
        
    m = re.search(r'~~([^~]+)~~', text)
    if m:
        text = re.sub(r'~~([^~]+)~~', '\\\\sout{\\1}', text)
        
    m1 = re.search(r'!\[([^]]+)\]\(([^)]+)\)', text)
    m2 = re.search(r'\[([^]]+)\]\(([^)]+)\)', text)
    m3 = re.search(r'\[\]\(([^)]+)\)', text)
    if m1 or m2 or m3:
        if m1:
            f = util.find_file(m1.group(2), 'clipart_path', config)
            [t, opt_rel, opt_abs] = generate_latex_option(m1.group(1))
        
            opt_rel = opt_rel.replace('\\', '\\\\')
            opt_abs = opt_abs.replace('\\', '\\\\')
            if t == 0:
                text = re.sub(r'!\[([^]]+)\]\(([^)]+)\)', '\\\\begin{center}\\n\\\\includegraphics[' + opt_rel + ']{' + f + '}\\n\\\\end{center}\\n', text)
            elif t == 1:
                text = re.sub(r'!\[([^]]+)\]\(([^)]+)\)', '\\\\begin{textblock*}' + opt_abs + '\\n\\\\centering\\\\includegraphics[' + opt_rel + ']{' + f + '}\\n\\\\end{textblock*}\\n', text)

        if m2:
            s = '\\\\href{' + url_quote(m2.group(2)) + '}{' + m2.group(1) + '}\n'
            text = re.sub(r'\[([^]]+)\]\(([^)]+)\)', s, text)
        
        if m3:
            s = '\\\\url{' + url_quote(m3.group(1)) + '}\n'
            text = re.sub(r'\[\]\(([^)]+)\)', s, text)
    else:
        m = re.search(r'#', text)
        if m:
            text = re.sub(r'#', '\\#', text)
    
    return text

def escape_latex_directive(text):
    text = text.replace('&', '\&')
    return(text)

def url_quote(url):
    url = url.replace('_', '\_')
    url = url.replace('%', '\%')
    return(url)

def output_latex_paragraph(di, config):
    text = format_text(di.content, config)
    return(text + '\n\n')

def output_latex_quote(di, config):
    buf = ''
    buf += '\\begin{quote}'
    for l in di.content:
        l = l.replace('> ', '')
        buf += l + '\\par\n'
    buf += '\\end{quote}'
    return(buf)

def strip_vertical_bar(s):
    s = re.sub('^\| *', '', s)
    s = re.sub(' *\|$', '', s)
    s = re.sub(' *\| *', '|', s)
    return(s.split('|'))

def output_latex_table(di):
    buf = ''

    if len(di.content) < 3:
        print('Error: invalid tabular format.', file=sys.stderr)
        exit(1)
        
    header = strip_vertical_bar(di.content[0])
    fmt = strip_vertical_bar(re.sub('-+', '-', di.content[1]))

    tex_fmt = ''
    for s in fmt:
        if s == ':-':
            tex_fmt += 'l'
        elif s == '-:':
            tex_fmt += 'r'
        elif s == ':-:':
            tex_fmt += 'c'
        else:
            tex_fmt += 'c'
            
    buf += '\\begin{table}[hbtp]\n'
    buf += '\\centering\n'
    buf += '\\begin{tabular}{' + tex_fmt + '}\n'
    buf += '\\toprule\n'
    buf += ' & '.join(header) + '\\\\\n'
    buf += '\\midrule\n'
    for l in di.content[2:]:
        l = strip_vertical_bar(l)
        buf += ' & '.join(l) + '\\\\\n'

    buf += '\\bottomrule\n'
    buf += '\\end{tabular}\n'
    buf += '\\end{table}\n'
    return(buf)

def output_latex_table_color(di):
    buf = ''

    if len(di.content) < 3:
        print('Error: invalid tabular format.', file=sys.stderr)
        exit(1)
        
    header = strip_vertical_bar(di.content[0])
    fmt = strip_vertical_bar(re.sub('-+', '-', di.content[1]))

    tex_fmt = ''
    for s in fmt:
        if s == ':-':
            tex_fmt += '|l|'
        elif s == '-:':
            tex_fmt += '|r|'
        elif s == ':-:':
            tex_fmt += '|c|'
        else:
            tex_fmt += '|c|'

    col_hdr = '\\cellcolor[rgb]{0.941,0.941,0.863}'
    col_bdy = '\\cellcolor[rgb]{0.949,0.949,0.949}'

    buf += '{'
    buf += '\\arrayrulewidth=0pt\n'
    buf += '\\begin{table}[hbtp]\n'
    buf += '\\centering\n'
    buf += '\\begin{tabular}{' + tex_fmt + '}\n'
    buf += '\\specialrule{0.5pt}{0pt}{0.2pt}\n'
    buf += col_hdr
    buf += (' & ' + col_hdr).join(header) + '\\\\\n'
    for l in di.content[2:]:
        l = strip_vertical_bar(l)
        buf += '\\specialrule{0.25pt}{0.2pt}{0.2pt}\n'
        buf += col_bdy
        buf += (' & ' + col_bdy).join(l) + '\\\\\n'

    buf += '\\specialrule{0.5pt}{0.2pt}{0pt}\n'
    buf += '\\end{tabular}\n'
    buf += '\\end{table}\n'
    buf += '}'
    return(buf)
