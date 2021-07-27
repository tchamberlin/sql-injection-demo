import csv

from bottle import request, template, route, run, redirect


def read_students_from_csv():
    """Return a list of lists from the students CSV"""
    with open("./students.csv", newline="") as file:
        reader = csv.reader(file)
        return [row for row in reader]


def write_students_to_csv(students, mode="a+"):
    """Add given students to the CSV file"""
    with open("./students.csv", mode, newline="") as file:
        writer = csv.writer(file)
        writer.writerows(students)


# Handle all requests made to http://localhost:8085/
@route("/")
def index():
    students = read_students_from_csv()
    if request.query.first_name_filter:
        filtered_students = [
            [first_name, last_name]
            for first_name, last_name in students
            if first_name.lower().startswith(request.query.first_name_filter.lower())
        ]
    else:
        filtered_students = students
    # In response to a request to "/", render template student_dashboard.html
    # and give it access to the students from our CSV file
    return template(
        "student_dashboard.html",
        students=filtered_students,
        first_name_filter=request.query.first_name_filter,
    )


# If run as a script
@route("/add", method="POST")
def add():
    # Get first/last name out of POST form data and append it to our CSV file
    write_students_to_csv([(request.forms.first_name, request.forms.last_name)])
    # Redirect browser back to the home page
    return redirect("/")


if __name__ == "__main__":
    # Create empty students list every time the server restarts
    # write_students_to_csv([], mode="w")
    # Run server on this computer, on port 8085, in debug mode (give extra info on errors)
    # also, automatically update the server process when this file changes
    run(host="localhost", port=8085, debug=True, reload=True)
