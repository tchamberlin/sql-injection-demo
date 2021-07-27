import psycopg2

from pygments import highlight
from pygments.formatters import Terminal256Formatter

from pygments.lexers.sql import PostgresLexer

from utils import cursor


def add_student(first_name, last_name, card_info):
    """Add student with given info to database"""

    try:
        # THIS IS WHERE THE MAGIC HAPPENS
        query = (
            "INSERT INTO students (card_info, first_name, last_name) VALUES "
            f"('{card_info}', '{first_name}', '{last_name}')"
        )
        print("Executing query:")
        print(f"\n    {highlight((query), PostgresLexer(), Terminal256Formatter())}\n")
        cursor.execute(query)

        query = (
            "SELECT id, first_name, last_name, card_info FROM students "
            "WHERE first_name = %s AND last_name = %s ORDER BY ID DESC LIMIT 1"
        )
        cursor.execute(query, (first_name, last_name))
        result = cursor.fetchone()
        print("Newly-added student:")
        print(result)
    except psycopg2.DatabaseError:
        # We don't care about DB errors (they'll show up in Ipython anyway)
        pass


add_student("thomas", "chamberlin", "###")
