import os
import re
import sys
import json
import pprint
from getopt import getopt

import nltk
from bs4 import BeautifulSoup as bsoup
from bs4.element import Tag, NavigableString, Comment

REJECTED_TAG = {
    'blockquote',
    'img',
    }

strsyn_matcher = re.compile('"(?:\\\\"|[^"])*"')
charsyn_matcher = re.compile("'(?:\\\\.|.)?'")
parentheses_matcher = re.compile('\\([^()]*(?:\\([^()]*(?:\\([^()]*(?:\\([^()]*(?:\\([^()]*(?:\\([^()]*(?:\\([^()]*\\)[^()]*)*\\)[^()]*)*\\)[^()]*)*\\)[^()]*)*\\)[^()]*)*\\)[^()]*)*[^()]*\\)')
oneline_matcher = re.compile('^[^;]+;\\w*$|^[^\\n]+\\n?$')
link_matcher = re.compile('https?://')
whitespaces_matcher = re.compile('\\s+')

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

        result = ''
        if tag_name in REJECTED_TAG:
            result = '#%s' % tag_name

        elif tag_name == 'code':
            # textContent only
            result = simplify(node.text.strip())

        elif tag_name == 'pre':
            # one line textContent only
            pre_txt = node.text
            matches = oneline_matcher.match(pre_txt)

            result = '#pre'
            if matches is not None:
                result = simplify(pre_txt.strip())

        elif tag_name == 'a':
            # one line textContent only
            a_txt = node.text
            matches = link_matcher.match(a_txt)

            result = '#a'
            if matches is None:
                result = a_txt.strip()

        else:
            temp = []
            if tag_name == 'li':
                # only <li> for now
                temp.append('#%s' % tag_name)

            for child in node.children:
                temp.append(flatten(child))
            temp = list(filter(''.__ne__, temp))
            result = ' '.join(temp)

        return result

    elif isinstance(node, NavigableString):
        return node.string.strip()


def clean(html_str):
    souped = bsoup(html_str.strip(), 'html.parser')

    temp = []
    for element in souped.find_all(True, recursive=False):
        temp.append(flatten(element))

    result = ' '.join(temp)
    result = whitespaces_matcher.sub(' ', result)
    return result

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
    output_txts = []
    with open(input_filename, encoding='UTF-8', mode='r') as input_fileptr:
        json_data = json.load(input_fileptr)

        output_arr = output['items']
        for item in json_data['items']:
            entry = {}
            cleaned_body = clean(item['body'])

            output_txts.append('Question-%d%s' % (int(item['question_id']), ', answer-%d' % int(item['answer_id']) if 'answer_id' in item else ''))
            output_txts.append('%s\n' % cleaned_body)

            entry['cleaned'] = cleaned_body
            entry['question_id'] = item['question_id']
            if 'answer_id' in item:
                entry['answer_id'] = item['answer_id']

            output_arr.append(entry)

    if not output_filename:
        print(json.dumps(output, indent=4))

    elif output_filename[-4:] == 'json':
        with open(output_filename, encoding='UTF-8', mode='w') as output_fileptr:
            json.dump(output,
                output_fileptr,
                indent=4,
                )

    elif output_filename[-3:] == 'txt':
        with open(output_filename, encoding='UTF-8', mode='w') as output_fileptr:
            output_str = '\n'.join(output_txts)
            output_fileptr.write(output_str)
