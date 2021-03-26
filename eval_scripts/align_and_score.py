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
    opt.add_argument('tgt_file', type=str, help='text file with  tgt file')
    opt.add_argument('feat_file', type=str, help='text file with feat file')
    opt.add_argument('occ_file', type=str, help='text file with occ file')
    opt.add_argument('expected_gender', type=str, help='the expected gender associated with the occupation noun')
    options = opt.parse_args()
    genders = ['Fem', 'Masc']
    assert options.expected_gender in genders
    not_expected_gender = [i for i in genders if i != options.expected_gender][0]
    model = transformers.BertModel.from_pretrained('bert-base-multilingual-cased')
    tokenizer = transformers.BertTokenizer.from_pretrained('bert-base-multilingual-cased')
    occpations =  set([i.strip().lower() for i in open(options.occ_file, 'r', encoding='utf8').readlines()[1:]])
    accuracies = {o : [0, 0, 0, 0] for o in occpations}
    accuracies['all'] = [0, 0, 0, 0]
    srcs = [i.strip() for i in open(options.src_file, 'r', encoding='utf8').readlines()]
    tgts = [i.strip() for i in open(options.tgt_file, 'r', encoding='utf8').readlines()]
    feats = [i.strip() for i in open(options.feat_file, 'r', encoding='utf8').readlines()]
    for src, tgt, feat in zip(srcs, tgts, feats):
        sent_src, sent_tgt, sent_feat = src.strip().split(), tgt.strip().split(), feat.strip().split()
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
          out_src = model(ids_src.unsqueeze(0), output_hidden_states=True)[2][align_layer][0, 1:-1]
          out_tgt = model(ids_tgt.unsqueeze(0), output_hidden_states=True)[2][align_layer][0, 1:-1]

          dot_prod = torch.matmul(out_src, out_tgt.transpose(-1, -2))

          softmax_srctgt = torch.nn.Softmax(dim=-1)(dot_prod)
          softmax_tgtsrc = torch.nn.Softmax(dim=-2)(dot_prod)

          softmax_inter = (softmax_srctgt > threshold)*(softmax_tgtsrc > threshold)

        align_subwords = torch.nonzero(softmax_inter, as_tuple=False)
        align_words = set()
        for i, j in align_subwords:
          align_words.add( (sub2word_map_src[i], sub2word_map_tgt[j]) )

        # printing
        class color:
           PURPLE = '\033[95m'
           CYAN = '\033[96m'
           DARKCYAN = '\033[36m'
           BLUE = '\033[94m'
           GREEN = '\033[92m'
           YELLOW = '\033[93m'
           RED = '\033[91m'
           BOLD = '\033[1m'
           UNDERLINE = '\033[4m'
           END = '\033[0m'

        print(f'{color.BLUE}{src}{color.END}\t{color.CYAN}{tgt}{color.END}')
        is_skip = True
        for i, j in sorted(align_words):
          #TODO: This check will ignore occupations with multiple tokens like "Truck driver" etc. Must fix in next version
          if sent_src[i].lower() in occpations:
              is_skip = False
              accuracies[sent_src[i].lower()][-1] += 1
              accuracies['all'][-1] += 1
              if sent_feat[j] == options.expected_gender:
                  accuracies[sent_src[i].lower()][0] += 1
                  accuracies['all'][0] += 1
                  print(f'{color.BLUE}{sent_src[i]}{color.END}==={color.CYAN}{sent_tgt[j]}{color.END} {sent_feat[j]} {color.BOLD}{color.GREEN}Correct{color.END}')
              elif sent_feat[j] == not_expected_gender:
                  accuracies[sent_src[i].lower()][1] += 1
                  accuracies['all'][1] += 1
                  print(f'{color.BLUE}{sent_src[i]}{color.END}==={color.CYAN}{sent_tgt[j]}{color.END} {sent_feat[j]} {color.BOLD}{color.RED}Wrong!{color.END}')
              else:
                  accuracies[sent_src[i].lower()][2] += 1
                  accuracies['all'][2] += 1
                  print(f'{color.BLUE}{sent_src[i]}{color.END}==={color.CYAN}{sent_tgt[j]}{color.END} {sent_feat[j]} {color.BOLD}{color.YELLOW}Meh{color.END}')
          else:
              print(f'{color.BLUE}{sent_src[i]}{color.END}==={color.CYAN}{sent_tgt[j]}{color.END}')
        if is_skip:
          print(f'{color.YELLOW}skipped...{color.END}')




    for k in sorted(accuracies):
        v = accuracies[k]
        sv = v[-1]
        pv = [float(i) / (1e-4 + sv) for i in v]
        pv[0] = f'{color.GREEN}{pv[0]:.2f}{color.END}'
        pv[1] = f'{color.RED}{pv[1]:.2f}{color.END}'
        pv[2] = f'{color.YELLOW}{pv[2]:.2f}{color.END}'
        pv[3] = f'{pv[3]:.2f}'
        v[0] = f'{color.GREEN}{v[0]:.2f}{color.END}'
        v[1] = f'{color.RED}{v[1]:.2f}{color.END}'
        v[2] = f'{color.YELLOW}{v[2]:.2f}{color.END}'
        v[3] = f'{v[3]:.2f}'
        if sv > 0:
            print('\t'.join([k.ljust(25, ' '), ' '.join([i for i in pv]), ' '.join([i for i in v])]))
