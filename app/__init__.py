from flask import Flask
app = Flask(__name__)

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for

import sqlite3   #enable control of an sqlite database
import datetime

# our helper db files
import data_setup
import data


DB_FILE="data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

# create tables
data_setup.create_users_table()
data_setup.create_favs_table()
data_setup.create_groceries_table()

app = Flask(__name__)
app.secret_key = "secret"


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # store username and password as a variable
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        # render login page if username or password box is empty
        if not username or not password:
            return render_template('login.html', error="No username or password inputted")

        #search user table for password from a certain username
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        account = c.execute("SELECT password FROM users WHERE name = ?", (username,)).fetchone()
        db.close()

        #if there is no account then reload page
        if account is None:
            return render_template("login.html", error="Username or password is incorrect")

        # check if password is correct, if not then reload page
        if account[0] != password:
            return render_template("login.html", error="Username or password is incorrect")

        # if password is correct redirect home
        session["username"] = username
        return redirect(url_for("home"))

    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('username', None) # remove username from session
    return redirect(url_for('login'))

@app.route("/home")
def home():
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')
