from flask import Flask, render_template


app = Flask(__name__, template_folder="../templates")


@app.route("/")
def home_page():
    return render_template("homepage.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/features")
def features_page():
    return render_template("features.html")


@app.route("/signUp")
def signUp_page():
    return render_template("signUp.html")


@app.route("/logIn")
def logIn_page():
    return render_template("logIn.html")


@app.route("/contacts")
def contacts_page():
    return render_template("contacts.html")
