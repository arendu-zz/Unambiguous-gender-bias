#!/usr/bin/env python
# coding: utf-8
__author__ = 'adirendu'
from nltk.parse.generate import generate
from nltk import CFG
for g in ['mofc', 'fomc', 'template']:
    grammar  = CFG.fromstring(open(g + '.grammar', 'r').readlines())
    w_gen = open(g + '.en', 'w')
    for sen in generate(grammar):
        w_gen.write(' '.join(sen) + '\n')
    w_gen.close()
