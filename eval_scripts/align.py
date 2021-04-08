#!/usr/bin/env python
# coding: utf-8
__author__ = 'adirendu'

import argparse
import torch
import transformers
import itertools

if __name__ == '__main__':
    opt = argparse.ArgumentParser(description="write program description here")
    # insert options here
    opt.add_argument('src_file', type=str, help='text file with src file')
    opt.add_argument('ans_file', type=str, help='text file with answers file')
    opt.add_argument('tgt_file', type=str, help='text file with  tgt file')
    opt.add_argument('feat_file', type=str, help='text file with feat file')
    opt.add_argument('occ_file', type=str, help='text file with occ file')
    options = opt.parse_args()
    model = transformers.BertModel.from_pretrained('bert-base-multilingual-cased')
    model = model.cuda()
    tokenizer = transformers.BertTokenizer.from_pretrained('bert-base-multilingual-cased')
    occupations =  set([i.strip().lower() for i in open(options.occ_file, 'r', encoding='utf8').readlines()])
    accuracies = {o : [0, 0, 0, 0] for o in occupations}
    accuracies['all'] = [0, 0, 0, 0]
    srcs = [i.strip() for i in open(options.src_file, 'r', encoding='utf8').readlines()]
    tgts = [i.strip() for i in open(options.tgt_file, 'r', encoding='utf8').readlines()]
    answers = [i.strip() for i in open(options.ans_file, 'r', encoding='utf8').readlines()]
    feats = [i.strip() for i in open(options.feat_file, 'r', encoding='utf8').readlines()]
    result = open(options.tgt_file + '.result', 'w', encoding='utf-8')
    occupation_alignments = open(options.tgt_file + '.occ_align', 'w', encoding='utf-8')
    alignments = open(options.tgt_file + '.align', 'w', encoding='utf-8')
    for src, tgt, feat, answer in zip(srcs, tgts, feats, answers):
        sent_src, sent_tgt, sent_feat = src.strip().split(), tgt.strip().split(), feat.strip().split()
        assert len(sent_tgt) == len(sent_feat)
        token_src, token_tgt = [tokenizer.tokenize(word) for word in sent_src], [tokenizer.tokenize(word) for word in sent_tgt]
        wid_src, wid_tgt = [tokenizer.convert_tokens_to_ids(x) for x in token_src], [tokenizer.convert_tokens_to_ids(x) for x in token_tgt]
        ids_src, ids_tgt = tokenizer.prepare_for_model(list(itertools.chain(*wid_src)), return_tensors='pt', model_max_length=tokenizer.model_max_length, truncation=True)['input_ids'], tokenizer.prepare_for_model(list(itertools.chain(*wid_tgt)), return_tensors='pt', truncation=True, model_max_length=tokenizer.model_max_length)['input_ids']
        sub2word_map_src = []
        for i, word_list in enumerate(token_src):
            sub2word_map_src += [i for x in word_list]
        sub2word_map_tgt = []
        for i, word_list in enumerate(token_tgt):
            sub2word_map_tgt += [i for x in word_list]
        # alignment
        align_layer = 8
        threshold = 1e-3
        model.eval()
        with torch.no_grad():
            out_src = model(ids_src.unsqueeze(0).cuda(), output_hidden_states=True)[2][align_layer][0, 1:-1]
            out_tgt = model(ids_tgt.unsqueeze(0).cuda(), output_hidden_states=True)[2][align_layer][0, 1:-1]
            dot_prod = torch.matmul(out_src, out_tgt.transpose(-1, -2))
            softmax_srctgt = torch.nn.Softmax(dim=-1)(dot_prod)
            softmax_tgtsrc = torch.nn.Softmax(dim=-2)(dot_prod)
            softmax_inter = (softmax_srctgt > threshold)*(softmax_tgtsrc > threshold)
        align_subwords = torch.nonzero(softmax_inter, as_tuple=False).cpu()
        align_words = set()
        for i, j in align_subwords:
          align_words.add( (sub2word_map_src[i], sub2word_map_tgt[j]) )

        is_skip = True
        align_res = 'None'
        align_text = []
        for i, j in sorted(align_words):
            align_text.append(sent_src[i] + '->' + sent_tgt[j] + '->' + sent_feat[j])
            if sent_src[i].lower() in occupations:
                occupation_alignments.write(sent_src[i] + '->' + sent_tgt[j] + '\n')
                align_res = sent_feat[j]
        result.write(align_res + '\n')
        alignments.write(' '.join(align_text) + '\n')
    result.close()
    occupation_alignments.close()
    alignments.close()
