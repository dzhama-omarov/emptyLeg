from flask import Flask, render_template, request, session, redirect, url_for
from database.db_funcs import register_user, logIn_success, get_from_db
from database.db_funcs import SessionLocal


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)
app.secret_key = "some_secret_key"


@app.route("/")
def home_page():
    if 'user_name' in session:
        return render_template(
            "homepage.html",
            user_name=session['user_name']
        )
    else:
        return render_template("homepage.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/features")
def features_page():
    return render_template("features.html")


@app.route("/signUp", methods=["GET", "POST"])
def signUp_page():
    message = None
    if request.method == "POST":
        company = request.form["company"]
        fullName = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        with SessionLocal() as db:
            message = register_user(db, email, fullName, company, password)
    return render_template("signUp.html", message=message)


@app.route("/logIn", methods=["GET", "POST"])
def logIn_page():
    if request.method == "GET":
        if 'user_id' in session:
            return redirect(url_for('profile_page'))
        return render_template('logIn.html')

    login = request.form["email"]
    password = request.form["password"]
    with SessionLocal() as db:
        user_id, user_name = logIn_success(db, login, password)
    if user_id:
        session['user_id'] = user_id
        session['user_name'] = user_name
        return redirect(url_for('profile_page'))
    else:
        return render_template('logIn.html', message='Wrong email or password')


@app.route("/contacts")
def contacts_page():
    return render_template("contacts.html")


@app.route("/profile")
def profile_page():
    with SessionLocal() as db:
        name, email, company = get_from_db(
            db, session['user_id'], 'fullName', 'email', 'company'
        )
    return render_template(
        'profile.html',
        user_name=name,
        user_email=email,
        user_company=company
    )


@app.route("/profile/orders")
def orders_page():
    return render_template('orders.html')


@app.route("/profile/settings")
def settings_page():
    return render_template('settings.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home_page'))
