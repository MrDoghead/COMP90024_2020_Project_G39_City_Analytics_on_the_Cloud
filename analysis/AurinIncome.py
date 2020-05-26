import statistics, math, numpy
from statistics import *
import folium
import schedule
import time

def aurin_income():
    aurinIncome=[{'tolIncome': 57267.0, 'loc': [-37.840935,144.946457]}, {'tolIncome': 52271.0, 'loc': [-28.016666,153.399994]}, {'tolIncome': 48862.0, 'loc': [-41.429825,147.157135]}, {'tolIncome': 79243.0, 'loc': [-31.953512,115.857048]}, {'tolIncome': 58859.0, 'loc': [-32.916668,151.750000]}, {'tolIncome': 59856.0, 'loc': [-34.425072,150.893143]}, {'tolIncome': 69779.0, 'loc': [-31.745001,115.766113]}, {'tolIncome': 55388.0, 'loc': [-23.6975,133.8836]}, {'tolIncome': 59063.0, 'loc': [-34.730194,135.850479]}, {'tolIncome': 46251.0, 'loc': [-34.921230,138.599503]}, {'tolIncome': 45659.0, 'loc': [-41.180557,146.346390]}, {'tolIncome': 50975.0, 'loc': [-37.549999,143.850006]}, {'tolIncome': 64687.0, 'loc': [-27.470125,153.021072]}, {'tolIncome': 68007.0, 'loc': [-33.865143,151.209900]}, {'tolIncome': 71283.0, 'loc': [-35.282001,149.128998]}, {'tolIncome': 66129.0, 'loc': [-32.528889,115.723053]}, {'tolIncome': 58276.0, 'loc': [-42.880554,147.324997]}]
    income=[57267.0, 52271.0, 48862.0, 79243.0, 58859.0, 59856.0, 69779.0, 55388.0, 59063.0, 46251.0, 45659.0, 50975.0, 64687.0, 68007.0, 71283.0, 66129.0, 58276.0]
    #mean=statistics.mean(income)
    q=numpy.quantile(income, 0.25, axis = None) 
#print(q)



    m3 = folium.Map([-27, 135], zoom_start=4)

    for data in aurinIncome:
        loc=data["loc"]
        inc=data["tolIncome"]
        if inc<q:
            folium.Marker(location=loc, popup='poor',icon=folium.Icon(color="red"),).add_to(m3)
        if inc>=q:
            folium.Marker(location=loc, popup='rich',icon=folium.Icon(color="green"),).add_to(m3)

    
    m3
    m3.save("/home/ubuntu/project/flask/static/AURIN_INCOME.html")
    #aurin_map(aurinIncome).save('/home/ubuntu/project/flask/static/AURIN_INCOME.html')


schedule.every().day.at("00:00").do(aurin_income)
while True:
    schedule.run_pending()
    time.sleep(1)