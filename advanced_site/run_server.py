# Load the DB string into the environment
from dotenv import load_dotenv

load_dotenv()
from index import app


def main():
    app.run(debug=True, reload=True)


if __name__ == "__main__":
    main()
