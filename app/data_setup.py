import sqlite3                      # enable control of an sqlite database
import hashlib                      # for consistent hashes
import secrets                      # to generate ids

DB_FILE="data.db"

#=============================MAKE=TABLES=============================#

# users
def create_users_table():
    contents =  """
                CREATE TABLE IF NOT EXISTS users (
                    username        TEXT        NOT NULL    PRIMARY KEY,
                    password        TEXT        NOT NULL
                )"""
    create_table(contents)

# grocery
def create_grocery_table():
    contents =  """
                CREATE TABLE IF NOT EXISTS grocery (
                    country         TEXT        NOT NULL,
                    name            TEXT        NOT NULL,
                    price           REAL        NOT NULL,
                    month           INTEGER     NOT NULL,
                    year            INTEGER     NOT NULL
                )"""
    create_table(contents)

#=============================PARSE=CSVS=============================#

def parse_csv():

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # parse each line of the csv
    # clean for only the data we need
    # change into preferred format
    # add field to table
    c.execute('INSERT INTO grocery VALUES (?, ?, ?, ?, ?)', (country, name, price, month, year,))

    db.commit()
    db.close()

#=============================GENERAL=HELPERS=============================#

def create_table(contents):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(contents)
    db.commit()
    db.close()
