#!/usr/bin/env python
# coding: utf-8
__author__ = 'adirendu'

import argparse
from easynmt import EasyNMT


if __name__ == '__main__':
    opt = argparse.ArgumentParser(description="write program description here")

    # insert options here
    opt.add_argument('inp_file', type=str, help='this is an English input')
    opt.add_argument('tgt_lang', type=str, help='this should be the target language')
    options = opt.parse_args()
    model = EasyNMT('m2m_100_1.2B')
    lines =  [l.strip() for l in open(options.inp_file, 'r', encoding='utf8').readlines()]
    translations = model.translate(lines, target_lang=options.tgt_lang)
    print('\n'.join(translations))
