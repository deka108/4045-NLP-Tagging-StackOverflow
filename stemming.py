from nltk.corpus import stopwords
import json
import io
import re
from collections import Counter
from nltk.stem.snowball import SnowballStemmer
import fileinput
from string import punctuation
import nltk

# if you havent download stopwords
# nltk.download('stopwords')

preprocessed_path_java = [
    'preprocessed/preprocessed_2011-01-01-2011-06-30_java.json',
    'preprocessed/preprocessed_2011-07-01-2011-12-31_java.json',
    'preprocessed/preprocessed_2012-01-01-2012-06-30_java.json',
    'preprocessed/preprocessed_2012-07-01-2012-12-31_java.json',
    'preprocessed/preprocessed_2013-01-01-2013-06-30_java.json',
    'preprocessed/preprocessed_2013-07-01-2013-12-31_java.json',
    'preprocessed/preprocessed_2014-01-01-2014-06-30_java.json',
    'preprocessed/preprocessed_2014-07-01-2014-12-31_java.json',
    'preprocessed/preprocessed_2015-01-01-2015-06-30_java.json',
    'preprocessed/preprocessed_2015-07-01-2015-12-31_java.json'
]

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
# FILE_DEST = 'Stat\\'
FILE_DEST = 'Stat_API\\'

def read_json(file_path):
    with io.open(file_path, "r", encoding="utf-8") as source_file:
        data = json.load(source_file)
    return data

def strip_punctuation(w):
    return''.join(s for s in w if s not in punctuation)

def preprocess(file_paths, after,choice):
    stemmer = SnowballStemmer("english")
    json_new = {'tokens': []}
    stopword = set(stopwords.words('english'))
    stopword.add("n't")
    stopword.add("would")
    if choice.lower() == "json":
        for file_path in file_paths:
            data = read_json(file_path)
            for i,item in enumerate(data['items'],0):
                for j,(token) in enumerate(item['tokens'],0):
                    if re.match('^\w+',token) and token.lower() not in stopword:
                        if after:
                            json_new['tokens'].append(stemmer.stem(item['tokens'][j]))
                        else:
                            json_new['tokens'].append(item['tokens'][j])
        lst = Counter(json_new['tokens'])
        return lst
    else:
        source = fileinput.input(file_paths)
        for line in source:
            sentence = line.split()
            for word in sentence:
                if re.match('^\w+[\.\,\?\!\:\;]$', word):
                    word = strip_punctuation(word)
                if re.match('^\w+', word) and word.lower() not in stopword:
                    if isinstance(word,str):
                        word = word.decode('utf-8')
                    if after:
                        json_new['tokens'].append(stemmer.stem(word))
                    else:
                        json_new['tokens'].append(word)
        source.close()
        lst = Counter(json_new['tokens'])
        return lst

def stem(path,choice,after=False):
    if choice=='json':
        lst = preprocess(preprocessed_path_java, after,choice)
    else:
        lst = preprocess(api_preprocessed_path, after,choice)
    dct = [(value,key) for key,value in lst.iteritems()]
    dct.sort(reverse=True)
    if after:
        stem_file_path = path + 'stemmed_after.txt'
    else:
        stem_file_path = path + 'stemmed_before.txt'

    with io.open(stem_file_path, "w+",encoding='utf-8') as dest_file:
        dest_file.write(unicode('The 20 most frequent words are :\n'))
        for i,(count, word) in enumerate(dct[:20], 1):
            dest_file.write(unicode('{}. {} {}\n'.format(i, count, word)))

# True for looking after stemming
stem(FILE_DEST,choice = 'api',after=True)