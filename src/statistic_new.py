from __future__ import division
import io
from string import punctuation
import pandas
from collections import Counter
import re
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import fileinput

mydict = {}

FILE_DEST = 'Stat_API\\'
    
api_preprocessed_path = [
    'api_preprocessed\\2011-01-01-2011-06-30.txt',
    'api_preprocessed\\2011-07-01-2011-12-31.txt',
    'api_preprocessed\\2012-01-01-2012-06-30.txt',
    'api_preprocessed\\2012-07-01-2012-12-31.txt',
    'api_preprocessed\\2013-01-01-2013-06-30.txt',
    'api_preprocessed\\2013-07-01-2013-12-31.txt',
    'api_preprocessed\\2014-01-01-2014-06-30.txt',
    'api_preprocessed\\2014-07-01-2014-12-31.txt',
    'api_preprocessed\\2015-01-01-2015-06-30.txt',
    'api_preprocessed\\2015-07-01-2015-12-31.txt'
]

def read_files(file_paths):
    data = fileinput.input(file_paths)
    return data

def strip_punctuation(w):
    return''.join(s for s in w if s not in punctuation)

def len_of_posts(dataset,path):
    quest = re.compile('^Question-\d')
    total_all = 0
    mydict = []
    data = read_files(dataset)
    questions_id =''
    count = 0
    i = -1
    with open(path + 'post_length.txt', 'w+') as test:
        with open(path + 'post_length.txt', 'a+') as dest:
            for lines in data:
                if quest.match(lines):
                    if i >=0:
                        dest.write("length of pos {} : {}\n".format(i, count))
                    i+=1
                    total_all += count
                    count = 0
                else:
                    sentence = lines.split()
                    for word in sentence:
                        if re.match('^\w+[\.\,\?\!\:\;]$', word):
                            word = strip_punctuation(word)
                        if re.match('^\w+', word):
                            count +=1
            dest.write("length of pos {} : {}\n".format(i, count))
            dest.write("total number of posts:{} \n".format(total_all))
    data.close()

def get_statistics(data,path):
    answer_file = []
    total_quest = 0
    total_ans = 0
    total = 0
    ans_list = []
    quest = re.compile('^Question-\d')
    data = fileinput.input(data)
    for lines in data:
        if quest.match(lines):
            line = lines.split(',')
            try:
                test = line[1].strip('\n')
            except IndexError:
                mydict[line[0].strip('\n')] = 1
                total_quest +=1
            else:
                try:
                    mydict[line[0].strip('\n')] += 1
                except KeyError:
                    mydict[line[0].strip('\n')] = 1
                    ans_list.append(line[0].strip('\n'))
                total_ans +=1
    for key in mydict.keys():
        if key in ans_list:
            answer_file.append(mydict[key])
        elif (mydict[key] -1 > 0):
            answer_file.append(mydict[key]-1)
    lst = Counter(mydict)
    with open(path+'num_of_thread.txt','w+') as source:
        source.write("number of Thread in all of the post : \n")
        dst = [(value,key) for (key,value) in lst.iteritems()]
        for i,(answer,quest) in enumerate(dst,0):
            total += answer
            source.write("{}------{}\n".format(answer,quest))
        source.write("total thread:{}\n\ntotal post:{}\n\ntotal questions:{}\n\ntotal answer:{}\n".format(i+1,total,total_quest,total_ans))
    data.close()
    return answer_file

def to_percent(y, position):
    s = str(100 * y)
    return s + '%'

def create_histo(data,path):
    # change the upper limit if you want to make bigger histogram e.g.
    # e.g. 12 means that answer counts above 12 will be combined with 12
    upper_limit = 6
    temp_list = []
    total = 0
    for i in data:
        if i >= upper_limit:
            temp_list.append(upper_limit)
        else:
            temp_list.append(i)
    df = pandas.DataFrame(temp_list)
    bins = range(min(df[0]),max(df[0])+2,1)
    plt.hist(df[0], bins = bins,  align= 'left', histtype='bar',normed = True)
    plt.xticks(bins)
    formatter = FuncFormatter(to_percent)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.xlabel('# of answers')
    plt.ylabel('Distribution value')
    plt.title('Answer Distribution')
    plt.savefig(path+'histogram.png')

if __name__=="__main__":
    len_of_posts(api_preprocessed_path,FILE_DEST)
    stats_file = get_statistics(api_preprocessed_path,FILE_DEST)
    create_histo(stats_file,FILE_DEST)


