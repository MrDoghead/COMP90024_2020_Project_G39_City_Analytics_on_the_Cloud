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
    return render_template('emotion_chart.html')

@app.route('/distribution')
def distribution():
    return render_template('distribution_chart.html')

@app.route('/language')
def language():
    return render_template('language_chart.html')


if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000)

