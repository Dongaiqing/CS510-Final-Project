from flask import render_template, request, Response
import json

from searchengine import app
from searchengine import model

import pprint

@app.route("/search", methods=["POST"])
def search():
    req = request.get_json()
    results = model.query(req['query'], 10)
    res = list({'id': 'n/a', 'authors': 'n/a', 'link': 'n/a', 'title': result[0], 'abstract': result[1]} for result in results)
    #prepare a res list
    titles = []
    abstracts = []
    ids = []
    for i in range(len(results)):
        titles.append(res[i]['title'])
        abstracts.append(res[i]['abstract'])
        ids.append(res[i]['id'])
    resultData = {'titles': titles, 'abstracts': abstracts, 'ids': ids}
    return Response(response=json.dumps(resultData),
                    status=200,
                    mimetype="application/json")

@app.route("/relevance-selection", methods=["POST"])
def rel_selection_log():
    req = request.get_json()
    id = req['id']
    query = req['query']
    rel = req['rel']

    print("RELEVANCE SELECTION EVENT: paper {} marked {} to query '{}'.".format(id, "relevant" if rel == 1 else "irrelevant", query))
    return "Logged", 200

@app.route("/link-click", methods=["POST"])
def link_click_log():
    req = request.get_json()
    id = req['id']
    query = req['query']

    print("LINK CLICK EVENT: paper {} clicked under query '{}'.".format(id, query))
    return "Logged", 200

@app.route("/")
def root():
    return render_template('index.html')
