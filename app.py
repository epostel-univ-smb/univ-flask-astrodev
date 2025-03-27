from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def start():
    return render_template('startpage.html')

@app.route("/astronomy")
def astronomy():
    return render_template('astronomy.html')