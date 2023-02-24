from flask import Flask, render_template

app = Flask(__name__)

isLoggedIn = False

@app.route('/')
def index():
    return render_template("index.html", isLoggedIn=isLoggedIn)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/flashcard')
def flashcard():
    return render_template("flashcard.html")