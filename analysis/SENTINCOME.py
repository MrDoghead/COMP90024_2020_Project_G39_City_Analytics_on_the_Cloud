import sys
import json
import couchdb
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
import folium
from folium.plugins import MarkerCluster
import schedule
import time

def analysis_COVID():
    class Task3:
        def __init__(self,server,db_name):
            self.server = couchdb.Server(server)
            self.db_name = db_name
            self.db = self.server[self.db_name]
            self.task_name = 'tweet_location'
            self.map = "function(doc){if (doc.text && doc.coordinates){emit(doc.text,doc.coordinates);}}"

        def get_results(self,rows):
            results = []
            for row in rows:
                tweet = row.key.strip()
                tweet = tweet.replace('\n',' ').replace('\r',' ')
                tweet = tweet.replace('\t',' ')
                location = row.value
                results.append([tweet,location])
            return results

    def get_rows(task):
        design_name = '-'.join([task.db_name,task.task_name])
        view_id = '/'.join(['_design',design_name])
        print('view_id',view_id)
        view_name = task.task_name
        index = '/'.join([design_name,view_name])
        try:
            view_text = create_view_text(view_id,view_name,map_fn=task.map)
            print(view_text)
            task.db.save(view_text)
            print('created new view',index)
        except:
            pass
        print('loading rows from view',index)
    #rows = task.db.view(index,skip=0,limit=10000)
        rows = task.db.view(index)
        return rows


    def create_view_text(view_id,view_name,map_fn):
        view_text = {
            '_id': view_id,
            'views': {
                view_name: {
                    'map': map_fn
                }
            }
        }
        return view_text


    if __name__ == '__main__':
       
        task = Task3(server='http://admin:password@172.26.133.0:5984/', db_name='income')
        print('task:',task.task_name)
        rows = get_rows(task)
        results = task.get_results(rows)
        N = -1
        data=[]
        for res in results[:N]:
            tweet=[]
            loc=[]
            text = str(res[0])
            tweet.append(text)
            location = res[1]
            lo = location[1]
            loc.append(lo)
            la = location[0]
            loc.append(la)
            tweet.append(loc)
            data.append(tweet)
    #print(data)


    def sentiment_analysis(each):
        pos_count=0
        neg_count=0
        nt_count=0
        sen_list=[]
        for t in each:
    #print(text)
            ss = sid.polarity_scores(str(t[0]))
    #print(ss)
            score=ss["compound"]
            if score>=0.05:
                t.append("P")
                pos_count+=1
            elif score<=-0.05:
                t.append("N")
                neg_count+=1
            else:
                t.append("NT")
                nt_count+=1
            sen_list.append(t)
        return sen_list

    result1=sentiment_analysis(data)
    #print(result1)



    def is_au(loc):
        au_loc = [112.9211,-54.6403,159.2787,-9.2288]
        lo = loc[1]
        la = loc[0]
        if au_loc[0] < lo < au_loc[2] and au_loc[1] < la < au_loc[3]:
            return True
        else:
            return False
    



    m = folium.Map(location=[-27, 135], zoom_start=4)

    marker_cluster = MarkerCluster().add_to(m)
    #folium.Marker(location=[-37.8136, 144.9631], popup='Add popup text here.',icon=folium.Icon(color="green"),).add_to(marker_cluster)

    for tweet in result1:
        if type(tweet[1])==list:
            loc=tweet[1]
            check=is_au(loc)
            if check is True:
                if tweet[2]=="P":
                    folium.Marker(location=loc, popup='Positive',icon=folium.Icon(color="green"),).add_to(marker_cluster)
                if tweet[2]=="N":
                    folium.Marker(location=loc, popup='Negative',icon=folium.Icon(color="red"),).add_to(marker_cluster)
                if tweet[2]=="NT":
                    folium.Marker(location=loc, popup='Neutral',icon=folium.Icon(color="blue"),).add_to(marker_cluster)
        else:
            continue
    m.save('/home/ubuntu/project/flask/static/SentMap_INCOME.html')
    
schedule.every().day.at("00:00").do(analysis_COVID)
while True:
    schedule.run_pending()
    time.sleep(1)
#m.save('/home/ubuntu/project/flask/static/SentMap_INCOME.html')