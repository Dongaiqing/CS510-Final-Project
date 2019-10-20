from flask import render_template, request, Response
import json

from searchengine import app
from searchengine import model

import pprint

@app.route("/search", methods=["POST"])
def search():
    req = request.get_json()
    results = model.query(req['query'], 10)
    res = list({'title': result[0], 'abstract': result[1]} for result in results)
    
    return Response(response=json.dumps(res), status=200, mimetype="application/json")

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/result")
def rank():
    return render_template('result.html')