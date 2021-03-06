'''
Title: COMP90024 project
Author: Team-39
Dongnan Cao 970205
Fuyao Zhang 813023
Liqin Zhang 890054
Zhiqian Chen 1068712
Chuxin Zou  1061714
'''
import couchdb
from get_data_from_db import *

def update_task1():
    task = Task1(server='http://admin:password@172.26.133.0:5984/', db_name='australia-covid-19')
    print('task:',task.task_name)
    rows = get_rows(task)
    counts = {}
    for row in rows:
        lang = row.key
        counts[lang] = counts.get(lang,0) + 1
    results = sorted(counts.items(),key=lambda x:x[1],reverse=True)
    task.update_results(results)


if __name__ == '__main__':
    update_task1()
