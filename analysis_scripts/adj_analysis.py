#!/usr/bin/env python
# coding: utf-8
__author__ = 'adirendu'

import argparse
import pandas as pd
import pdb

if __name__ == '__main__':
    opt = argparse.ArgumentParser(description="write program description here")

    # insert options here
    opt.add_argument('size', type=str, help='size of model for analysis')
    opt.add_argument('model', type=str, help='name of model for analysis')
    opt.add_argument('langs', type=str, help='path of langs for analysis')
    opt.add_argument('adj', type=str, help='path of adj for analysis')
    opt.add_argument('src', type=str, help='path of adj for analysis')
    opt.add_argument('src_feats', type=str, help='path of adj for analysis')
    options = opt.parse_args()

    langs = [l.strip() for l in open(options.langs, 'r').readlines()]
    src = [l.strip() for l in open(options.src, 'r').readlines()]
    src_feats = [l.strip() for l in open(options.src_feats, 'r').readlines()]
    for line in open(options.adj, 'r', encoding='utf8').readlines():
        print(line)
        items = [i.strip() for i in line.strip().split(',')]
        if items[0] == 'F':
            f_adj = set(items[1:])
        elif items[0] == 'M':
            m_adj = set(items[1:])
    data = []
    for l in langs:
        path = '/checkpoint/adirendu/Unambiguous-gender-bias/generated/' + options.size + '/' + options.model + '/'
        tgt_result = [l.strip() for l in open(path + 'target.' + l + '.tok.result', 'r').readlines()]
        for s_line, s_feat, t_result in zip(src, src_feats, tgt_result):
            s_items = set(s_line.split())
            m_adj_item = list(s_items.intersection(m_adj))
            f_adj_item = list(s_items.intersection(f_adj))
            if len(f_adj_item) == 1:
                adj_category = 'ADJ_F'
                adj_item = f_adj_item[0] + '(F)'
            elif len(m_adj_item) == 1:
                adj_category = 'ADJ_M'
                adj_item = m_adj_item[0] + '(M)'
            else:
                adj_category = '_'

            if adj_category != '_':
                clue = [c for c in s_feat.split() if c.startswith('_CLUE_')][0].split('_')[3]
                clue = 'Masc' if clue == 'M' else 'Fem'
                occ = [o for o in s_feat.split() if o.startswith('_OCC_NO_')][0].split('_')[3]
                occ = 'OCC_M' if occ == 'M' else 'OCC_F'
                print(l, s_line, s_feat, t_result, clue, occ, m_adj_item, f_adj_item)
                if t_result == '_':
                    r = [0.0, 0.0, 1.0]
                elif t_result == clue:
                    r = [1.0, 0.0, 0.0]
                else:
                    r = [0.0, 1.0, 0.0]
                d_line = [clue, occ, adj_item] + r
                data.append(d_line)

    df = pd.DataFrame(data, columns='trigger_category occ_category adj_token correct wrong na'.split())
    df = df.groupby(['trigger_category', 'occ_category', 'adj_token'], as_index=False).mean()
    mm = df.loc[(df['trigger_category'] == 'Masc') & (df['occ_category'] == 'OCC_M')].sort_values(by=['correct'], ascending=False)
    ff = df.loc[(df['trigger_category'] == 'Fem') & (df['occ_category'] == 'OCC_F')].sort_values(by=['correct'], ascending=False)
    mf = df.loc[(df['trigger_category'] == 'Masc') & (df['occ_category'] == 'OCC_F')].sort_values(by=['correct'], ascending=False)
    fm = df.loc[(df['trigger_category'] == 'Fem') & (df['occ_category'] == 'OCC_M')].sort_values(by=['correct'], ascending=False)

    for t, dd in [('mm', mm), ('ff', ff), ('mf', mf), ('fm', fm)]:
        print(t)
        adj_order = dd['adj_token'].to_list()
        print('{' + ','.join(['avg'] + adj_order) + '}')
        avg_correct = dd['correct'].astype(float).mean()
        avg_na = dd['na'].astype(float).mean()
        avg_wrong = dd['wrong'].astype(float).mean()
        d_correct = [f'(avg,{avg_correct:.2f})'] +  ['(' + lo + ',' + f"{dd.loc[dd['adj_token'] == lo]['correct'].iat[0]:.2f}" + ')' for lo in adj_order]
        d_na = [f'(avg,{avg_na:.2f})'] +  ['(' + lo + ',' + f"{dd.loc[dd['adj_token'] == lo]['na'].iat[0]:.2f}" + ')' for lo in adj_order]
        d_wrong = [f'(avg,{avg_wrong:.2f})'] +  ['(' + lo + ',' + f"{dd.loc[dd['adj_token'] == lo]['wrong'].iat[0]:.2f}" + ')' for lo in adj_order]
        print('\\addplot +[fill=green!40,draw=green!90] coordinates {', ' '.join(d_correct), '};\n')
        print('\\addplot +[fill=yellow!40,draw=yellow!90] coordinates {', ' '.join(d_na), '};\n')
        print('\\addplot +[fill=red!40,draw=red!90] coordinates {', ' '.join(d_wrong), '};\n')
