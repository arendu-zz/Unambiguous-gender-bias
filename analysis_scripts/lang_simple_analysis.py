#!/usr/bin/env python
# coding: utf-8
__author__ = 'adirendu'

import argparse
import pandas as pd

if __name__ == '__main__':
    opt = argparse.ArgumentParser(description="write program description here")

    # insert options here
    opt.add_argument('size', type=str, help='size of model for analysis')
    opt.add_argument('model', type=str, help='name of model for analysis')
    opt.add_argument('langs', type=str, help='path of langs for analysis')
    options = opt.parse_args()

    langs = [l.strip() for l in open(options.langs, 'r').readlines()]
    path = '/checkpoint/adirendu/Unambiguous-gender-bias/generated/' + options.size + '/' + options.model + '/'
    data = []
    for l in langs:
        for line in open(path + 'target.' + l + '.tok.analysis.simple').readlines():
            if line.startswith('all CLUE'):
                data.append([l] + line.strip().split())

    df = pd.DataFrame(data, columns='lang category trigger occ correct wrong na correct_num wrong_num na_num total_num'.split())
    mm = df.loc[(df['trigger'] == 'CLUE_M') & (df['occ'] == 'OCC_M')].sort_values(by=['correct'], ascending=False)
    ff = df.loc[(df['trigger'] == 'CLUE_F') & (df['occ'] == 'OCC_F')].sort_values(by=['correct'], ascending=False)
    mf = df.loc[(df['trigger'] == 'CLUE_M') & (df['occ'] == 'OCC_F')].sort_values(by=['correct'], ascending=False)
    fm = df.loc[(df['trigger'] == 'CLUE_F') & (df['occ'] == 'OCC_M')].sort_values(by=['correct'], ascending=False)
    lang_order = mm['lang'].to_list()
    print('{' + ','.join(['avg'] + lang_order) + '}')
    for t, dd in [('mm', mm), ('ff', ff), ('mf', mf), ('fm', fm)]:
        print(t)
        avg_correct = dd['correct'].astype(float).mean()
        avg_na = dd['na'].astype(float).mean()
        avg_wrong = dd['wrong'].astype(float).mean()
        d_correct = [f'(avg,{avg_correct:.2f})'] +  ['(' + lo + ',' + dd.loc[dd['lang'] == lo]['correct'].iat[0] + ')' for lo in lang_order]
        d_na = [f'(avg,{avg_na:.2f})'] +  ['(' + lo + ',' + dd.loc[dd['lang'] == lo]['na'].iat[0] + ')' for lo in lang_order]
        d_wrong = [f'(avg,{avg_wrong:.2f})'] +  ['(' + lo + ',' + dd.loc[dd['lang'] == lo]['wrong'].iat[0] + ')' for lo in lang_order]

        print('\\addplot +[fill=green!40,draw=green!90] coordinates {', ' '.join(d_correct), '};\n')
        print('\\addplot +[fill=yellow!40,draw=yellow!90] coordinates {', ' '.join(d_na), '};\n')
        print('\\addplot +[fill=red!40,draw=red!90] coordinates {', ' '.join(d_wrong), '};\n')
