#!/usr/bin/env python
# encoding: UTF-8

import sys

FOOTNOTE = '.footnote[%s]'
TITLE = '''
template: inverse
%s
'''
PAGE = '''
layout: false
.left-column[
%s
]
.right-column[
%s
]
'''
root = ''
previous = []

def process(page):
    global root, previous
    lines = page.split('\n')
    if lines[-1].startswith('\\'):
        lines[-1] = FOOTNOTE % lines[-1][1:]
    if lines[0].startswith('/'):
        items = lines[0].split('/')[1:]
        if items[0] != root or len(previous) == 5:
            root = items[0]
            previous = []
        if len(items) > 1:
            previous.append(items[1])
        path = "### %s" % root
        for prev in previous[-6:]:
            path += '\n#### - %s' % prev
        return PAGE % (path, '\n'.join(lines[1:]))
    else:
        return TITLE % '\n'.join(lines)


def main(filename):
    with open(filename) as stream:
        text = stream.read().strip()
    pages = [p.strip() for p in text.split('---')]
    processed = [process(p) for p in pages]
    with open('template.html') as stream:
        template = stream.read()
    html = template.replace('<? CONTENT ?>', '\n---\n'.join(processed))
    with open('index.html', 'w') as stream:
        stream.write(html)


if __name__ == '__main__':
    filename = 'readme.md'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    main(filename)

