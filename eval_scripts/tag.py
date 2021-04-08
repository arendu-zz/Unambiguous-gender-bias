#!/usr/bin/env python
# coding: utf-8
__author__ = 'adirendu'

import argparse
import stanza
PIPE='＿'

if __name__ == '__main__':
    opt = argparse.ArgumentParser(description="write program description here")
    opt.add_argument('file', type=str, help='this is a positional arg')
    opt.add_argument('lang', type=str, help='this is a positional arg')
    options = opt.parse_args()
    stanza.download(options.lang)
    bs = 2500
    nlp = stanza.Pipeline(lang=options.lang, 
                          use_gpu=True,
                          verbose=True,
                          processors='tokenize,pos',
                          pos_batch_size=bs,
                          tokenize_no_ssplit=True,
                          tokenize_pretokenized=False)
    file_lines = open(options.file, 'r', encoding='utf-8').readlines()
    num_file_lines = len(file_lines)
    print(num_file_lines)
    str_file_lines = '\n'.join(file_lines)

    print('processing doc')
    file_text_tok = open(options.file + '.tok', 'w', encoding='utf-8')
    file_text_tag = open(options.file + '.tag', 'w', encoding='utf-8')
    file_text_fulltag = open(options.file + '.fulltag', 'w', encoding='utf-8')
    for i in range((len(file_lines) // bs) + 1):
        st = i * bs
        end = (1 + i) * bs
        print('processing segment', st, end)
        seg_lines = [l.strip() for l in file_lines[st: end]]
        num_seg_lines = len(seg_lines)
        if num_seg_lines  == 0:
            continue
        seg_lines_join = '\n\n'.join(seg_lines)
        doc = nlp(seg_lines_join)
        print('done processing seg')
        assert len(doc.sentences) ==  num_seg_lines, f"{len(doc.sentences)} is not equal to {num_seg_lines}"
        for sent in doc.sentences:
            w_toks = []
            w_fulltags = []
            w_tags = []
            for w in sent.words:
                w_toks.append(w.text)
                if w.feats is not None:
                    ff = w.feats
                    gf = [_g for _g in w.feats.split('|') if _g.startswith('Gender')]
                    if len(gf) == 1:
                        g = gf[0].split('=')[1]
                    else:
                        g = '_'
                else:
                    g = '_'
                    ff = '_'
                w_tags.append(g)
                w_fulltags.append(ff)
            assert len(w_toks) == len(w_tags), "num feat tags != num tokens"
            file_text_tok.write(' '.join(w_toks) + '\n')
            file_text_tag.write(' '.join(w_tags) + '\n')
            file_text_fulltag.write(' '.join(w_fulltags) + '\n')
    file_text_tok.close()
    file_text_tag.close()
    print(options.file + '.tok', 'closed')
    print(options.file + '.fulltag', 'closed')
    print(options.file + '.tag', 'closed')
