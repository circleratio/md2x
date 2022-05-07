#!/usr/bin/env python

import codecs
import re
import sys

def parse_latex_log(file):
    result = []
    with codecs.open(file, 'r', 'utf-8') as f:
        lines = [l.rstrip() for l in f.readlines()]

    for i in range(len(lines)):
        l = lines[i]
        m = re.match('^File: (.*) Graphic file', l)
        if m:
            i += 1
            img_file = m.group(1)
            #print(img_file)
            overfull = False
            while True:
                l = lines[i]
                m = re.match('(^<|^ |^\[|^\]|^$|^Overfull)', l)
                if m:
                    i += 1
                    if m.group(1) == 'Overfull':
                        #print(l)
                        overfull = True
                else:
                    #print('B:' + l)
                    break
            if overfull:
                result.append('{}: Overfull'.format(img_file))
            else:
                result.append('{}: OK'.format(img_file))
        else:
            i += 1
    return result

def write_result(file, result):
    with codecs.open(file, 'w', 'utf-8') as f:
        for r in result:
            f.write(r + '\n')
        
def main():
    res = parse_latex_log(sys.argv[1])
    write_result('imagecheck.log', res)
    return 0

if __name__ == '__main__':
    sys.exit(main())

