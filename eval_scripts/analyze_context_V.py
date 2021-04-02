#!/usr/bin/env python
# coding: utf-8
__author__ = 'adirendu'

import argparse


feat_map = {'_CLUE_NR_F_' : 'CLUE_F',
            '_CLUE_NR_M_' : 'CLUE_M',
            '_CLUE_Pr_F_' : 'CLUE_F',
            '_CLUE_Pr_M_' : 'CLUE_M',
            '_CONTEXT_A_F_' : '',
            '_CONTEXT_A_M_' : '',
            '_CONTEXT_NPO_A_' : '',
            '_CONTEXT_V_F_' : 'CONTEXT_V_F',
            '_CONTEXT_V_M_' : 'CONTEXT_V_M',
            '_OCC_AFTER_' : '', 
            '_OCC_BEFORE_' : '', 
            '_OCC_MIDDLE_' : '', 
            '_OCC_NO_F_' : 'OCC_F',
            '_OCC_NO_M_' : 'OCC_M'}

if __name__ == '__main__':
    opt = argparse.ArgumentParser(description="write program description here")

    # insert options here
    opt.add_argument('ans_file', type=str, help='this file should have the ground truth answers')
    opt.add_argument('src_file', type=str, help='this file should have the source text in En')
    opt.add_argument('fts_file', type=str, help='this file should have the source features')
    opt.add_argument('res_file', type=str, help='this file should have the translated file')
    opt.add_argument('occ_file', type=str, help='text file with occ file')
    options = opt.parse_args()

    srcs = [i.strip() for i in open(options.src_file, 'r', encoding='utf8').readlines()]
    answers = [i.strip() for i in open(options.ans_file, 'r', encoding='utf8').readlines()]
    fts = [i.strip() for i in open(options.fts_file, 'r', encoding='utf8').readlines()]
    results = [i.strip() for i in open(options.res_file, 'r', encoding='utf-8').readlines()]
    occpations =  set([i.strip().lower() for i in open(options.occ_file, 'r', encoding='utf8').readlines()])
    accuracies = {} 
    assert len(srcs) == len(answers) == len(results) == len(fts), "length mismatch between srcs, answer, results, features"
    
    for src, answer, result, feat in zip(srcs, answers, results, fts):
        o = set(src.lower().split()).intersection(occpations)
        o = 'occ=' + list(o)[0]
        feat_set = sorted(set([feat_map[i.strip()] for i in feat.strip().split() if feat_map[i.strip()] != '']))
        f_all = tuple(['all'] + feat_set)
        f_occ = tuple([o] + feat_set)
        sc = accuracies.get((o,), [0, 0, 0, 0])
        accuracies[(o,)] = sc
        all_sc = accuracies.get(('all',), [0, 0, 0, 0])
        accuracies[('all',)] = all_sc
        f_all_sc = accuracies.get(f_all, [0, 0, 0, 0])
        accuracies[f_all] = f_all_sc
        f_occ_sc = accuracies.get(f_occ, [0, 0, 0, 0])
        accuracies[f_occ] = f_occ_sc
        sc[3] += 1
        all_sc[3] += 1
        f_all_sc[3] += 1
        f_occ_sc[3] += 1
        if (answer == '_EXP_M_' and result == 'Masc') or (answer == '_EXP_F_' and result == 'Fem'):
            sc[0] += 1
            all_sc[0] += 1
            f_all_sc[0] += 1
            f_occ_sc[0] += 1
        elif (answer == '_EXP_M_' and result == 'Fem') or (answer == '_EXP_F_' and result == 'Masc'):
            sc[1] += 1
            all_sc[1] += 1
            f_all_sc[1] += 1
            f_occ_sc[1] += 1
        else:
            sc[2] += 1
            all_sc[2] += 1
            f_all_sc[2] += 1
            f_occ_sc[2] += 1

    for k, v in sorted(accuracies.items()):
        if v[3] > 0:
            vn = [float(i) / (1e-4 + v[-1]) for i in v[:-1]]
            k_str = ' '.join(list(k))
            vs = ' '.join([k_str] + [f'{i:.2f}' for i in vn] + [f'{s}' for s in v])
            print(vs)
