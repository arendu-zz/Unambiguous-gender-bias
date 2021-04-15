#!/usr/bin/env python
# coding: utf-8
__author__ = 'adirendu'

import argparse
import pandas as pd
import pdb

before_after_middle = set("BEFORE AFTER MIDDLE".split())
trigger = set("CLUE_F CLUE_M".split())
occ = set("OCC_F OCC_M".split())


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
        for line in open(path + 'target.' + l + '.tok.analysis.before_after').readlines():
            items = line.strip().split()
            s_items = set(items)
            bma = s_items.intersection(before_after_middle)
            occ_m_or_f = s_items.intersection(occ)
            trigger_m_or_f = s_items.intersection(trigger)
            if len(bma) == 1 and len(occ_m_or_f) == 1 and len(trigger_m_or_f) == 1 and line.startswith('all'):
                _d = items[-4:]
                bma = list(bma)[0]
                occ_m_or_f = list(occ_m_or_f)[0]
                trigger_m_or_f  = list(trigger_m_or_f)[0]
                data.append([bma, occ_m_or_f, trigger_m_or_f] + _d)

    df = pd.DataFrame(data, columns='category occ  trigger correct_num wrong_num na_num total_num'.split())
    df['correct_num'] = df['correct_num'].astype(float)
    df['wrong_num'] = df['wrong_num'].astype(float)
    df['total_num'] = df['total_num'].astype(float)
    df['na_num'] = df['total_num'] - (df['correct_num'] + df['wrong_num'])
    pdb.set_trace()
    df = df.groupby(['trigger', 'category', 'occ'], as_index=False).sum()
    df['correct'] = df['correct_num'].div(df['total_num'])
    df['na'] = df['na_num'].div(df['total_num'])
    df['wrong'] = df['wrong_num'].div(df['total_num'])
    print(df)
    pdb.set_trace()
    mm = df.loc[(df['trigger'] == 'CLUE_M') & (df['occ'] == 'OCC_M')] #.sort_values(by=['correct'], ascending=False)
    ff = df.loc[(df['trigger'] == 'CLUE_F') & (df['occ'] == 'OCC_F')] #.sort_values(by=['correct'], ascending=False)
    mf = df.loc[(df['trigger'] == 'CLUE_M') & (df['occ'] == 'OCC_F')] #.sort_values(by=['correct'], ascending=False)
    fm = df.loc[(df['trigger'] == 'CLUE_F') & (df['occ'] == 'OCC_M')] #.sort_values(by=['correct'], ascending=False)
    print(mm)
    pdb.set_trace()
    for t, dd in [('mm', mm), ('ff', ff), ('mf', mf), ('fm', fm)]:
        dd = dd.sort_values(by='correct', ascending=False)
        occ_order = "BEFORE MIDDLE AFTER".split()
        print(t)
        print('{' + ','.join(['avg'] + occ_order) + '}')
        avg_correct = dd['correct'].astype(float).mean()
        avg_na = dd['na'].astype(float).mean()
        avg_wrong = dd['wrong'].astype(float).mean()
        d_correct = [f'(avg,{avg_correct:.2f})'] +  ['(' + lo + ',' + f"{dd.loc[dd['category'] == lo]['correct'].iat[0]:.2f}" + ')' for lo in occ_order]
        d_na = [f'(avg,{avg_na:.2f})'] +  ['(' + lo + ',' + f"{dd.loc[dd['category'] == lo]['na'].iat[0]:.2f}" + ')' for lo in occ_order]
        d_wrong = [f'(avg,{avg_wrong:.2f})'] +  ['(' + lo + ',' + f"{dd.loc[dd['category'] == lo]['wrong'].iat[0]:.2f}" + ')' for lo in occ_order]
        print('\\addplot +[fill=green!40,draw=green!90] coordinates {', ' '.join(d_correct), '};\n')
        print('\\addplot +[fill=yellow!40,draw=yellow!90] coordinates {', ' '.join(d_na), '};\n')
        print('\\addplot +[fill=red!40,draw=red!90] coordinates {', ' '.join(d_wrong), '};\n')
