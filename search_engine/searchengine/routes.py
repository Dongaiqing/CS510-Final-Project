from flask import render_template
from searchengine import app

@app.route("/")
def search():
    return render_template('home.html')

@app.route("/result")
def rank():
    return render_template('result.html')