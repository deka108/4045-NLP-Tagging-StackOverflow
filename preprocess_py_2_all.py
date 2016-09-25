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
    'data/data_2011-01-01-2011-06-30_java.json',
    'data/data_2011-07-01-2011-12-31_java.json',
    'data/data_2012-01-01-2012-06-30_java.json',
    'data/data_2012-07-01-2012-12-31_java.json',
    'data/data_2013-01-01-2013-06-30_java.json',
    'data/data_2013-07-01-2013-12-31_java.json',
    'data/data_2014-01-01-2014-06-30_java.json',
    'data/data_2014-07-01-2014-12-31_java.json',
    'data/data_2015-01-01-2015-06-30_java.json',
    'data/data_2015-07-01-2015-12-31_java.json'
]
stat_file_path = "Stat/all_statistic.txt"

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


def preprocess_json(input_filename):
    output = {'items': []}
    total_answer = 0
    total_question = 0

    with io.open(input_filename, encoding='UTF-8', mode='r') as input_fileptr:
        json_data = json.load(input_fileptr)
        questions = json_data.get('items')

        output_arr = output['items']
        total_question += len(questions)

        for item in questions:
            entry = {}

            entry['tokens'] = clean(item['body'])
            entry['answer_count'] = item['answer_count']
            entry['question_id'] = item['question_id']
            if 'answer_id' in item:
                entry['answer_id'] = item['answer_id']

            output_arr.append(entry)

            # Nested post
            answers = item.get('answers')
            if answers:
                total_answer += len(answers)

                for ans in answers:
                    output_arr.append({
                        'tokens': clean(ans['body']),
                        'question_id': item['question_id'],
                        'answer_id': ans['answer_id'],
                    })
            else:
                print entry['question_id'], 'in', input_filename,\
                    'does not have any answers'

    output_filename = input_filename.replace('data/data',
                                             'preprocessed/preprocessed')
    if output_filename:
        with io.open(output_filename, encoding='UTF-8',
                     mode='w') as output_fileptr:
            output_fileptr.write(unicode(json.dumps(output)))
    else:
        print(json.dumps(output, indent=4))
        
    return total_question, total_answer


if __name__ == '__main__':
    agg_total_answer = 0
    agg_total_question = 0

    open(stat_file_path, "w").close()

    for input_path in datapath_java:
        total_question, total_answer = preprocess_json(input_path)

        with open(stat_file_path, "a") as stat_file:
            stat_file.write(input_path + "\n")
            stat_file.write("Total question posts: " + str(total_question) +
                            "\n")
            stat_file.write("Total answer posts: " + str(total_answer) +
                            "\n")
            stat_file.write("Total posts: " + str(total_question +
                                                 total_answer) + "\n")

        agg_total_question += total_question
        agg_total_answer += total_answer

    with open(stat_file_path, "a") as stat_file:
        stat_file.write("Aggregate total question posts: " +
                        str(agg_total_question) + "\n")
        stat_file.write("Aggregate total answer posts: " +
                        str(agg_total_answer) + "\n")
        stat_file.write("Aggregate total posts: " +
                        str(agg_total_question + agg_total_answer) + "\n")