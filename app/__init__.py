from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for, jsonify

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

# @app.route("/")
# def hello():
#     return "<h1 style='color:blue'>Hello There!</h1>"

@app.route("/", methods=['GET', 'POST'])
def login():

    # stored active session, take user to response page
    if 'username' in session:
        return redirect(url_for("home"))

    if 'username' in request.form:
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        # check if password is correct, if not then reload page
        if not data.auth(username, password):
            return render_template("login.html", error="Username or password is incorrect")

        # if password is correct redirect home
        session["username"] = username
        return redirect(url_for("home"))

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('username', None) # remove username from session
    return redirect(url_for('login'))

@app.route('/register', methods=["GET", "POST"])
def register():

    if request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        # reload page if no username or password was entered
        if not username or not password:
            return render_template("register.html", error="No username or password inputted")

        # puts user into database unless if there's an error
        execute_register = data.add_user(username, password)
        if execute_register == "success":
            session['username'] = username
            return redirect(url_for("home"))
        else:
            return render_template("register.html", error = execute_register)
    return render_template("register.html")

@app.route("/home", methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        grocery = request.form.get('grocery')
        time = request.form.get('time').split('_')
        month = time[0]
        year = int(time[1])
        #print(grocery)
        #print(time)
        #print(month)
        #print(year)
        print(data.best_deals_at(grocery, year, month))
        print(data.best_deals(grocery))
        print(data.get_all_countries())

    return render_template("home.html")

#jsonify flask stuff to send to map.js

@app.route("/api/stats", methods=['GET'])
def returnStats():
    testdata = data.best_deals("Apples (1 kg)")
    filteredtest = data.best_per_country(testdata, 2026, 3)
    testrange = data.get_range(filteredtest)
    testlow = data.get_lowest(filteredtest)

    return jsonify({
        "filtered": filteredtest,
        "range": testrange,
        "lowest": testlow
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0')
