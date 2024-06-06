from flask import Flask, jsonify,render_template
from pymongo import MongoClient
import subprocess

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')

@app.route('/main')
def mainpage():
    return "main page"

@app.route('/run_script')
def run_script():
    subprocess.run(['python', 'script.py'])
    lists = []
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client['Trending_Tweets']
    collection = db['dataitem']

    for x in collection.find():
        lists.append(x)

    latest_record = lists
  
    return jsonify(latest_record)



if __name__ == '__main__':
    app.run(debug=True)