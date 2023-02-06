import requests
import json
import csv
import get_lifecycyle
import time
import pandas as pd

question_list = []

def search_OS(position, keyword, tag, type):
    url = ""
    if type == 'text':
        url = "http://api.stackexchange.com/2.3/search/advanced?pagesize=100&order=desc&sort=votes&answers=1&{}={}&site=stackoverflow".format(position, keyword)
    elif type == 'tag':
        url = "http://api.stackexchange.com/2.3/search/advanced?pagesize=100&order=desc&sort=votes&answers=1&tagged={}&site=stackoverflow".format(tag)
    title_list, url_list, id_list, tags_list  = [], [], [], []
    last_activity_date_list, creation_date_list, is_answered_list = [], [], []
    num = 0
    print(url)
    response = requests.get(url)
    text = response.text
    data = json.loads(text)
    for post in data["items"]:
        title = post["title"]
        url_list.append(post["link"])
        title_list.append(post["title"])
        id_list.append(post["question_id"])
        last_activity_date_list.append(post["last_activity_date"])
        creation_date_list.append(post["creation_date"])
        is_answered_list.append(post["is_answered"])
        tags_list.append(post["tags"])
        num += 1
    print(num)
    return id_list, url_list, tags_list, title_list, creation_date_list, last_activity_date_list, is_answered_list, num

fl_name = 'data/SO/init.csv'
f_os = open(fl_name, 'w', encoding="utf-8")
writer_os = csv.writer(f_os, delimiter=',')
writer_os.writerow(['id', 'url', 'label', 'title', 'created_time', 'last_activity_date'])

all_num = 0

exclude_words = ["install"]

tag_list = ["tensorflow-federated", "federated-learning", "pysyft"]
for tag in tag_list:
    id_list3, url_list3, label_list3, title_list3, creation_date_list3, last_activity_date_list3, is_answered_list3, num3 = search_OS(None, None, tag, 'tag')
    #     print("{} Search from title: {}".format(fl, num))
    for i in range(num3):
        if id_list3[i] not in question_list and is_answered_list3[i]:
            question_list.append(id_list3[i])
            timeArray = time.localtime(creation_date_list3[i])
            creation_date3 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            timeArray2 = time.localtime(last_activity_date_list3[i])
            last_activity_date3 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray2)
            writer_os.writerow(
                [id_list3[i], url_list3[i], label_list3[i], title_list3[i], creation_date3, last_activity_date3])
            all_num += 1

fl_list = ["tensorflow_federated", "tensorflow+federated", "syft", "PySyft", "flwr", "fedlearner","federated+learning","paddle_fl", "PaddleFL","fedavg"]
for fl in fl_list:
    id_list, url_list, label_list, title_list, creation_date_list, last_activity_date_list, is_answered_list, num = search_OS(
        "title", fl, None, 'text')

    for i in range(num):
        if id_list[i] not in question_list and is_answered_list[i]:
            question_list.append(id_list[i])
            timeArray = time.localtime(creation_date_list[i])
            creation_date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            timeArray2 = time.localtime(last_activity_date_list[i])
            last_activity_date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray2)
            writer_os.writerow(
                [id_list[i], url_list[i], label_list[i], title_list[i], creation_date, last_activity_date])
            all_num += 1

    id_list2, url_list2, label_list2, title_list2, creation_date_list2, last_activity_date_list2, is_answered_list2, num2 = search_OS(
        "body", fl, None, 'text')
    for i in range(num2):
        if id_list2[i] not in question_list and is_answered_list2[i]:
            question_list.append(id_list2[i])
            timeArray3 = time.localtime(creation_date_list2[i])
            creation_date2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray3)
            timeArray4 = time.localtime(last_activity_date_list2[i])
            last_activity_date2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray4)
            writer_os.writerow(
                [id_list2[i], url_list2[i], label_list2[i], title_list2[i], creation_date2, last_activity_date2])
            all_num += 1

print("All number: {}".format(all_num))
f_os.close()