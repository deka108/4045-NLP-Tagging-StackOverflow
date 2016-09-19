from bs4 import BeautifulSoup,NavigableString
import io , json

# change the path later on
datapath_java = ['data//data_2012-01-01-2012-06-30_java.json',
'data//data_2011-01-01-2011-06-30_java.json',
'data//data_2011-07-01-2011-12-31_java.json',
'data//data_2012-01-01-2012-06-30_java.json',
'data//data_2012-07-01-2012-12-31_java.json',
'data//data_2013-01-01-2013-06-30_java.json',
'data//data_2013-07-01-2013-12-31_java.json',
'data//data_2014-01-01-2014-06-30_java.json',
'data//data_2014-07-01-2014-12-31_java.json',
'data//data_2015-01-01-2015-06-30_java.json',
'data//data_2015-07-01-2015-12-31_java.json'
]

# change the path later on
datapath = [
'data//data_2011-01-01-2011-06-30.json',
'data//data_2011-07-01-2011-12-31.json',
'data//data_2012-01-01-2012-06-30.json',
'data//data_2012-07-01-2012-12-31.json',
'data//data_2013-01-01-2013-06-30.json',
'data//data_2013-07-01-2013-12-31.json',
'data//data_2014-01-01-2014-06-30.json',
'data//data_2014-07-01-2014-12-31.json',
'data//data_2015-01-01-2015-06-30.json',
'data//data_2015-07-01-2015-12-31.json'
]
invalid_tags = ["p","li","ul","hr"]
json_list = []
index = 100
# change the index
source_file = io.open(datapath_java[3], "r", encoding="utf-8")
# change the path
dest_file = io.open("data//parsed.json", "w+", encoding="utf-8")
# add another tag if you want to delete the content as well before preprocessed

# def delete_pre(html, invalid_tags):
#     soup = BeautifulSoup(html, "html.parser")
#     for tag in soup.find_all(True):
#         if tag.name in invalid_tags:
#             tag.decompose()
#     return soup

def delete_tag(html, invalid_tags):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(True):
        if tag.name in invalid_tags:
            s = ""
            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = delete_tag(unicode(c), invalid_tags)
                s += unicode(c)
            tag.replace_with(s)

    return soup

data = json.load(source_file)
for i in xrange(0, index):
    count =  data["items"][i]["answer_count"]
    json_list.append({
        "body": delete_tag(data["items"][i]["body"],invalid_tags).prettify(formatter="html"),
        # "body": BeautifulSoup(data["items"][i]["body"], "html.parser").get_text(),
        # use the below one if you want to delete the multi line block
        # "body": delete_pre(data["items"][i]["body"],invalid_tags).get_text(),
        "tags": data["items"][i]["tags"],
        "title": data["items"][i]["title"],
        "answer_count":count,
        "link": data["items"][i]["link"],
        "question_id": data["items"][i]["question_id"],
        "answers":[]
    })
    for j in xrange(0, count):
        json_list[i]["answers"].append({
            "body": delete_tag(data["items"][i]["answers"][j]["body"], invalid_tags).prettify(formatter="html"),
            # "body": BeautifulSoup(data["items"][i]["answers"][j]["body"], "html.parser").get_text(),
            # use the below one if you want to delete the multi line block
            # "body": delete_pre(data["items"][i]["answers"][j]["body"], invalid_tags).get_text(),
            "tags": data["items"][i]["answers"][j]["tags"],
            "title": data["items"][i]["answers"][j]["title"],
            "link": data["items"][i]["answers"][j]["link"],
            "answer_id": data["items"][i]["answers"][j]["answer_id"],
        })

dest_file.write(unicode(json.dumps({"item":json_list})))


