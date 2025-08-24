import json
from flask import Flask, render_template, request, session, redirect, url_for
from database.db_funcs import register_user, logIn_success, get_from_db
from database.db_funcs import SessionLocal
from model.forms import LoginForm, RegistrationForm


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)
app.secret_key = "some_secret_key"


def load_translation(language):
    try:
        with open(f"languages/{language}.json", encoding="utf-8") as dictfile:
            return json.load(dictfile)
    except FileNotFoundError:
        with open("languages/en.json", encoding="utf-8") as dictfile:
            return json.load(dictfile)


@app.before_request
def set_language():
    lang = request.args.get('lang')
    if lang:
        session['lang'] = lang
    session.setdefault('lang', 'en')


@app.context_processor
def inject_translations():
    lang = session.get('lang', 'en')
    return {'l': load_translation(lang)}


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
    if 'user_name' in session:
        return render_template(
            "about.html",
            user_name=session['user_name']
        )
    else:
        return render_template("about.html")


@app.route("/features")
def features_page():
    if 'user_name' in session:
        return render_template(
            "features.html",
            user_name=session['user_name']
        )
    else:
        return render_template("features.html")


@app.route("/signUp", methods=["GET", "POST"])
def signUp_page():
    form = RegistrationForm()
    message = None

    if form.validate_on_submit():
        company = form.company.data
        fullName = f'{form.firstName.data} {form.lastName.data}'
        email = form.email.data
        userType = form.userType.data
        password = form.password.data

        with SessionLocal() as db:
            message = register_user(db, email, fullName, company, userType, password)

        if message == 'Registration successful':
            return redirect(url_for('logIn_page'))

    return render_template("signUp.html", form=form, message=message)


@app.route("/logIn", methods=["GET", "POST"])
def logIn_page():
    if 'user_id' in session:
        return redirect(url_for('profile_page'))

    form = LoginForm()
    if form.validate_on_submit():
        login = form.email.data
        password = form.password.data

        with SessionLocal() as db:
            user_id, user_name = logIn_success(db, login, password)
        if user_id:
            session['user_id'] = user_id
            session['user_name'] = user_name
            return redirect(url_for('profile_page'))
        else:
            return render_template(
                'logIn.html',
                form=form,
                message='Wrong email or password'
            )
    return render_template('logIn.html', form=form)


@app.route("/contacts")
def contacts_page():
    if 'user_name' in session:
        return render_template(
            "contacts.html",
            user_name=session['user_name']
        )
    else:
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


@app.route("updateProfile")
def update_profile():
    


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('home_page'))
