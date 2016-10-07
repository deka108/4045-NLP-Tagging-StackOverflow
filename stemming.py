from collections import Counter
from nltk.corpus import stopwords
import json
import io
import nltk
import re
from collections import Counter
from nltk.stem.snowball import SnowballStemmer

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


def read_json(file_path):
    with io.open(file_path, "r", encoding="utf-8") as source_file:
        data = json.load(source_file)
    return data


def preprocess(file_paths, after):
    stemmer = SnowballStemmer("english")
    lst = {}
    json_new = {'tokens': []}
    stopword = set(stopwords.words('english'))
    stopword.add("n't")
    stopword.add("would")

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


def stem(after=False):
    lst = preprocess(preprocessed_path_java, after)

    dct = [(value,key) for key,value in lst.iteritems()]
    dct.sort(reverse=True)

    if after:
        stem_file_path = 'Stat/stemmed_after.txt'
    else:
        stem_file_path = 'Stat/stemmed_before.txt'

    with io.open(stem_file_path, "w+", encoding="utf-8") as dest_file:
        dest_file.write(unicode('The 20 most frequent words are :\n'))
        for i,(count, word) in enumerate(dct[:20], 1):
            dest_file.write(unicode('{}. {} {}\n'.format(i, count, word)))

# True for looking after stemming
stem()