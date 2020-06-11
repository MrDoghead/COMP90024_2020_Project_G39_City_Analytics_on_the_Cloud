'''
Title: COMP90024 project
Author: Team-39
Dongnan Cao 970205
Fuyao Zhang 813023
Liqin Zhang 890054
Zhiqian Chen 1068712
Chuxin Zou  1061714
'''

from get_data_from_twitter import *
import time

def task():
    consumer_key = ''
    consumer_secret = ''
    access_token_key = ''
    access_token_secret = ''
    keys = [consumer_key,consumer_secret,access_token_key,access_token_secret]
    #proxy_url = '192.168.10.101'
    topic = 'income' #'COVID-19'
    location_name = 'Australia'
    locations = {'Australia':[112.9211,-54.6403,159.2787,-9.2288]}
    location = locations['Australia']

    print('Task:',topic)
    print('start task...')
    #task = harvester(keys=keys,server='http://admin:password@172.26.133.0:5984/',db_name='income',topic=topic,location=location)
    #task.stream()

    # run continously
    while True:
        try:
            task = harvester(keys=keys,server='http://admin:password@172.26.133.0:5984/',db_name='income',topic=topic,location=location)
            task.stream()
        except Exception as e:
            print(e)
            print('restart task...')
            time.sleep(10)
            continue

if __name__ == '__main__':
    task()

