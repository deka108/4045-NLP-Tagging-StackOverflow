
import io
import pandas
import os
import re
import matplotlib.pyplot as plt

questions_list = []

# change the index
with io.open('processed.json', "r", encoding="utf-8") as source_file:
    data = pandas.read_json(source_file)


def len_of_posts(data):
    i=-1
    total=0
    questions_id=''
    for item in data['items']:
        if questions_id != item['question_id']:
            if i >=0:
                # change path for another data
                with open("Stat\\post length.txt", "a+") as len_file:
                    len_file.write("length of pos {} : {}\n".format(i, count))
            i += 1
            count = 0
            questions_id = item['question_id']
        for token in item['tokens']:
            count += len(re.findall(r'^\w+',token))
        total += count
    # change path for another data
    with open("Stat\\post length.txt", "a+") as len_file:
        len_file.write("length of pos {} : {}\n".format(i, count))
        len_file.write("total length:{} \n".format(total))
    # change path for another data


def get_statistics(data):
    info = {}
    item_count = 0
    num_of_answers = 0
    answer_file = []
    for item in data["items"]:
        if 'answer_count' in item:
            answer_file.append(item["answer_count"])
            num_of_answers += item["answer_count"]
            item_count += 1

    with open("Stat\\statistic.txt", "a+") as stat_file:
        if os.stat("Stat\\statistic.txt").st_size != 0:
            for line in stat_file:
                ans,ques = (item.strip('}') for item in line.split(','))
                ques = int(ques.split(':')[1]) + item_count
                ans = int(ans.split(':')[1]) + num_of_answers
            info = dict(zip(('total questions','total answers'),(ques,ans)))
        else:
            info = dict(zip(('questions', 'answers'), (item_count, num_of_answers)))

    with open("Stat\\statistic.txt", "w+") as file:
        file.write(str(info))

    return answer_file


def create_histo(data):
    # change the upper limit if you want to make bigger histogram e.g.
    # e.g. 12 means that answer counts above 12 will be combined with 12
    upper_limit = 12
    temp_list = []
    for i in data:
        if i >= upper_limit:
            temp_list.append(upper_limit)
        else:
            temp_list.append(i)
    df = pandas.DataFrame(temp_list)
    plt.hist(df[0], bins =upper_limit, range=(1,upper_limit),  align= 'mid', histtype='bar')
    plt.xticks(range(1, upper_limit+1, 1))
    plt.yticks(range(0, max(df[0].value_counts())+2))
    plt.xlabel('# of answers')
    plt.ylabel('Distribution value')
    plt.title('Answer Distribution')
    # plt.show()
    # change the save path for other pict
    plt.savefig('Stat\\histogram.png')


len_of_posts(data)
stats_file = get_statistics(data)
create_histo(stats_file)


