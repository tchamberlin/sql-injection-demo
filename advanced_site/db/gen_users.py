#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate any number of randomly generated users for the users table"""


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


def gen_users(num_users):
    # TODO: don't hardcode this
    conn = psycopg2.connect(dbname="inject-test", host="localhost")
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    users = (
        f"{fake.first_name().lower()}\t{fake.password()}" for __ in range(num_users)
    )
    file = StringIO("\n".join(users))
    cursor.copy_from(
        file,
        "users",
        columns=[
            "username",
            "password",
        ],
    )
    cursor.execute("SELECT COUNT(*) FROM users")
    result = cursor.fetchone()
    print(f"There are now {result[0]} users in the DB")
    return users


def main():
    args = parse_args()
    users = gen_users(args.num_users)
    print(f"Successfully generated {args.num_users} users")


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("num_users", type=int, help="The number of users to generate")
    return parser.parse_args()


if __name__ == "__main__":
    main()
