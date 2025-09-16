"""Flask application endpoints and helpers.

This module initializes the Flask app, configures language handling,
and defines routes for public pages and authenticated user pages.

Main features:
- Multi-language support via JSON dictionaries in `languages/`.
- User registration and authentication with SQLAlchemy sessions.
- Session-based user state management and logout.
- Routes for home, about, features, contacts, profile, orders, and
  settings pages.
"""

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


def load_translation(language: str):
    """
    Load a translation dictionary for the given language.

    Args:
        language (str): Language code (e.g., "en", "de", "fr").

    Returns:
        dict: Dictionary with translations loaded from JSON file.

    Notes:
        - Falls back to English (`languages/en.json`) if the file is not found.
    """
    try:
        with open(f"languages/{language}.json", encoding="utf-8") as dictfile:
            return json.load(dictfile)
    except FileNotFoundError:
        with open("languages/en.json", encoding="utf-8") as dictfile:
            return json.load(dictfile)


@app.before_request
def set_language():
    """
    Set the current language for the session.

    Behavior:
        - Reads 'lang' parameter from query string if provided.
        - Defaults to English ('en') if no language is set in session.
    """
    lang = request.args.get('lang')
    if lang:
        session['lang'] = lang
    session.setdefault('lang', 'en')


@app.context_processor
def inject_translations():
    """
    Inject translations into Jinja2 templates.

    Returns:
        dict: Contains the `l` variable with the loaded translation dictionary.
    """
    lang = session.get('lang', 'en')
    return {'l': load_translation(lang)}


@app.route("/")
def home_page():
    """
    Render the home page.

    Returns:
        Rendered homepage template, optionally with user context.
    """
    if 'user_name' in session:
        return render_template(
            "homepage.html",
            user_name=session['user_name']
        )
    else:
        return render_template("homepage.html")


@app.route("/about")
def about_page():
    """
    Render the "About" page.

    Returns:
        Rendered about template, optionally with user context.
    """
    if 'user_name' in session:
        return render_template(
            "about.html",
            user_name=session['user_name']
        )
    else:
        return render_template("about.html")


@app.route("/features")
def features_page():
    """
    Render the "Features" page.

    Returns:
        Rendered features template, optionally with user context.
    """
    if 'user_name' in session:
        return render_template(
            "features.html",
            user_name=session['user_name']
        )
    else:
        return render_template("features.html")


@app.route("/signUp", methods=["GET", "POST"])
def signUp_page():
    """
    Handle user registration.

    Workflow:
        - Display registration form.
        - On POST: validate input, register user via database functions.
        - Redirect to login page on success.

    Returns:
        Rendered signup template (with possible messages) or redirect.
    """
    form = RegistrationForm()
    message = None

    if form.validate_on_submit():
        company = form.company.data
        fullName = f'{form.firstName.data} {form.lastName.data}'
        email = form.email.data
        userType = form.userType.data
        password = form.password.data

        with SessionLocal() as db:
            message = register_user(
                db, email, fullName, company, userType, password
            )

        if message == 'Registration successful':
            return redirect(url_for('logIn_page'))

    return render_template("signUp.html", form=form, message=message)


@app.route("/logIn", methods=["GET", "POST"])
def logIn_page():
    """
    Handle user login.

    Workflow:
        - Display login form.
        - On POST: validate input, authenticate via database.
        - On success: save user info in session and redirect to profile.
        - On failure: re-render login page with error message.

    Returns:
        Rendered login template or redirect to profile.
    """
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
    """
    Render the "Contacts" page.

    Returns:
        Rendered contacts template, optionally with user context.
    """
    if 'user_name' in session:
        return render_template(
            "contacts.html",
            user_name=session['user_name']
        )
    else:
        return render_template("contacts.html")


@app.route("/profile")
def profile_page():
    """
    Display the logged-in user's profile.

    Workflow:
        - Fetch user data (name, email, company) from database.
        - Render profile template with user details.

    Returns:
        Rendered profile template.
    """
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
    """
    Display the user's orders page.

    Returns:
        Rendered orders template.
    """
    return render_template('orders.html')


@app.route("/profile/newOrder")
def new_order_page():
    pass


@app.route("/profile/settings")
def settings_page():
    """
    Display the user's settings page.

    Returns:
        Rendered settings template.
    """
    return render_template('settings.html')


@app.route("/updateProfile")
def update_profile():
    """
    Placeholder for profile update functionality.

    TODO:
        - Implement form handling for updating user profile details.
    """
    pass


@app.route('/logout')
def logout():
    """
    Log out the current user.

    Workflow:
        - Remove user-related data from session.
        - Redirect to home page.

    Returns:
        Redirect response to home page.
    """
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('home_page'))
