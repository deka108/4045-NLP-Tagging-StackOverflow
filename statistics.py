
import io
import pandas
import os
import re
import matplotlib.pyplot as plt

questions_list = []

# change the index

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
FILE_DEST = 'Stat\\'
# FILE_DEST = 'Stat_API\\'

def read_json(file_path):
    with io.open(file_path, "r", encoding="utf-8") as source_file:
        data = pandas.read_json(source_file)
    return data

def len_of_posts(dataset,path):
    total_all = 0
    for file_path in dataset:
        len_file = open(path + "post length.txt", "a+")
        len_file.write("DATA : {}".format(file_path))
        total = 0
        i = -1
        questions_id = ''
        data = read_json(file_path)
        for item in data['items']:
            if questions_id != item['question_id']:
                if i >=0:
                    # change path for another data
                    len_file.write("length of pos {} : {}\n".format(i, count))
                i += 1
                count = 0
                questions_id = item['question_id']
            for token in item['tokens']:
                count += len(re.findall(r'^\w+',token))
            total += count
        len_file.write("length of pos {} : {}\n".format(i, count))
        len_file.write("total:{} \n".format(total))
        total_all += total
    len_file.write("total number of posts:{} \n".format(total_all))
    len_file.close()


def get_statistics(dataset,path):
    answer_file = []
    with open(path +"statistic.txt", "w+") as del_file:
        del_file.write('')
    for file_path in dataset:
        item_count = 0
        num_of_answers = 0
        data = read_json(file_path)
        for item in data["items"]:
            if 'answer_count' in item:
                answer_file.append(item["answer_count"])
                num_of_answers += item["answer_count"]
                item_count += 1

        with open(path+"statistic.txt", "a+") as stat_file:
            if os.stat(path+ "statistic.txt").st_size != 0:
                for line in stat_file:
                    ques,ans = (item.strip('}') for item in line.split(','))
                    ques = int(ques.split(':')[1]) + item_count
                    ans = int(ans.split(':')[1]) + num_of_answers
                print("1.2.3.4.5 {} , {}".format(item_count,num_of_answers))
                print ques,ans
                info = dict(zip(('total questions','total answers'),(ques,ans)))
                with open (path +"statistic.txt", "w+") as temp_file:
                    temp_file.write(str(info))
            else:
                print 'yes'
                info = dict(zip(('total questions', 'total answers'), (item_count, num_of_answers)))
                stat_file.write(str(info))
    return answer_file


def create_histo(data,path):
    # change the upper limit if you want to make bigger histogram e.g.
    # e.g. 12 means that answer counts above 12 will be combined with 12
    upper_limit = 20
    temp_list = []
    for i in data:
        if i >= upper_limit:
            temp_list.append(upper_limit)
        else:
            temp_list.append(i)
    df = pandas.DataFrame(temp_list)
    plt.hist(df[0], bins =upper_limit, range=(1,upper_limit),  align= 'mid', histtype='bar')
    plt.xticks(range(1, upper_limit+1, 1))
    # plt.yticks(range(0,100))
    plt.xlabel('# of answers')
    plt.ylabel('Distribution value')
    plt.title('Answer Distribution')
    # plt.show()
    # change the save path for other pict
    plt.savefig(path+'histogram.png')


len_of_posts(api_preprocessed_path,FILE_DEST)
stats_file = get_statistics(api_preprocessed_path,FILE_DEST)
create_histo(stats_file,FILE_DEST)


