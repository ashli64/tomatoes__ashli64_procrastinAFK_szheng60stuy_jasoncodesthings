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

#global variables

selected_grocery = ""
selected_time = []

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
        time = request.form.get('time').split('_') #helper variable
        month = int(time[0])
        year = int(time[1])

        global selected_time
        global selected_grocery

        selected_time = time
        selected_grocery = grocery

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
        if request.form.get('favoriteselect') != "None" and 'username' in session:
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
    print(selected_grocery)
    print(selected_time)
    testdata = data.best_deals_at(selected_grocery, int(selected_time[1]), int(selected_time[0]))
    filteredtest = data.best_per_country(testdata)
    print(filteredtest)
    testrange = data.get_range(filteredtest)
    testlow = data.get_lowest(filteredtest)

    return jsonify({
        "filtered": filteredtest,
        "range": testrange,
        "lowest": testlow
    })

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
