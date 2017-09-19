"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import jsonify
from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Rating, Movie, connect_to_db, db


from model import connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/register", methods=["GET"])
def register_process():
    """what happens after it queries database"""

    return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def register_form():
    """Register user"""

    email = request.form.get('email')
    password = request.form.get('password')

    #here we do a db.seession query and bind it to user_email
    user = db.session.query(User).filter(User.email == email).first()
    if user is None:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
    else:
        print "Already in database"
        return redirect("/log-in")

    return redirect("/log-in")


@app.route("/log-in", methods=["GET"])
def login_process():
    """User login"""

    return render_template("login.html")


@app.route("/log-in", methods=["POST"])
def log_in():
    """Log in user"""

    session['email'] = request.form.get('email')
    session['password'] = request.form.get('password')

    user = db.session.query(User).filter(User.email == session['email'],
                                         User.password == session['password']).first()

    if user is None:
        return redirect("/register")
    else:
        return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')
