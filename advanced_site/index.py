#!/usr/bin/env python3

"""THE WEBSITE

All Bottle routes are defined here
"""


import psycopg2

from bottle import (
    Bottle,
    static_file,
    redirect,
    request,
)


from utils import cursor, appState, template

app = Bottle()


def get_students():
    """Get all students from the database

    There is no opportunity for SQL injection here, as we are not accepting any
    user inputs
    """

    cursor.execute(
        "SELECT id, first_name, last_name, card_info FROM students ORDER BY id DESC"
    )
    ret = cursor.fetchall()
    return ret


def check_login_bad(username, password):
    """Verify login. VULNERABLE TO SQL INJECTION

    Returns the result: a tuple of (id, username, password). Or, None if no results
    """
    # Note that we are building our own query via an f-string: this is what makes
    # us vulnerable to SQL injection
    query = (
        "SELECT id, username, password FROM users "
        f"WHERE username = '{username}' AND password = '{password}'"
    )
    cursor.execute(query)
    result = cursor.fetchone()
    return result


def check_login_good(username, password):
    """Verify login. NOT vulnerable to sql injection

    Returns the result: a tuple of (id, username, password). Or, None if no results
    """
    # Note that we are NOT building our own query via string formatting --
    # we are allowing the psycopg2 library to handle escaping the user inputs
    query = (
        "SELECT id, username, password FROM users "
        "WHERE username = %s AND password = %s"
    )
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    return result


def do_add_student_bad(first_name, last_name, card_info):
    """Insert a student into the DB. VULNERABLE TO SQL INJECTION"""

    # Note that we are building our own query via an f-string: this is what makes
    # us vulnerable to SQL injection
    query = (
        "INSERT INTO students (card_info, first_name, last_name) VALUES "
        f"('{card_info}', '{first_name}', '{last_name}')"
    )
    cursor.execute(query)


def do_add_student_good(first_name, last_name, card_info):
    """Insert a student into the DB. NOT vulnerable to sql injection"""

    # Note that we are NOT building our own query via string formatting --
    # we are allowing the psycopg2 library to handle escaping the user inputs
    query = (
        "INSERT INTO students (first_name, last_name, card_info) VALUES (%s, %s, %s)"
    )
    cursor.execute(query, (first_name, last_name, card_info))


@app.route("/")
def index():
    return template("templates/index.html")


def _students(behave_sensibly):
    """List all students

    Handle both "good" and "bad" versions (to keep code DRY)
    """

    if appState.logged_in:
        try:
            students = get_students()
        except psycopg2.DatabaseError:
            students = []

        num_students = len(students)

        return template(
            "templates/add_students.html",
            students=students,
            num_students=num_students,
            submit_to="/students/add/fixed" if behave_sensibly else "/students/add",
        )

    return template("templates/login_required.html")


@app.route("/students/fixed", method="GET")
def students_good():
    return _students(behave_sensibly=True)


@app.route("/students", method="GET")
def students_bad():
    return _students(behave_sensibly=False)


def _add_student_submit(behave_sensibly):
    """Allow addition of new students

    Handle both "good" and "bad" versions (to keep code DRY)
    """

    try:
        if behave_sensibly:
            do_add_student_good(
                first_name=request.forms.first_name,
                last_name=request.forms.last_name,
                card_info=request.forms.card_info,
            )
        else:
            do_add_student_bad(
                first_name=request.forms.first_name,
                last_name=request.forms.last_name,
                card_info=request.forms.card_info,
            )
    except psycopg2.DatabaseError:
        pass

    return redirect("/students")


@app.route("/students/add/fixed", method="POST")
def add_student_submit_good():
    return _add_student_submit(behave_sensibly=True)


@app.route("/students/add", method="POST")
def add_student_submit_bad():
    return _add_student_submit(behave_sensibly=False)


@app.route("/login")
def login():
    return template("templates/login.html", submit_to="/login")


@app.route("/login/fixed")
def login_fixed():
    return template("templates/login.html", submit_to="/login/fixed")


@app.route("/logout")
def logout():
    appState.logged_in = False
    return template("templates/logout.html")


def _post_login(behave_sensibly):
    """Handle login

    Handle both "good" and "bad" versions (to keep code DRY)
    """

    username = request.forms.get("username")
    password = request.forms.get("password")
    try:
        if behave_sensibly:
            result = check_login_good(username, password)
        else:
            result = check_login_bad(username, password)
    except psycopg2.DatabaseError:
        success = False
    else:
        success = bool(result)
        if success:
            (__, username, __) = result
            appState.logged_in = True

    return template(
        "templates/post_login.html",
        success=success,
        username=username,
        errors=appState.errors,
    )


@app.route("/login/fixed", method="POST")
def post_login_good():
    return _post_login(behave_sensibly=True)


@app.route("/login", method="POST")
def post_login_bad():
    return _post_login(behave_sensibly=False)


@app.route("/static/<filename:path>")
def send_static(filename):
    """Serve all static files in /static"""
    return static_file(filename, root="static/")
