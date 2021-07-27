#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate any number of randomly generated students for the students table"""


import argparse
from io import StringIO

from faker import Faker
import psycopg2
import re

fake = Faker()
# Allow for deterministic generation
Faker.seed(0)


card_regex = re.compile(r"\w+\n[\w\s]+\n(\d+)\s(\d+/\d+)\n\w+: (\d+)\n")


def gen_card_parts():
    return " ".join(card_regex.search(fake.credit_card_full()).groups())


def gen_students(num_students):
    # TODO: don't hardcode this
    conn = psycopg2.connect(dbname="inject-test", host="localhost")
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    students = (
        f"{fake.first_name()}\t{fake.last_name()}\t{fake.credit_card_number()}"
        for __ in range(num_students)
    )
    file = StringIO("\n".join(students))
    cursor.copy_from(
        file,
        "students",
        columns=[
            "first_name",
            "last_name",
            "card_info",
        ],
    )
    cursor.execute("SELECT COUNT(*) FROM students")
    result = cursor.fetchone()
    print(f"There are now {result[0]} students in the DB")
    return students


def main():
    args = parse_args()
    students = gen_students(args.num_students)
    print(f"Successfully generated {args.num_students} students")


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "num_students", type=int, help="The number of students to generate"
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
