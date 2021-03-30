#!/usr/bin/env python
# coding: utf-8
__author__ = 'adirendu'

import argparse

if __name__ == '__main__':
    opt = argparse.ArgumentParser(description="write program description here")

    # insert options here
    opt.add_argument('occ_file', type=str, help='file with list of occ')
    opt.add_argument('en_file', type=str, help='file with ground truth answer')
    opt.add_argument('ans_file', type=str, help='file with ground truth answer')
    opt.add_argument('res_file', type=str, help='file with gender tag for translation')
    options = opt.parse_args()
    occpations =  set([i.strip().lower() for i in open(options.occ_file, 'r', encoding='utf8').readlines()])
    accuracies = {o : [0, 0, 0, 0] for o in occpations}
    accuracies['all'] = [0, 0, 0, 0]
    en_srcs = [i.strip() for i in open(options.en_file, 'r', encoding='utf8').readlines()]
    answers = [i.strip() for i in open(options.ans_file, 'r', encoding='utf8').readlines()]
    results = [i.strip() for i in open(options.res_file, 'r', encoding='utf8').readlines()]
    
    for sent, answer, result in zip(en_srcs, answers, results):
        o = set(sent.lower().split()).intersection(occpations)
        o = list(o)
        sc = accuracies[o[0]]
        all_sc = accuracies['all']
        sc[3] += 1
        all_sc[3] += 1
        if (answer == '_EXP_M_' and result == 'Masc') or (answer == '_EXP_F_' and result == 'Fem'):
            sc[0] += 1
            all_sc[0] += 1
        elif (answer == '_EXP_M_' and result == 'Fem') or (answer == '_EXP_F_' and result == 'Masc'):
            sc[1] += 1
            all_sc[1] += 1
        else:
            sc[2] += 1
            all_sc[2] += 1

    for k, v in sorted(accuracies.items()):
        if v[3] > 0:
            vn = [float(i) / (1e-4 + v[-1]) for i in v[:-1]]
            vs = ' '.join([k] + [f'{i:.2f}' for i in vn] + [f'{s}' for s in v])
            print(vs)
