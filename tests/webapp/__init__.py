"""

"""
from contextlib import closing
from functools import wraps
import sqlite3
from flask import Flask, Blueprint, request, session, redirect, render_template, flash, make_response, url_for, abort, jsonify
import hashlib

bp = Blueprint("test", __name__)

view_vars = {
    "project_name":"Holmium test suite",
}

class DB:
    def __init__(self):
        self._db = None
    def init_app(self, app):
        self.app = app

    @property
    def db(self):
        if not self._db:
            self._db = sqlite3.connect(self.app.config['DATABASE'], check_same_thread=False)
        return self._db

    def create_db(self):
        with self.app.open_resource('schema.sql', mode='r') as f:
            self.db.cursor().executescript(f.read())
        self.db.commit()

    def get_user(self, email):
        return self.db.execute("select email, password from users where email = ?", (email,)).fetchone()

    def create_user(self, email, password):
        values = (email, hashlib.md5(password.encode("utf-8")).hexdigest())
        return self.db.execute("insert into users (email, password) values(?,?)", values)

    def get_entry(self, entry_name):
        return self.db.execute("select value from entries where link = ?", (entry_name,)).fetchone()

    def get_entries(self):
        return dict(self.db.execute("select link, title from entries").fetchall())


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config["DEBUG"] = True
    app.config["DATABASE"] = ":memory:"
    app.config["SECRET_KEY"] = "wow"
    db.init_app(app)
    return app

db = DB()

def requires_login(fn):
    @wraps(fn)
    def __inner(*a, **kw):
        def check_cookie():
            try:
                user = db.get_user(session.get("current_user"))
                return user and request.cookies["uid"] == hashlib.md5(
                    session.get("current_user").encode("utf-8")).hexdigest() + ":" + user[1]
            except Exception as e:
                return False
        if not ("uid" in request.cookies and check_cookie()):
            if "current_user" in session:
                session.pop("current_user")
            return redirect("/login?return=%s" % request.url_rule)
        return fn(*a, **kw)
    return __inner

def validate_login(email, password):
    flash_and_back = lambda msg:flash(msg, "warning") or redirect(url_for("test.login"))
    if not email:
        return flash_and_back("Email required")
    if not password:
        return flash_and_back("Password required")
    user = db.get_user(email)
    if user:
        if hashlib.md5(password.encode("utf-8")).hexdigest() == user[1]:
            cookie = ("uid", hashlib.md5(email.encode("utf-8")).hexdigest() + ":" + hashlib.md5(password.encode("utf-8")).hexdigest())
            response = make_response(redirect(request.args.get("return", "/")))
            session["current_user"] = email
            response.set_cookie(*cookie)
            return response
        else:
            return flash_and_back("Invalid password")
    else:
        return flash_and_back("Unknown user")

def validate_signup(email, password):
    flash_and_back = lambda msg:flash(msg, "warning") or redirect(url_for("test.signup"))
    if "current_user" in session:
        flash_and_back("You are already signed in")
    if not email:
        return flash_and_back("Email required")
    if not password:
        return flash_and_back("Password required")
    user = db.get_user(email)
    if user:
        return flash_and_back("User already exists")
    else:
        db.create_user(email, password)
        cookie = ("uid", hashlib.md5(email.encode("utf-8")).hexdigest() + ":" + hashlib.md5(password.encode("utf-8")).hexdigest())
        response = make_response(redirect(url_for("test.index")))
        session["current_user"] = email
        response.set_cookie(*cookie)
        return response

@bp.route("/")
@requires_login
def index():
    return render_template("index.html", callout="Here's a few ways it can be good", links=db.get_entries(), **view_vars)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.form:
        return  validate_login(request.form["email"], request.form["password"])
    return render_template("login.html", callout="Sign up", **view_vars)

@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if "current_user" in session:
        return redirect(url_for("test.index"))
    if request.form:
        return  validate_signup(request.form["email"], request.form["password"])
    return render_template("signup.html", callout="Testing is good", **view_vars)

@bp.route("/logout")
def logout():
    if "current_user" in session:
        session.pop("current_user")
    resp = redirect(url_for("test.index"))
    resp.set_cookie("uid", "", expires=0)
    return resp

@bp.route("/reference/<link>")
@requires_login
def reference(link):
    entry =  db.get_entry(link)
    if not entry:
        abort(404)
    else:
        return make_response(jsonify({"link":link, "data": entry[0]}))


if __name__ == "__main__":
    app = create_app()
    db.create_db()
    app.run()
