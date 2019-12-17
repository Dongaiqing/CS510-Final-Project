from flask import render_template, request, Response
import json

from searchengine import app
from searchengine import model
from searchengine import db_controller
import random

@app.route("/search", methods=["POST"])
def search():
    req = request.get_json()
    print(req)
    uname = req['uname']
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
    pid = req['pid']
    uname = req['uname']
    query = req['query']
    rel = req['rel']

    print("==== [REL SEL EVENT] ====\n  [USER] - {}\n  [QUERY] - {}\n  [PAPER] - {}\n  [REL] - {}".format(uname, query, pid, rel))
    return "Logged", 200

@app.route("/link-click", methods=["POST"])
def link_click_log():
    req = request.get_json()
    pid = req['pid']
    uname = req['uname']
    query = req['query']
    duration = req['duration']

    uid = db_controller.get_user_id(uname)
    db_controller.record_user_click(uid, pid, query, duration)
    print("==== [CLICK EVENT] ====\n  [USER] - {}\n  [QUERY] - {}\n  [PAPER] - {}\n  [DURATION] - {}s".format(uname, query, pid, duration))
    return "Logged", 200

@app.route("/login", methods=["POST"])
def log_in():
    req = request.get_json()
    uname = req['uname']
    db_controller.add_user(uname)
    print("==== [LOG IN EVENT] ====\n  [USER] - {}".format(uname))
    return "Logged in", 200

@app.route("/")
def root():
    return render_template('index.html')
