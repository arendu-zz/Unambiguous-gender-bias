#!/usr/bin/env python
# coding: utf-8
__author__ = 'adirendu'

import argparse
from nltk.lm import MLE

from nltk import word_tokenize, sent_tokenize, ngrams
from nltk.lm import MLE
from nltk.lm.preprocessing import pad_both_ends, padded_everygram_pipeline


eng_wordlist = set([i.strip().lower() for i in open('/usr/share/dict/words', 'r', encoding='utf8').readlines()])
n = 3
data = [[("<s>",), ("</s>",), ("</s>", "</s>")]]
vocab = set(['<s>', '</s>'])
for sent in open('occ.space.en', 'r', encoding='utf8').readlines():
    t = '<s> ' + sent.strip() + ' </s>'
    t = t.split()
    vocab.update(t)
    ng1 = list(ngrams(t, 1))
    ng2 = list(ngrams(t, 2))
    ng3 = list(ngrams(t, 3))
    data.append(ng3 )
    data.append(ng2)
    data.append(ng1)

lm = MLE(3)
lm.fit(data, list(vocab))

out_set = set([])
for s in range(1000):
    occ = lm.generate(100, text_seed=['<s>'], random_seed=s)
    end = occ.index('</s>')
    occ = ''.join(occ[:end])
    if 3 < end < 15 and occ not in eng_wordlist:
        out_set.add(occ[:end])

print('\n'.join(list(out_set)))
