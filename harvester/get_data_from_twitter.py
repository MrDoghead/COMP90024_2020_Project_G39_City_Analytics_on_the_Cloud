import json
from TwitterAPI import TwitterAPI,TwitterPager
import tweepy
import couchdb
import sys
import time

class Twitter:
    def __init__(self):
        self.data_frame = {
                'tweet_id': None,
                'created_at': None,
                'text': None,
                'hashtags': None,
                'lang': None,
                'coordinates': None,
                'place': {
                    'country': None,
                    'full_name': None,
                    'type': None},
                'user': {
                    'user_id': None,
                    'location': None},
                'retweeted_status': {
                    'created_at': None,
                    'tweet_id': None,
                    'text': None,
                    'hashtags': None},
                 'quoted_status': {
                     'created_at': None,
                    'tweet_id': None,
                    'text': None,
                    'hashtags:': None}
                 }
    def extract_data(self,item):
        self.data_frame['tweet_id'] = item['id']
        self.data_frame['created_at'] = item['created_at']
        if 'extended_tweet' not in item.keys():
            self.data_frame['text'] = item['text']
        else:
            self.data_frame['text'] = item['extended_tweet']['full_text']
        if item['entities']:
            self.data_frame['hashtags'] = item['entities']['hashtags']
        self.data_frame['lang'] = item['lang']
        if item['coordinates']:
            self.data_frame['coordinates'] = item['coordinates']['coordinates']
        if item['place']:
            self.data_frame['place']['country'] = item['place']['country']
            self.data_frame['place']['full_name'] = item['place']['full_name']
            self.data_frame['place']['type'] = item['place']['place_type']
        self.data_frame['user']['user_id'] = item['user']['id_str']
        self.data_frame['user']['location'] = item['user']['location']
        if 'retweeted_status' in item.keys():
            self.data_frame['retweeted_status']['created_at'] = item['retweeted_status']['created_at']
            self.data_frame['retweeted_status']['tweet_id'] = item['retweeted_status']['id']
            self.data_frame['retweeted_status']['text'] = item['retweeted_status']['text']
            self.data_frame['retweeted_status']['hashtags'] = item['retweeted_status']['entities']['hashtags']
        if 'quoted_status' in item.keys():
            self.data_frame['quoted_status']['created_at'] = item['quoted_status']['created_at']
            self.data_frame['quoted_status']['tweet_id'] = item['quoted_status']['id']
            self.data_frame['quoted_status']['text'] = item['quoted_status']['text']
            self.data_frame['quoted_status']['hashtags'] = item['quoted_status']['entities']['hashtags']

        return self.data_frame

class harvester:
    def __init__(self,keys,server,db_name,topic,location):
        self.consumer_key = keys[0]
        self.consumer_secret = keys[1]
        self.access_token_key = keys[2]
        self.access_token_secret = keys[3]
        self.server = server
        self.db_name = db_name
        self.db = self.__connect_db()
        self.topic = topic
        self.location = location

    def __connect_db(self):
        SERVER = self.server
        couch = couchdb.Server(SERVER)
        DBNAME = self.db_name
        print('connecting couchdb',DBNAME,'...')
        try:
            db = couch[DBNAME]
        except:
            db = couch.create(DBNAME)
        return db

    def stream(self):
        api = TwitterAPI(self.consumer_key,self.consumer_secret,self.access_token_key,self.access_token_secret)
        r = api.request('statuses/filter',{'track':self.topic, 'locations':self.location})
        # deal with data duplication
        data_buffer = []
        tid_set = set()
        count = 0
        print('start downloading...')
        for item in r.get_iterator():
            if 'text' not in item:
                continue
            tweet = Twitter()
            data = tweet.extract_data(item)
            tid = data['tweet_id']
            tid_set.add(tid)
            data_buffer.append(data)
            count += 1
            if count % 100 == 0:
                print(count,'...')
            if count % 10000 == 0:
                self.save_data(data_buffer,tid_set)
                print(count,'saved')
                time.sleep(5*60)

    def save_data(self,data_buffer,tid_set):
        for data in data_buffer:
            tid = data['tweet_id']
            if tid in tid_set:
                try:
                    self.db.save(data)
                    tid_set.remove(tid)
                except Exception as e:
                    print('error:',e)
                    continue

    def search(self):
        auth = tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)
        auth.set_access_token(self.access_token,self.access_token_secret)
        api = tweepy.API(auth)
        geocode = ','.join([str(self.location[0]),str(self.location[1]),"1000000km"])
        search_results = api.search(q=self.topic,geocode="1000000km",count=1500)
        data_buffer = []
        tid_set = set()
        count = 0
        for item in search_results:
            if 'text' not in item:
                 continue
            tweet = Twitter()
            data = tweet.extract_data(item)
            tid = data['tweet_id']
            tid_set.add(tid)
            data_buffer.append(data)
            if count % 100 == 0:
                print(count,'...')
            if count % 10000 == 0:
                self.save_data(data_buffer,tid_set)
                print(count,'saved')
                time.sleep(15*60)
            count += 1

if __name__ == '__main__':

    consumer_key = 'O7VdcNQferxQglccX8Vj5i69y'
    consumer_secret = 'YuV982BJyMBi8zMWYzgsKJ21CmFnsDgXJp4k65IHoSW7jF9ocS'
    access_token_key = '1251724444373942272-fgchtfjfNz8ZJQy1Qbsuuyg8bPWNwg'
    access_token_secret = 'y9VOQUvurz3lC4tkA8xwI92nWDw2H1YMBC050vZEo5l6I'
    keys = [consumer_key,consumer_secret,access_token_key,access_token_secret]
    #proxy_url = '192.168.10.101'
    topic = 'income' #'COVID-19'
    location_name = 'Australia'
    locations = {'Australia':[112.9211,-54.6403,159.2787,-9.2288]}
    location = locations['Australia']

    print('start task...')
    #task = harvester(keys=keys,server='http://admin:password@172.26.133.0:5984/',db_name='income',topic=topic,location=location)
    #task.stream()

    # run continously
    while True:
        try:
            #task = harvest(keys=keys,server='http://admin:password@172.26.133.0:5984/',db_name='australia-covid-19',topic=topic,location=location)
            task = harvester(keys=keys,server='http://admin:password@172.26.133.0:5984/',db_name='income',topic=topic,location=location)
            task.stream()
        except Exception as e:
            print(e)
            print('restart task...')
            continue









