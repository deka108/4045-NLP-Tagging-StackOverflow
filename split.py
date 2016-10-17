import os
import sys
import time
import math
import random

import csv

from getopt import getopt

if '__main__' == __name__:
    test_ratio = 0.3
    args = sys.argv[1:]
    opts, args = getopt(args, '', ['conll='])
    conll_inputs=''
    for option, value in opts:
        if '--conll' == option:
            conll_inputs=value
    assert conll_inputs, 'Provide .conll file(s)!, e.g.:\npython train.py --conll=file1.conll,file2.conll,file3.conll'
    post_list = []
    for conll_filename in conll_inputs.split(','):
        post = []
        with open(conll_filename, encoding='UTF-8', mode='r') as conll_file:
            for line in conll_file:
                line = line.strip()
                if not line:
                    continue
                name_entity, _, _, token = line.split('\t')
                if 'Question' == token:
                    if post:
                        post_list.append(post)
                    post = []
                post.append((token, name_entity))
            if post:
                post_list.append(post)
    random.shuffle(post_list)
    dataset_size = len(post_list)
    test_size = int(test_ratio * dataset_size)
    train_size = dataset_size - test_size
    train_list = post_list[:train_size]
    test_list = post_list[-test_size:]
    with open('train.tsv', mode='w', encoding='UTF-8') as train_file, open('test.tsv', mode='w', encoding='UTF-8') as test_file:
        for post in train_list:
            for token, name_entity in post:
                train_file.write('%s\t%s\n' % (token, name_entity))
        for post in test_list:
            for token, name_entity in post:
                test_file.write('%s\t%s\n' % (token, name_entity))