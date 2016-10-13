import os
import re
import sys
import json
import pprint
from getopt import getopt

import nltk
from bs4 import BeautifulSoup as bsoup
from bs4.element import Tag, NavigableString, Comment

ACCEPTED_TAG = {
    'p',
    'li',
    'span',
    'ol',
    'ul',
    }

NO_REPR = {
    'p',
    'span',
    'ol',
    'ul',
    }

REJECTED_TAG = {
    'pre',
    'blockquote',
    'a',
    'img',
    }

strsyn_matcher = re.compile('"(?:\\\\"|[^"])*"')
charsyn_matcher = re.compile("'(?:\\\\.|.)?'")
parentheses_matcher = re.compile('\\([^()]*(?:\\([^()]*(?:\\([^()]*(?:\\([^()]*(?:\\([^()]*(?:\\([^()]*(?:\\([^()]*\\)[^()]*)*\\)[^()]*)*\\)[^()]*)*\\)[^()]*)*\\)[^()]*)*\\)[^()]*)*[^()]*\\)')

def simplify(code_str):
    # print('--------------------------------------------------------------')
    # print(code_str)
    code_str = strsyn_matcher.sub('_str', code_str)
    # print(code_str)
    code_str = charsyn_matcher.sub('_char', code_str)
    # print(code_str)
    code_str = parentheses_matcher.sub('(_exprs)', code_str)
    # print(code_str)
    return code_str


def flatten(node):
    assert isinstance(node, Tag) or isinstance(node, NavigableString), 'expected class Tag or NavigableString, got %s instead' % str(type(node))

    if isinstance(node, Tag):
        tag_name = node.name

        if tag_name in REJECTED_TAG:
            result = '#%s' % tag_name

        elif tag_name in ACCEPTED_TAG:
            temp = []
            if tag_name not in NO_REPR:
                # only <li> for now
                temp.append('#%s' % tag_name)

            for child in node.children:
                temp.append(flatten(child))
            temp = list(filter(''.__ne__, temp))
            result = ' '.join(temp)

        elif tag_name == 'code':
            result = simplify(node.string.strip())

        else:
            # I have no idea what to do here
            result = ''

        return result

    elif isinstance(node, NavigableString):
        return node.string.strip()


def clean(html_str):
    souped = bsoup(html_str.strip(), 'html.parser')

    temp = []
    for element in souped.find_all(True, recursive=False):
        temp.append(flatten(element))

    return ' '.join(temp)

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)

    args = sys.argv[1:]
    parsed, args = getopt(args, 'i:o:')

    input_filename = ''
    output_filename = ''
    for opt, val in parsed:
        if opt == '-i':
            input_filename = val
        elif opt == '-o':
            output_filename = val

    assert os.path.isfile(input_filename), 'Example usage: python preprocess.py -i <json_inputfile> [-o <json_outputfile>]'

    output = {'items': []}
    with open(input_filename, encoding='UTF-8', mode='r') as input_fileptr:
        json_data = json.load(input_fileptr)

        output_arr = output['items']
        for item in json_data['items']:
            entry = {}

            entry['cleaned'] = clean(item['body'])
            entry['question_id'] = item['question_id']
            if 'answer_id' in item:
                entry['answer_id'] = item['answer_id']

            output_arr.append(entry)

    if not output_filename:
        f_out = input_filename.split("/")[1]
        f_out = f_out[:len(f_out) - len('.json')] + ".txt"
        output_filename = os.path.join("api_preprocessed", f_out)

    with open(output_filename, encoding='UTF-8', mode='w') as output_fileptr:
        json.dump(output,
            output_fileptr,
            indent=4,
            )

    # else:
    #     print(json.dumps(output, indent=4))
