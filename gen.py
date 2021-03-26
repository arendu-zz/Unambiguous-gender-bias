#!/usr/bin/env python
# coding: utf-8
__author__ = 'adirendu'
from nltk.parse.generate import generate
from nltk import CFG
import argparse

if __name__ == '__main__':
    opt = argparse.ArgumentParser(description="write program description here")
    # insert options here
    opt.add_argument('grammar_file', type=str, help='path to grammar')
    opt.add_argument('text_file', type=str, help='path to output')
    options = opt.parse_args()
    grammar  = CFG.fromstring(open(options.grammar_file, 'r').readlines())
    w_gen = open(options.text_file, 'w')
    for sen in generate(grammar):
        w_gen.write(' '.join(sen) + '\n')
    w_gen.close()
