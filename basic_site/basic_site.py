from bottle import route, run


# Handle all requests made to http://localhost:8085/
@route("/")
def index():
    return "Hello World!"


# If run as a script
if __name__ == "__main__":
    # Run server on this computer, on port 8085, in debug mode (give extra info on errors)
    # also, automatically update the server process when this file changes
    run(host="localhost", port=8085, debug=True, reload=True)
