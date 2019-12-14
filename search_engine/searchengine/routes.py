from flask import render_template, request, Response
import json

from searchengine import app
from searchengine import model
import random

@app.route("/search", methods=["POST"])
def search():
    req = request.get_json()
    print(req)
    uid = req['uid']
    results = model.query(req['query'], 10)

    # prepare a res list
    titles = []
    abstracts = []
    ids = []

    for i in range(len(results)):
        titles.append(results[i][0])
        abstracts.append(results[i][1])
        ids.append(results[i][2])

    res = {'titles': titles, 'abstracts': abstracts, 'ids': ids}

    return Response(response=json.dumps(res),
                    status=200,
                    mimetype="application/json")

@app.route("/relevance-selection", methods=["POST"])
def rel_selection_log():
    req = request.get_json()
    id = req['id']
    uid = req['uid']
    query = req['query']
    rel = req['rel']

    print("USER {}: paper {} marked {} to query '{}'.".format(uid, id, "relevant" if rel == 1 else "irrelevant", query))
    return "Logged", 200

@app.route("/link-click", methods=["POST"])
def link_click_log():
    req = request.get_json()
    id = req['id']
    uid = req['uid']
    query = req['query']
    time = req['time']

    print("USER {}: paper {} clicked under query '{}' for {} seconds.".format(uid, id, query, time))
    return "Logged", 200

@app.route("/")
def root():
    return render_template('index.html')
