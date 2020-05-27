'''
Title: COMP90024 project
Author: Team-39
D:ongnan Cao 970205
Fuyao Zhang 813023
Liqin Zhang 890054
Zhiqian Chen 1068712
Chuxin Zou  1061714
'''

from get_data_from_db import Task1
from iso639 import languages
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts
import json
import pandas as pd
import re
import numpy as np
# import schedule
# import time


task = Task1(server='http://admin:password@172.26.133.0:5984', db_name='australia-covid-19')
result = task.get_results(20)
lang_ls = []
lang_cnt = []
for i in result[:min(20,len(result))]:
    if i[0]=='in':
        lang_ls.append(languages.get(alpha2='id').name)
    elif i[0]=='und':
        continue
    else:
        lang_ls.append(languages.get(alpha2=i[0]).name)
    lang_cnt.append(i[1])

lang_df = pd.DataFrame(columns=['language','count'])
lang_df['language'] = lang_ls
lang_df['count'] = lang_cnt

# draw 
(
    Pie()
    .add(
        series_name="Language",
        data_pair=[list(z) for z in zip(list(lang_ls), list(lang_cnt))],
        radius=["30%", "70%"],
        label_opts=opts.LabelOpts(is_show=False, position="center")
    )
    .set_global_opts(legend_opts=opts.LegendOpts(pos_left="left", orient="vertical"))
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        label_opts=opts.LabelOpts(formatter="{b}: {c}")
    )
    .render("/home/ubuntu/project/flask/static/tweet_language_doughnut_chart.html")
)


# compare with aurin
with open('/home/ubuntu/project/aurin/AURIN-lang.json') as f:
    aurin = json.load(f)
f.close()

tot_ls = []
for key in aurin['features'][0]['properties'].keys():
    if key.endswith('all_eng_profic'):
        tot_ls.append(key)
    elif key.endswith('eng_only'):
        tot_ls.append(key)

aurin_lang_df = pd.DataFrame(columns=['language','count'])
aurin_lang_df['language'] = ['Indonesian','Japanese','French','Italian','English','German','Dutch','Turkish','Spanish','Thai','Korean']
aurin_lang_df['count'] = [0,0,0,0,0,0,0,0,0,0,0]


pattern = ['indo','japan','french','italian','eng_only','german','dutch','turkish','spanish','thai','korean']
for data in aurin['features']:
    for key in tot_ls:
        for i in range(0, len(pattern)):
            if re.search(pattern[i],key):
                aurin_lang_df.iloc[i,1] = aurin_lang_df.iloc[i,1] + data['properties'][key]

lang_common = [x for x in aurin_lang_df['language'] if x in lang_ls]
tweet_common_cnt,aurin_common_cnt = [],[]
for l in lang_common:
    tweet_common_cnt.append(lang_df['count'].values[np.where(lang_df['language']==l)[0]][0])
    aurin_common_cnt.append(aurin_lang_df['count'].values[np.where(aurin_lang_df['language']==l)[0]][0])

# draw
bar = (
    Bar()
    .add_xaxis(lang_common)
    .add_yaxis("Tweets", [round(x,2) for x in tweet_common_cnt/lang_df['count'].sum()*100])
    .add_yaxis("Aurin", [round(x,2) for x in aurin_common_cnt/aurin_lang_df['count'].sum()*100])
    .set_global_opts(title_opts=opts.TitleOpts(title="Compare of Language Use Percentage"))
)
bar.render('/home/ubuntu/project/flask/static/compare_language_bar_chart.html')
