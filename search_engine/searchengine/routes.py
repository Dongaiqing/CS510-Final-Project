from flask import render_template, request, Response
import json

from searchengine import app
from searchengine import model
import random

## for fake demo ##
usrs = {}
###################

@app.route("/search", methods=["POST"])
def search():
    global usrs

    req = request.get_json()
    print(req)
    uid = req['uid']
    
    ## for fake demo ##
    if uid.lower() in usrs and len(usrs[uid.lower()]) != 0:
        results = model.query(req['query'], 20)
    else:
    ###################
        results = model.query(req['query'], 10)

    # prepare a res list
    titles = []
    abstracts = []
    ids = []

    ## for fake demo ##
    previous_selections = []
    ###################

    for i in range(len(results)):
        ## for fake demo ##
        if uid.lower() in usrs:
            if results[i][2] in usrs[uid.lower()]:
                previous_selections.append(results[i])
                continue
            elif len(usrs[uid.lower()]) != 0 and i < 10:
                continue
        ###################
        titles.append(results[i][0])
        abstracts.append(results[i][1])
        ids.append(results[i][2])

    print(previous_selections)

    ## for fake demo ##
    res = {}
    if uid.lower() in usrs:
        random.shuffle(previous_selections)
        for sel in previous_selections:
            titles.insert(0, sel[0])
            abstracts.insert(0, sel[1])
            ids.insert(0, sel[2])

        res = {'titles': titles, 'abstracts': abstracts, 'ids': ids}
    else:
    ###################
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
    global usrs
    req = request.get_json()
    id = req['id']
    uid = req['uid']
    query = req['query']
    time = req['time']
    
    ## for fake demo ##
    if uid.lower() in usrs:
        usrs[uid.lower()].add(id)
    else:
        usrs[uid.lower()] = set()
        usrs[uid.lower()].add(id)
    ###################

    print("USER {}: paper {} clicked under query '{}' for {} seconds.".format(uid, id, query, time))
    return "Logged", 200

@app.route("/")
def root():
    return render_template('index.html')
