import json
import csv
import re
import jieba
import pandas as pd
import requests
from tqdm import tqdm
from github import Github

def is_match(list_a, list_b):
    for word_a in list_a:
        for word_b in list_b:
            result = re.match(word_a, word_b)
            if result != None:
                return True
    return False

bug_list = ["bug"]
pull_bug_list = ["cla: yes", "cla: no"]
bug_words = ["fix", "broken", "solve", "problem", "bug", "defect", "error", "incorrect", "unsuccessful", "wrong", "fault", "fail", "crash", "nan", "inf"]
token = ""
fl_list = ["OpenMined/PySyft", "FederatedAI/FATE", "tensorflow/federated", "mher/flower", "PaddlePaddle/PaddleFL", "bytedance/fedlearner"]
g = Github(token)

sum_issue = 0
sum_pull = 0
for fl in fl_list:
    search_text = ""
    issue_num = 0
    pull_num = 0
    repo = g.get_repo(fl)
    issues = repo.get_issues(state = "closed")
    
    issuename  = 'data/{}/issues_init.csv'.format(fl.split("/")[1])
    f_issue = open(issuename, 'w', encoding="utf-8")
    writer_issue = csv.writer(f_issue, delimiter='\t')
    writer_issue.writerow(['url', 'label', 'title', 'all_text', 'comments', 'created_time', 'updated_time', 'closed_time'])

    pullname = 'data/{}/PRs_init.csv'.format(fl.split("/")[1])
    f_pull = open(pullname, 'w', encoding="utf-8")
    writer_pull = csv.writer(f_pull, delimiter='\t')
    writer_pull.writerow(['url', 'label', 'title', 'all_text', 'comments','merged', 'created_time', 'updated_time', 'closed_time'])
    
    for i, issuepull in zip(tqdm(range(issues.totalCount)), issues):
        if issuepull.comments >= 1:
            if issuepull.pull_request == None:
                is_issue = True
            else:
                issuepull = repo.get_pull(issuepull.number)
                is_issue = False
                
            html_url = issuepull.html_url
            title = issuepull.title
            body = issuepull.body
            created_time, updated_time, closed_time = issuepull.created_at, issuepull.updated_at, issuepull.closed_at
            comments = issuepull.get_comments()
            comments_text = ""
            for comment in comments:
                comments_text += comment.body
            if body == None:
                all_text = title + comments_text
            else:
                all_text = title + body + comments_text
                
            search_text_list =  []
            search_text_list = title.split(" ") 
            search_text_list = [word.lower() for word in search_text_list]            
            
            labels = issuepull.labels
            label_list = []
            for  label in labels:
                label = str(label).split("\"")[1]
                if re.match("Type", label) == None:
                    label_list.append(label.lower())
                else:
                    label_list.append(label.split(":")[1][1:].lower())

            if is_issue:
                if is_match(bug_list, label_list) or (len(label_list) == 0 and is_match(bug_words, search_text_list)):
                    writer_issue.writerow([html_url, label_list, title, all_text, issuepull.comments, created_time, updated_time, closed_time])
                    issue_num += 1
            else:
                if is_match(bug_list, label_list) or ((is_match(pull_bug_list, label_list) or len(label_list) == 0) and is_match(bug_words, search_text_list)):
                    writer_pull.writerow([html_url, label_list, title, all_text, issuepull.comments, issuepull.merged, created_time, updated_time, closed_time])
                    pull_num += 1                
                      
    print("{}: issue: {} pull: {}".format(fl, issue_num, pull_num))
    sum_issue += issue_num
    sum_pull += pull_num
    f_issue.close()
    f_pull.close()
print("Sum of Issues: {}. Pull: {}".format(sum_issue, sum_pull))
