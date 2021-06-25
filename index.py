#! /usr/bin/env python3

"""docstring"""


import argparse
from datetime import datetime

from bottle import (
    Bottle,
    static_file,
    redirect,
    route,
    run,
    jinja2_template as template,
    request,
)
import psycopg2

import psycopg2.extensions
import logging

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers.sql import PostgresLexer

queries = []
errors = []


app = Bottle()

logged_in = False


class CodeHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile):
        return self._wrap_code(source)

    def _wrap_code(self, source):
        yield 0, '<div class="highlight">'
        for i, t in source:
            if i == 1:
                # it's a line of formatted code
                t += "<br>"
            yield i, t
        yield 0, "</div>"


class LoggingCursor(psycopg2.extensions.cursor):
    def execute(self, sql, args=None):
        global errors
        query = self.mogrify(sql, args).decode("utf-8")
        logger = logging.getLogger("sql_debug")
        logger.info(f"Query: '{query}'")

        error_ = None
        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
        except Exception as error:
            logger.error(f"{error.__class__.__name__}: {error}")
            errors = [str(error)]
            error_ = error
            raise
        finally:
            queries.append(
                (
                    datetime.now(),
                    highlight((query), PostgresLexer(), CodeHtmlFormatter()),
                    error_,
                )
            )


# TODO: cli args
conn = psycopg2.connect(dbname="inject-test", host="galileo")
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor(cursor_factory=LoggingCursor)


def get_students():
    cursor.execute("SELECT id, first_name, last_name FROM students")
    ret = cursor.fetchall()
    return ret


def check_login_bad(username, password):
    query = (
        "SELECT id, username, password FROM users "
        f"WHERE username = '{username}' AND password = '{password}'"
    )
    cursor.execute(query)
    actual_query = cursor.query.decode("utf-8")
    result = cursor.fetchone()
    return result, actual_query


def do_add_student_bad(first_name, last_name):
    query = (
        "INSERT INTO students (first_name, last_name) VALUES "
        f"('{first_name}', '{last_name}')"
    )
    cursor.execute(query)
    print(f"{query=}")
    actual_query = cursor.query.decode("utf-8")
    try:
        results = cursor.fetchone()
    except psycopg2.ProgrammingError:
        results = []
    return results, actual_query

def do_add_student_good(first_name, last_name):
    query = (
        "INSERT INTO students (first_name, last_name) VALUES "
        "(%s, %s)"
    )
    cursor.execute(query, (first_name, last_name))
    print(f"{query=}")
    actual_query = cursor.query.decode("utf-8")
    try:
        results = cursor.fetchone()
    except psycopg2.ProgrammingError:
        results = []
    return results, actual_query

@app.route("/")
def index():
    return template("templates/index.html", queries=queries[-10:])


@app.route("/admin/queries")
def debug_queries():
    return template("templates/queries.html", queries=queries[-10:])


@app.route("/students", method="GET")
def add_student_form():
    if logged_in:
        try:
            students = get_students()
        except psycopg2.DatabaseError:
            students = []
        num_students = len(students)
        return template(
            "templates/add_students.html",
            students=students,
            num_students=num_students,
            queries=queries[-10:],
            errors=errors,
        )
    else:
        return template("templates/login_required.html")


@app.route("/students/add", method="POST")
def add_student_submit():
    global errors
    errors = []
    try:
        do_add_student_bad(
            first_name=request.forms.first_name, last_name=request.forms.last_name
        )
    except psycopg2.DatabaseError:
        pass
    else:
        errors = []

    return redirect("/students")


@app.route("/login")
def login():
    return template("templates/login.html", queries=queries[-10:])

@app.route("/logout")
def logout():
    global logged_in
    logged_in = False
    return template("templates/logout.html", queries=queries[-10:])


@app.route("/login", method="POST")
def post_login():
    global errors
    global logged_in
    username = request.forms.get("username")
    password = request.forms.get("password")
    try:
        result, query = check_login_bad(username, password)
    except psycopg2.DatabaseError:
        success = False
        query = None
    else:
        errors = []
        success = bool(result)
        if success:
            (__, username, __) = result
            logged_in = True

    return template(
        "templates/post_login.html",
        success=success,
        username=username,
        query=query,
        queries=queries[-10:],
        errors=errors,
    )


@app.route("/static/<filename:path>")
def send_static(filename):
    return static_file(filename, root="static/")


def main():
    args = parse_args()
    init_logging(logging.DEBUG if args.verbose else logging.WARNING)
    app.run(host=args.host, port=args.port, debug=args.debug, reloader=args.reload)


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--reload", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    return parser.parse_args()


def init_logging(level=logging.WARNING):
    _logger = logging.getLogger("sql_debug")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))

    _logger.addHandler(console_handler)
    _logger.setLevel(level)


if __name__ == "__main__":
    main()
