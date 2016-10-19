import os
import sys
import re
import time

from getopt import getopt

filename = ''

args = sys.argv[1:]
opts, args = getopt(args, '', ['filename='])

for option, value in opts:
    if option == '--filename':
        filename = value

assert os.path.isfile(filename), 'invalid filename!'

nerline_matcher = re.compile('([^\\t]+)\\t([^\\t]+)\\t([^\\t]+)\\n')
digit_matcher = re.compile('\\d{6,}')
with open(filename, mode='r', encoding='latin_1') as filepointer:
    lines = list(filter(lambda line: nerline_matcher.match(line) is not None, filepointer.readlines()))

error = []
error_list = []
for i in range(len(lines)):
    line = lines[i]
    token, human, predicted = nerline_matcher.match(line).groups()
    if 'Question' == token and i + 2 < len(lines):
        next_token = nerline_matcher.match(lines[i + 1]).group(1)
        next2_token = nerline_matcher.match(lines[i + 2]).group(1)
        if '-' == next_token and digit_matcher.match(next2_token) is not None:
            if error:
                error_list.extend(error)
            error = lines[i:i+7]
    if human[1:] != predicted[1:]:
        error.append(line)
if error:
    error_list.extend(error)

with open('error_filter.out', mode='w', encoding='latin_1') as filepointer:
    filepointer.write(''.join(error_list))
