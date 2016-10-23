import os
import re
import sys
import time
import math
import random

from getopt import getopt

if '__main__' == __name__:
    digit_matcher = re.compile('\\d{6,}')
    question_ptn = re.compile("Question-\d+")
    K = 4
    seed = 42
    args = sys.argv[1:]
    opts, args = getopt(args, '', ['conll=', 'seed='])
    conll_inputs=''
    for option, value in opts:
        if '--conll' == option:
            conll_inputs=value
        if '--seed' == option:
            seed = value
    assert conll_inputs, 'Provide .conll file(s)!, e.g.:\npython train.py --conll=file1.conll,file2.conll,file3.conll'
    post_list = []
    post_text_list = []

    for conll_filename in conll_inputs.split(','):
        post = []
        with open(conll_filename, encoding='UTF-8', mode='r') as conll_file:
            conll_filecontents = list(filter('\n'.__ne__, conll_file.readlines()))
            for i in range(len(conll_filecontents)):
                line = conll_filecontents[i].strip()
                name_entity, _, _, token = line.split('\t')
                if 'Question' == token and i + 2 < len(conll_filecontents):
                    next_token = conll_filecontents[i + 1].split('\t')[-1][:-1] # strip newline
                    next2_token = conll_filecontents[i + 2].split('\t')[-1][:-1] # strip newline
                    if post and '-' == next_token and digit_matcher.match(next2_token) is not None:
                        post_list.append(post)
                        post = []
                post.append((token, name_entity))
            if post:
                post_list.append(post)

        txt_filename = conll_filename[:-len("conll")] + "txt"
        with open(txt_filename, encoding='UTF-8', mode='r') as txt_file:
            lines = txt_file.readlines()
            post_body = ''
            for i in range(len(lines)):
                if (question_ptn.match(lines[i]) and i != 0):
                    post_text_list.append(post_body)
                    post_body = lines[i]
                else:
                    post_body += lines[i]
            post_text_list.append(post_body)
    
    # random.shuffle(post_list)
    dataset_size = len(post_list)
    indices = list(range(dataset_size))

    random.seed(seed)
    random.shuffle(indices)

    # don't mind this folks
    partition_sizes = ([dataset_size // K + 1] * (dataset_size % K)) + ([dataset_size // K] * (K - (dataset_size % K)))

    previous_last = 0
    for k in range(K):
        train_indices = indices[:previous_last] + indices[previous_last + partition_sizes[k]:]
        test_indices = indices[previous_last:previous_last + partition_sizes[k]]

        train_list = [post_list[i] for i in train_indices]
        test_list = [post_list[i] for i in test_indices]
        test_text_list = [post_text_list[i] for i in test_indices]
        
        previous_last = previous_last + partition_sizes[k]

        assert len(train_list) + len(test_list) == dataset_size, 'sumting wong!'

        with open('train/test-%d.txt' % k, mode='w', encoding='UTF-8') as txt_file:
            txt_file.write(''.join(test_text_list))

        with open('train/train-%d.tsv' % k, mode='w', encoding='UTF-8') as train_file, open('train/test-%d.tsv' % k, mode='w', encoding='UTF-8') as test_file:
            for post in train_list:
                for token, name_entity in post:
                    train_file.write('%s\t%s\n' % (token, name_entity))
            for post in test_list:
                for token, name_entity in post:
                    test_file.write('%s\t%s\n' % (token, name_entity))
