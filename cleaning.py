from bs4 import BeautifulSoup,NavigableString
import io , json

# change the path later on
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

# change the path later on
datapath = [
'data\\data_2011-01-01-2011-06-30.json',
'data\\data_2011-07-01-2011-12-31.json',
'data\\data_2012-01-01-2012-06-30.json',
'data\\data_2012-07-01-2012-12-31.json',
'data\\data_2013-01-01-2013-06-30.json',
'data\\data_2013-07-01-2013-12-31.json',
'data\\data_2014-01-01-2014-06-30.json',
'data\\data_2014-07-01-2014-12-31.json',
'data\\data_2015-01-01-2015-06-30.json',
'data\\data_2015-07-01-2015-12-31.json'
]
valid_tags = ["p", "code", "pre", "blockquote"]
json_list = []
index = 100
# change the index
source_file = io.open(datapath_java[2], "r", encoding="utf-8")
# change the path
dest_file = io.open("data\\parsed.json", "w+", encoding="utf-8")

def delete_tag(html, valid_tags):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(True):
        if tag.name not in valid_tags:
            s = ""
            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = delete_tag(unicode(c), valid_tags)
                s += unicode(c)
            tag.replace_with(s)
        # else:
        #     if tag.name in replace_tags:
    return soup.get_text()

data = json.load(source_file)
for i in xrange(0, index):
    count =  data["items"][i]["answer_count"]
    json_list.append({
        "body": delete_tag(data["items"][i]["body"],valid_tags),
        "tags": data["items"][i]["tags"],
        "title": data["items"][i]["title"],
        "answer_count":count,
        "link": data["items"][i]["link"],
        "question_id": data["items"][i]["question_id"],
        "answers":[]
    })
    for j in xrange(0, count):
        json_list[i]["answers"].append({
            "body": delete_tag(data["items"][i]["answers"][j]["body"], valid_tags),
            "tags": data["items"][i]["answers"][j]["tags"],
            "title": data["items"][i]["answers"][j]["title"],
            "link": data["items"][i]["answers"][j]["link"],
            "answer_id": data["items"][i]["answers"][j]["answer_id"],
        })

dest_file.write(unicode(json.dumps({"item":json_list})))


