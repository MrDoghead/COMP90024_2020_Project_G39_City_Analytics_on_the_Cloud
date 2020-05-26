import sys
import json
import couchdb

class Task1:
    def __init__(self,server,db_name):
        self.server = couchdb.Server(server)
        self.db_name = db_name
        self.db = self.server[self.db_name]
        self.task_name = 'languages'
        self.map = "function(doc){if (doc.lang){emit(doc.lang,1);}}"
        self.reduce = None
        self.res_db_name = '-'.join(['results',self.task_name])

    def save_results(self,results):
        try:
            res_db = self.server.create(self.res_db_name)
            print('created new db',self.res_db_name)
        except:
            print(self.res_db_name,'already exits')
        doc = {}
        for res in results:
            lang,count = res
            doc[lang] = count
        try:
            _id,_rev = res_db.save(doc)
            print('_id:',_id,'_rev',_rev,'saved')
        except Exception as e:
            print('saving fails', e)

    def update_results(self,results):
        if self.res_db_name not in self.server:
            print('no results saved yet')
            sys.exit()
        res_db = self.server[self.res_db_name]
        ids = []
        for _id in res_db:
            ids.append(_id)
        uid = ids[0]
        data = res_db[uid]
        for res in results:
            lang,count = res
            data[lang] = count
        try:
            _id,_rev = res_db.save(data)
            print('_id:',_id,'_rev',_rev,'updated')
        except Exception as e:
            print('saving fails', e)

    def get_results(self,N):
        if self.res_db_name not in self.server:
            print('no results saved yet')
            sys.exit()
        res_db = self.server[self.res_db_name]
        ids = []
        for _id in res_db:
            ids.append(_id)
        uid = ids[0]
        data = res_db[uid]
        results = []
        for k in data:
            pair = (k,data[k])
            results.append(pair)
        return results[2:2+N]


class Task2:
    def __init__(self,server,db_name):
        self.server = couchdb.Server(server)
        self.db_name = db_name
        self.db = self.server[self.db_name]
        self.task_name = 'locations'
        self.map = "function(doc){if (doc.coordinates){emit(doc.coordinates[0],doc.coordinates[1]);}}"

    def get_results(self,rows):
        results = []
        for row in rows:
            lo = row.key
            la = row.value
            pair = [lo,la]
            results.append(pair)
        return results

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
    # sample1:  get lang data ({lang:count}) from covid db
    '''
    task = Task1(server='http://admin:password@172.26.133.0:5984/', db_name='australia-covid-19')
    print('task:',task.task_name)
    rows = get_rows(task)
    counts = {}
    for row in rows:
        lang = row.key
        counts[lang] = counts.get(lang,0) + 1
    results = sorted(counts.items(),key=lambda x:x[1],reverse=True)
    #task.save_results(results)
    task.update_results(results)
    new_res = task.get_results(10)
    for each in new_res:
        print(each)
    '''
    # sample2:  get covid data (lo+la) from covid db
    '''
    task = Task2(server='http://admin:password@172.26.133.0:5984/', db_name='australia-covid-19')
    print('task:',task.task_name)
    rows = get_rows(task)
    results = task.get_results(rows)
    N = 20
    for res in results[:N]:
        lo,la = res
        print(lo,la)
    '''

    # sample3: get income data (tweet+location) from income db
    '''    
    task = Task3(server='http://admin:password@172.26.133.0:5984/', db_name='income')
    print('task:',task.task_name)
    rows = get_rows(task)
    results = task.get_results(rows)
    N = -1
    for res in results[:N]:
        tweet = res[0]
        location = res[1]
        lo = location[0]
        la = location[1]
        output = '\t'.join([tweet,str(lo),str(la)])
        print(output)
    '''

