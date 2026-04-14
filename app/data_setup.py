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

# groceries
def create_groceries_table():
    contents =  """
                CREATE TABLE IF NOT EXISTS groceries (
                    country         TEXT        NOT NULL,
                    name            TEXT        NOT NULL,
                    price           REAL        NOT NULL,
                    month           INTEGER     NOT NULL,
                    year            INTEGER     NOT NULL
                )"""
    create_table(contents)
    # initialize the table with values
    parse_csv()

# favs
def create_favs_table():
    contents = """
               CREATE TABLE IF NOT EXISTS favs (
                   search_id       TEXT         NOT NULL    PRIMARY KEY,
                   user	    	   TEXT	        NOT NULL,
                   item            TEXT         NOT NULL,
                   month           INTEGER,
                   year            INTEGER
               )"""
    create_table(contents)

#=============================PARSE=CSVS=============================#

def parse_csv():

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # first of all, check if the table is already populated
    c.execute("SELECT COUNT(*) FROM groceries")
    rows = int(c.fetchone()[0])
    if (rows > 0):
        return;

    # parse each line of the csv
    filelines = []
    with open("grocery.csv") as f:
        filelines = f.readlines()[1:]   # get rid of the headaer line

    for line in filelines:

        # deal with items that have our delimiter, commas, in them (in quotes)
        quote_ind = line.find('"')
        if quote_ind != -1:
            # search through this segment until the closing " for commas
            quote_ind+=1
            while line[quote_ind] != '"':
                if line[quote_ind] == ',':
                    # replace with semicolons
                    line = line[:quote_ind] + ';' + line[quote_ind+1:]
                quote_ind+=1

        # extract the data we need
        items = line.split(",")
        country = items[1]
        name = items[7]
        price = items[14]	# convert to numerical
        time = items[5]		# convert to numerical

        # change into preferred format
        pricenum = round(float(price),2)
        monthnum = int(time[5:])
        yearnum = int(time[:4])

        # add field to table
        c.execute('INSERT INTO groceries VALUES (?, ?, ?, ?, ?)', (country, name, pricenum, monthnum, yearnum,))

    db.commit()
    db.close()

#=============================GENERAL=HELPERS=============================#

def create_table(contents):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(contents)
    db.commit()
    db.close()
