#!/usr/bin/env python
# coding: utf-8
__author__ = 'adirendu'

import argparse

if __name__ == '__main__':
    opt = argparse.ArgumentParser(description="write program description here")

    # insert options here
    opt.add_argument('ans_file', type=str, help='this file should have the ground truth answers')
    opt.add_argument('src_file', type=str, help='this file should have the source text in En')
    opt.add_argument('feats_file', type=str, help='this file should have the source features')
    opt.add_argument('result_file', type=str, help='this file should have the gender tag of the target-side occupation noun')
    opt.add_argument('occ_file', type=str, help='text file with occ file')
    options = opt.parse_args()

    srcs = [i.strip() for i in open(options.src_file, 'r', encoding='utf8').readlines()]
    answers = [i.strip() for i in open(options.ans_file, 'r', encoding='utf8').readlines()]
    feats = [i.strip() for i in open(options.feat_file, 'r', encoding='utf8').readlines()]
    result = open(options.tgt_file + '.result', 'w', encoding='utf-8')
    alignments = open(options.tgt_file + '.align', 'w', encoding='utf-8')
