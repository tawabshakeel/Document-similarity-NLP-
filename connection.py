from flask import Flask
from flask import render_template
from flask_restful import Resource, Api
from json import dumps
from flask.ext.jsonpify import jsonify
import main as tk
import json

from pymongo import MongoClient
client = MongoClient('localhost:27017')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/hello')
def check():
    name='4300-0.txt'
    data= tk.countingAllWords('4300-0.txt')
    abc= json.dumps(data)
    return render_template('table.html', result=data,book=name)

if __name__ == '__main__':
    app.run()
