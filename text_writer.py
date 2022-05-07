import sys

import const

def render(doctree, config):
    doctree.result = []

    body = ''
    for di in doctree.body:
        if di.type == const.HEADER1:
            body += '===================================\n'
            body += '   ' + di.content + '\n'
            body += '===================================\n'
        elif di.type == const.HEADER2:
            body += '|| ' + di.content + '\n'
        elif di.type == const.HEADER3:
            body += '| ' + di.content + '\n'
        elif di.type == const.HEADER4:
            body += '- ' + di.content + '\n'
        elif di.type == const.PARAGRAPH:
            body += di.content + '\n\n'
        elif di.type == const.CODE:
            body += output_text_asis(di) + '\n'
        elif di.type == const.ITEMIZE:
            body += output_text_asis(di) + '\n'
        elif di.type == const.ENUM:
            body += output_text_asis(di) + '\n'
        else:
            print(f'Warning: Unknown DocItem: {di.type}', file=sys.stderr)
    doctree.result.append(body)
    doctree.result.append('<EOF>\n')

def output_text_asis(di):
    buf = ''
    for l in di.content:
        buf += l + '\n'
    return buf
