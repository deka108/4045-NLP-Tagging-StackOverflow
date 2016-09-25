import os
import sys
import json
import io
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
    'a',
    }

IGNORED_TAG = {
    'span',
    'ol',
    'ul',
    'a',
    }

REJECTED_TAG = {
    'pre',
    'blockquote',
    }

datapath_java = [
    'data\\data_2011-01-01-2011-06-30_java.json',
    'data\\data_2011-07-01-2011-12-31_java.json',
    'data\\data_2012-01-01-2012-06-30_java.json',
    'data\\data_2012-07-01-2012-12-31_java.json',
    'data\\data_2013-01-01-2013-06-30_java.json',
    'data\\data_2013-07-01-2013-12-31_java.json',
    'data\\data_2014-01-01-2014-06-30_java.json',
    'data\\data_2014-07-01-2014-12-31_java.json',
    'data\\data_2015-01-01-2015-06-30_java.json',
    'data\\data_2015-07-01-2015-12-31_java.json'
]

def flatten(node):
    result = []
    if isinstance(node, Tag):
        tag_name = node.name

        if tag_name in REJECTED_TAG:
            result.append('#%s' % tag_name)

        elif tag_name in ACCEPTED_TAG:

            if tag_name not in IGNORED_TAG:
                result.append('#%s' % tag_name)

            for child in node.children:
                result.extend(flatten(child))

        elif tag_name == 'code':
            result.append(node.__str__())

        else:
            # I have no idea what to do here
            pass

    elif isinstance(node, NavigableString):
        stripped_str = node.string.strip()

        if stripped_str:
            tokens = nltk.word_tokenize(stripped_str)
            result.extend(tokens)

    return result


def clean(html_str):
    souped = bsoup(html_str.strip(), 'html.parser')

    result = []
    for element in souped.find_all(True, recursive=False):
        result.extend(flatten(element))

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
    with io.open(input_filename, encoding='UTF-8', mode='r') as input_fileptr:
        json_data = json.load(input_fileptr)

    # with open(input_filename, encoding='UTF-8', mode='r') as input_fileptr:
    #     json_data = json.load(input_fileptr)

        output_arr = output['items']
        for item in json_data['items']:
            entry = {}

            entry['tokens'] = clean(item['body'])
            entry['answer_count'] = item['answer_count']
            entry['question_id'] = item['question_id']
            if 'answer_id' in item:
                entry['answer_id'] = item['answer_id']

            output_arr.append(entry)

            answers = item.get('answers')

            if answers:
                # Nested post
                for ans in item['answers']:
                    output_arr.append({
                        'tokens': clean(ans['body']),
                        'question_id': item['question_id'],
                        'answer_id': ans['answer_id'],
                        })

    if output_filename:
        with io.open(output_filename, encoding='UTF-8', mode='w') as output_fileptr:
            output_fileptr.write(unicode(json.dumps(output)))

        # with open(output_filename, encoding='UTF-8', mode='w') as output_fileptr:
        #     json.dump(output, output_fileptr)

    else:
        print(json.dumps(output, indent=4))
