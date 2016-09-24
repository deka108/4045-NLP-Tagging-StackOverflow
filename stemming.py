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

with io.open('processed.json', "r", encoding="utf-8") as source_file:
    data = json.load(source_file)

def preprocess(data,after):
    stemmer = SnowballStemmer("english")
    lst = {}
    json_new = {'tokens':[]}
    stopword = set(stopwords.words('english'))
    for i,item in enumerate(data['items'],0):
        for j,(token) in enumerate(item['tokens'],0):
            if re.match('^\w+',token) and token.lower() not in stopword:
                if after:
                    json_new['tokens'].append(stemmer.stem(item['tokens'][j]))
                else:
                    json_new['tokens'].append(item['tokens'][j])
    lst = Counter(json_new['tokens'])
    return lst

def stem(data,after= False):
    lst = preprocess(data,after)
    dct = [(value,key) for key,value in lst.iteritems()]
    dct.sort(reverse=True)
    with io.open('Stat/stem.txt', "w+", encoding="utf-8") as dest_file:
        dest_file.write(unicode('\n The 20 most frequent words are :\n'))
        for i,(count, word) in enumerate(dct[:20],1):
            dest_file.write(unicode('{}. {} {}\n'.format(i, count, word)))

# True for looking after stemming
stem(data,True)