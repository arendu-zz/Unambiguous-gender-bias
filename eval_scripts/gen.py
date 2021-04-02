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
    tokens_gen = open(options.text_file + '.en', 'w')
    tags_gen = open(options.text_file + '.feats', 'w')
    ans_gen = open(options.text_file + '.ans', 'w')
    for sen in generate(grammar):
        tokens = []
        tags = []
        exp = []
        j_sen = ' '.join(sen).strip()
        for word in j_sen.split():
            if word.startswith('_'):
                if word.startswith('_EXP_'):
                    exp.append(word)
                else:
                    tags.append(word)
            else:
                tokens.append(word)
        tokens_gen.write(' '.join(tokens).capitalize() + '\n')
        tags_gen.write(' '.join(tags) + '\n')
        ans_gen.write(' '.join(list(set(exp))) + '\n')
    ans_gen.close()
    tokens_gen.close()
    tags_gen.close()
