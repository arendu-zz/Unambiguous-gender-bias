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
    opt.add_argument('mt_model', type=str, help='this should be the target language')
    options = opt.parse_args()
    model = EasyNMT(options.mt_model)
    lines =  [l.strip() for l in open(options.inp_file, 'r', encoding='utf8').readlines()]
    if options.mt_model == 'm2m_100_1.2B':
        batch_size=64
    elif options.mt_model == 'opus-mt':
        batch_size=512
    else:
        batch_size=128
    translations = model.translate(lines, source_lang='en', target_lang=options.tgt_lang, batch_size=batch_size, beam_size=5)
    print('\n'.join(translations))
