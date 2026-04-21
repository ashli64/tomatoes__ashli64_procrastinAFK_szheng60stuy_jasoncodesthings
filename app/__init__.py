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
        account = c.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()
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
        time = request.form.get('time').split('_') #helper variable
        month = int(time[0])
        year = int(time[1])

        favoriteadd = request.form.get('favoriteadd')
        if favoriteadd:
            #print("omg it works")
            if 'username' not in session:
                print("The search input did not save because you are not logged in.") #have a variable that tells you if the favorite add works or not
            else:
                grocery = request.form.get('grocery')
                grocery = grocery.replace(' ', '_')
                #time = request.form.get('time').split('_') #helper variable
                #month = int(time[0])
                #year = int(time[1])
                grocery = grocery + "|" + time[0] + "|" + time[1]
                data.add_fav_search(session.get('username'), grocery, year, month)

        #print("fme")
        #print(request.form.get('favoriteselect'))
        if request.form.get('favoriteselect') != "None":
            favoriteselect=request.form.get('favoriteselect')
            favoriteselect_to_list = favoriteselect.split("|")
            grocery = favoriteselect_to_list[0].replace('_', ' ')
            month = int(favoriteselect_to_list[1])
            year = int(favoriteselect_to_list[2])
        #print("aaaa")
        #print(grocery)
        #print(month)
        #print(year)
        #print("bbbb")

    if 'username' in session:
        fav_list = data.get_fav_searches(session.get('username')) #if have time, for loop that goes through dict and makes a list of DISPLAY names
        #print(fav_list)
        return render_template("home.html", loggedin = "true", fav_list = fav_list)
    return render_template("home.html", loggedin = "false")

#jsonify flask stuff to send to map.js

@app.route("/api/stats", methods=['GET'])
def returnStats():
    testdata = data.get_item_data("Apples (1 kg)")
    filteredtest = data.filter_time(testdata, 2026, 3)
    testrange = data.get_range(filteredtest)
    testlow = data.get_lowest(filteredtest)

    return jsonify({
        "filtered": filteredtest,
        "range": testrange,
        "lowest": testlow
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0')
