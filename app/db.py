import sqlite3
from flask import g


def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect('instance/calender.db')
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db_connection():
    db = g.pop('db', None)
    if db is not None:
        db.close()
