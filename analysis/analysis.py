# Team: 39
# Chuxin Zou 1061714
# Dongnan Cao 970205
# Fuyao Zhang 813023
# Liqin Zhang 890054
# Zhiqian Chen 1068712

# Author: Chuxin Zou (1061714)

from get_data_from_db import *
import folium
from location import *
from iso639 import languages
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts
import json
import pandas as pd
import re
import numpy as np
import schedule
import time

def analysis_lang():
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



def analysis_location():
    task = Task2(server='http://admin:password@172.26.133.0:5984/', db_name='australia-covid-19')
    rows = get_rows(task)
    results = task.get_results(rows)

    latitude_ls,longitude_ls = [],[]

    for coordinate in results:
        latitude_ls.append(coordinate[1])
        longitude_ls.append(coordinate[0])

    melbourne_map = folium.Map([-28.043995, 136.264296], zoom_start=5)

# # Instantiate a feature group for the incidents in the dataframe
    incidents = folium.map.FeatureGroup()
    cities = Cities()
# Loop through the 200 crimes and add each to the incidents feature group
    for lat, lng, in zip(latitude_ls, longitude_ls):
        if cities.is_au([lng, lat]):
            incidents.add_child(
                folium.CircleMarker(
                    [lat, lng],
                    radius=7, # define how big you want the circle markers to be
                    color='yellow',
                    fill=True,
                    fill_color='red',
                    fill_opacity=0.5
                )
            )

# melbourne_map.add_child(incidents).save('./location.html')

    with open('/Users/apple/Desktop/AURIN-population.json') as f:
        aurin = json.load(f)
    f.close()

    code_ls,tot_ls = [],[]
    for i in aurin['features']:
        code_ls.append(i['properties']['lga_code18'])
        tot_ls.append(i['properties']['est_res_pop_ur_erp_30_jun_p_tot_num'])

    pop_df = pd.DataFrame(columns=['code','tot','la','lo','city'])
    pop_df['code'] = code_ls
    pop_df['tot'] = tot_ls

    ls = ['24600','64010','62810','61610','89399','57080','55110','54170','20570','70200','17200','18450','15900','40070','46300','31000']
    index = []
    for i in range(0,pop_df.shape[0]):
        if pop_df['code'].values[i] not in ls:
            index.append(i)
    pop_df = pop_df.drop(index,axis=0).reset_index().drop(['index'],axis=1)

    for i in range(0,pop_df.shape[0]):
        pop_df.iloc[i,2]= cities.lga2loc(code=pop_df['code'].values[i])[1]
        pop_df.iloc[i,3] = cities.lga2loc(code=pop_df['code'].values[i])[0]
        pop_df.iloc[i,4] = cities.lga2city(code=pop_df['code'].values[i])
        if pop_df['code'].values[i]=='24600':
            pop_df['tot'].values[i] = pop_df['tot'].values[i] + pop_df['tot'].values[np.where(pop_df['code'].values=='20570')[0]]
        if pop_df['code'].values[i]=='17200':
            pop_df['tot'].values[i] = pop_df['tot'].values[i] + pop_df['tot'].values[np.where(pop_df['code'].values=='18450')[0]] + pop_df['tot'].values[np.where(pop_df['code'].values=='15900')[0]] + pop_df['tot'].values[np.where(pop_df['code'].values=='89399')[0]]
        if pop_df['code'].values[i]=='57080':
            pop_df['tot'].values[i] = pop_df['tot'].values[i] + pop_df['tot'].values[np.where(pop_df['code'].values=='55110')[0]] + pop_df['tot'].values[np.where(pop_df['code'].values=='54170')[0]] + pop_df['tot'].values[np.where(pop_df['code'].values=='57080')[0]]

    pop_df = pop_df.drop([3,4,5,10,14],axis=0)

    for index, row in pop_df.iterrows():
        folium.Circle(
            location=[row['la'], row['lo']],
        #   popup= 'Location:' +row['city'],
            tooltip=row['city'],
            radius=row['tot']/2,
            color='lightgreen',
            fill=True,
            fill_color='green',
            fill_opacity=0.5,
        ).add_to(melbourne_map)
    melbourne_map.add_child(incidents).save('/home/ubuntu/project/flask/static/compare_aurin_location.html')    

schedule.every().day.at('00:00').do(analysis_lang)
schedule.every().day.at('00:00').do(analysis_location)

while True:
    schedule.run_pending()
    time.sleep(1)