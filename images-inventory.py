#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(format='%(asctime)s : %(filename)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import os
import sys

from bs4 import BeautifulSoup
import markdown as markdown_parser

fields = ['ready', 'folder', 'essay', 'thumbnail', 'manifest', 'height', 'width', 'format', 'iiif-url', 'attribution', 'source', 'author', 'description', 'license', 'label', 'url', 'attribution-url']
field_names_map = {'title': 'label'}

if __name__ == '__main__':

    rootDir = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print('\t'.join(fields))
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            if fname.endswith('.md'):
                essay = fname[:0-3]
                if essay == 'README':
                    essay = dirName.split('/')[-1]

                markdown = open(f'{dirName}/{fname}', 'r').read()
                soup = BeautifulSoup(markdown, 'html5lib')
                for tag in soup.find_all('param'):
                    if 've-image' in tag.attrs:
                        data = {'essay': essay}
                        for attr in ('attribution', 'description', 'label', 'license', 'manifest', 'title', 'url'):
                            if attr in tag.attrs:
                                data[field_names_map.get(attr, attr)] = tag.attrs[attr].replace('\t', ' ').replace('\n', ' ')
                        rec = [data.get(f,'') for f in fields]
                        print('\t'.join(rec))
                markdown = open(f'{dirName}/{fname}', 'r').read()
                html = markdown_parser.markdown(markdown, output_format='html5')
                soup = BeautifulSoup(html, 'html5lib')
                for tag in soup.find_all('img'):
                    if 've-button.png' in tag.attrs['src']: continue
                    data = {'folder': '/'.join(dirName.split('/')[1:]), 'essay': essay, 'url': tag.attrs['src']}
                    rec = [data.get(f,'') for f in fields]
                    print('\t'.join(rec))                    
