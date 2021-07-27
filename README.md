# SQL Injection Demo

Simple SQL injection demo, written in [Bottle](https://bottlepy.org). Intended to explain this comic strip:

![Her daughter is named Help I'm trapped in a driver's license factory.](https://imgs.xkcd.com/comics/exploits_of_a_mom.png "Exploits of a Mom")

## Disclaimer

This software is intended for educational purposes only. Do not attempt to run any of this software on any computer/network that you do not own.

This was made for a lunch talk; it's not particularly polished. If you are not already somewhat familiar with Python and PostgreSQL, you probably won't get much out of this.


## Install

Requirements:

* Python 3.8+ (only because of new-syntax f-strings)
* PostgreSQL 9+

I've only tested this on Linux with PostgreSQL 9/12, but it should be pretty portable

```sh
python -m venv sql-injection-demo-env
source sql-injection-demo-env/bin/activate
pip install -r requirements.txt
```

## Getting Started

Okay, now what?

### Basic Site

The `basic_site/` folder contains some examples of a very basic website. If you've never worked with websites before, it might be good to play around here to get a feel for the Bottle framework, etc., before diving into the SQL injection portion

### Advanced Site

The `advanced_site/` folder contains the core of the repo: the SQL injection demo. To run it:

1. Create a database in PostgreSQL to use for this demo, e.g. `$ createdb inject-test`
1. Populate the database, e.g. `$ psql inject-test < advanced_site/db/init_schema.sql`
1. Create your `.env` file: `cp .env.example .env`, then edit to match your created DB/username
1. Create your virtual env, if you didn't already, and activate it
1. `$ cd ./advanced_site/`
1. Use `$ python run_server.py` to run the server on your local machine
1. Navigate to URL it gives you to use the site

Once running, there are two main things you can do:

1. Log in
2. Add students

Both of these forms execute queries that are vulnerable to SQL injection. There are also "safe" versions of each form available at `/login/fixed` and `/students/fixed`; these are not vulnerable.
