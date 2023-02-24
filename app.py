from flask import Flask, render_template, request

app = Flask(__name__)

isLoggedIn = False

@app.route('/', methods=["GET", "POST"])
def index():
    email = request.form.get("email")
    return render_template("index.html", isLoggedIn=isLoggedIn, email=email)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signupResponse', methods=["POST"])
def signupResponse():
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    email = request.form.get("email")
    password = request.form.get("password")

    return render_template("signupResponse.html", firstName=firstName, lastName=lastName, email=email, password=password), {"Refresh": "2; url=/login"}

@app.route('/flashcard')
def flashcard():
    return render_template("flashcard.html")