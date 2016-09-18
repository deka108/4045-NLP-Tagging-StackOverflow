import json
import os
##################################################

question_index = []

answer_index = {
    # question_index : list of answer_index
    # example
}

##################################################
data_name_javatag = [
    'data_2011-01-01-2011-06-30_java.json',
    'data_2011-07-01-2011-12-31_java.json',
    'data_2012-01-01-2012-06-30_java.json',
    'data_2012-07-01-2012-12-31_java.json',
    'data_2013-01-01-2013-06-30_java.json',
    'data_2013-07-01-2013-12-31_java.json',
    'data_2014-01-01-2014-06-30_java.json',
    'data_2014-07-01-2014-12-31_java.json',
    'data_2015-01-01-2015-06-30_java.json',
    'data_2015-07-01-2015-12-31_java.json'
]
data_dir = 'data'
api_mention_dir = 'api_mention'
api_mention_suffix = '_api_mention.json'


def get_mention_api_path(json_data_file):
    fn = json_data_file[:len(json_data_file) - len('.json')]
    return os.path.join(api_mention_dir, fn + api_mention_suffix)


def extract_api_mention_post(index):
    items = []

    data_path = os.path.join(data_dir, data_name_javatag[index])
    api_mention_path = get_mention_api_path(data_name_javatag[index])
    print api_mention_path

    with open(data_path, "r") as source:
        data = json.load(source)

        for i in question_index:
            items.append({
                "post_type": "question",
                "body": data["items"][i]["body"],
                "tags": data["items"][i]["tags"],
                "title": data["items"][i]["title"],
                "link": data["items"][i]["link"],
                "question_id": data["items"][i]["question_id"]
            })

        # python 2 only
        for key, value in answer_index.iteritems():
            for i in value:
                items.append({
                    "post_type": "answer",
                    "body": data["items"][key]["answers"][i]["body"],
                    "tags": data["items"][key]["answers"][i]["tags"],
                    "title": data["items"][key]["answers"][i]["title"],
                    "link": data["items"][key]["answers"][i]["link"],
                    "answer_id": data["items"][key]["answers"][i]["answer_id"],
                    "question_id": data["items"][key]["question_id"]
                })

        with open(api_mention_path, "w") as target:
            target.write(json.dumps({"items": items}))

# Uncomment and change index of the data path
# extract_api_mention_post(7)