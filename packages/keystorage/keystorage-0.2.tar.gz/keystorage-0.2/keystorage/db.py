import os
import click
import sqlite3

from .schema import instructions

def get_db():
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, "databases/")

    db = sqlite3.connect(path + "data.db")
    c = db.cursor()

    return db, c

def init_db() -> None:
    db, c = get_db()

    try:    
        for i in instructions:
            c.execute(i)
    except:
        pass

    db.commit()