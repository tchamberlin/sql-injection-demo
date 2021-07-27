from bottle import request, template, route, run, redirect


# Store a list of students. Looks like:
# [["thomas", "chamberlin"], ["other", "person"]]
students = []


def add_student(first_name, last_name):
    """Append a student to the global students list"""
    global students
    students.append([first_name, last_name])


# Handle all requests made to http://localhost:8085/
@route("/")
def index():
    """Homepage route"""
    # In response to a request to "/", render template student_dashboard.html
    # and give it access to the students variable
    if request.query.first_name_filter:
        filtered_students = [
            [first_name, last_name]
            for first_name, last_name in students
            if first_name.lower().startswith(request.query.first_name_filter.lower())
        ]
    else:
        filtered_students = students
    return template(
        "student_dashboard.html",
        students=filtered_students,
        first_name_filter=request.query.first_name_filter,
    )


@route("/add", method="POST")
def add():
    """Add student route"""
    # Get first/last name out of POST form data and append it to our CSV file
    add_student(request.forms.first_name, request.forms.last_name)
    # Redirect browser back to the home page
    return redirect("/")


# If run as a script
if __name__ == "__main__":
    # Run server on this computer, on port 8085, in debug mode (give extra info on errors)
    # also, automatically update the server process when this file changes
    run(host="localhost", port=8085, debug=True, reload=True)
