from pathlib import Path
import re
import sys
import codecs

def parse_search_path(config, file_type):
    result = []

    for l in config[file_type].split(';'):
        l = l.strip()
        if re.match('^/', l):
            result.append(l)
        elif re.match('^[A-Z]:', l):
            result.append(l)
        else:
            result.append(config['root'] + '/' + l)
    return(result)

def find_file(filename, file_type, config):
    path = Path(filename)
    if path.exists():
        return(filename)

    for sp in parse_search_path(config, file_type):
        path = Path(sp + '/' + filename)
        if path.exists():
            return(sp + '/' + filename)

    print(f'Error: {filename} is not found.', file=sys.stderr)
    exit(1)

def read_external_file(filename, config):
    buf = []
    filename = filename.strip('\'"')
    fn = find_file(filename, 'snippet_path', config)

    with codecs.open(fn, 'r', 'utf_8') as f:
        rawlist = f.readlines()
        buf = [s.rstrip() for s in rawlist]

    return buf

def preprocess(md_text_list, cflags, config):
    i = 0
    args = re.split(', *', cflags)
    result = []
    #print(args)
    while i < len(md_text_list):
        m = re.match('^#include *(\S+)', md_text_list[i])
        if m:
            #print('include: ' + m.group(1))
            result.extend(read_external_file(m.group(1), config))
            i += 1
            continue
            
        m = re.match('^#ifdef *([A-Za-z0-9]+)', md_text_list[i])
        if m:
            flag = m.group(1)
            then_str = []
            else_str = []
            buf = []
            have_else = False
            while True:
                s = md_text_list[i]
                #print('|' + s)
                if re.match('^#endif *', s):
                    if have_else:
                        else_str = buf[1:]
                    else:
                        then_str = buf[1:]
                    break
                if re.match('^#else *', s):
                    have_else = True
                    then_str = buf[1:]
                    buf = []
                buf.append(s)
                i += 1
            #print(f'flag: {flag}')
            if flag in args:
                #print('add then-list')
                #print(then_str)
                result.extend(then_str)
            else:
                #print('add else-list')
                #print(else_str)
                result.extend(else_str)
        else:
            result.append(md_text_list[i])
        i += 1
    return result
