'''
title: COMP90024 project
Author: Team-39
Dongnan Cao 970205
Fuyao Zhang 813023
Liqin Zhang 890054
Zhiqian Chen 1068712
Chuxin Zou
'''

from flask import Flask, render_template, redirect, url_for
import couchdb
# import flaskext.couchdb

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    COUCHDB_SERVER='http://admin:password@172.26.133.0:5984',
    COUCHDB_DATABASE='test'
)
server = couchdb.Server('http://admin:password@172.26.133.0:5984')
db = server['australia-covid-19']
number_of_tweets = len(db)


@app.route('/')
def home():
    return render_template('index.html', num=number_of_tweets)

@app.route('/emotion')
def emotion():
    return render_template('emotion_page.html', num=number_of_tweets)

@app.route('/income')
def income():
    return render_template('income_page.html', num=number_of_tweets)

@app.route('/covid')
def covid():
    return render_template('covid-19_page.html', num=number_of_tweets)

@app.route('/language')
def language():
    return render_template('language_page.html', num=number_of_tweets)

@app.route('/location')
def location():
    return render_template('location_page.html', num=number_of_tweets)

@app.route('/twitter')
def twitter():
    return render_template('twitter_page.html', num=number_of_tweets)


if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000)

