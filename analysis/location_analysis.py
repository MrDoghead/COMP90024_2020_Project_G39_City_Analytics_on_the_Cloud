from get_data_from_db import *
import folium
from location import *
import json
import re
import pandas as pd
import numpy as np
from folium.plugins import MarkerCluster

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

# pop_df['color'] = ['red', 'blue', 'green', 'purple', 'orange',  
#          'beige', 'darkblue', 'darkgreen', 'cadetblue',  
#          'darkpurple', 'lightred', 'pink', 'darkred', 'lightgreen',  
#          'gray', 'black', 'lightgray']

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
melbourne_map.add_child(incidents).save('./compare_aurin_location.html')