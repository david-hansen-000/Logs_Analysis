#!/usr/bin/pyton3

import psycopg2

dbname = "news"


def get_sql(sql):
    """Return all posts given the sql from the news database."""
    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute(sql)
    posts = c.fetchall()
    db.close()
    return posts
