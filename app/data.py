import sqlite3                      # enable control of an sqlite database
import hashlib                      # for consistent hashes
import secrets                      # to generate ids


DB_FILE="data.db"

#=============================USERS=============================#


# returns a list of usernames
def get_all_users():

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT username FROM users').fetchall()

    db.commit()
    db.close()

    return clean_list(data)


# returns whether or not a user exists
def user_exists(username):
    all_users = get_all_users()
    for user in all_users:
        if (user == username):
            return True
    return False


# checks if provided password in login attempt matches user password
def auth(username, password):

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if not user_exists(username):
        db.commit()
        db.close()

        #raise ValueError("Username does not exist")
        return False

    # use ? for unsafe/user provided variables
    passpointer = c.execute('SELECT password FROM users WHERE username = ?', (username,))
    real_pass = passpointer.fetchone()[0]

    db.commit()
    db.close()

    password = password.encode('utf-8')

    # hash password here
    if real_pass != str(hashlib.sha256(password).hexdigest()):
        #raise ValueError("Incorrect password")
        return False

    return True


# adds a new user's data to user table
def add_user(username, password):

    if user_exists(username):
        #raise ValueError("Username already exists")
        return "Username already exists"

    if password == "":
        #raise ValueError("You must enter a non-empty password")
        return "Password cannot be empty"

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # hash password here
    password = password.encode('utf-8')
    password = str(hashlib.sha256(password).hexdigest())

    # use ? for unsafe/user provided variables
    c.execute('INSERT INTO users VALUES (?, ?)', (username, password,))

    db.commit()
    db.close()

    return "success"


# get a user's favorite searches
def get_fav_searches(user):
    keys = ["name", "month", "year"]
    2d_values = get_row_list("favs", "user", user)
    return 2d_list_to_dict_list(keys, 2d_values)


# add a favorite search for a user
def add_fav_search(user, item, year, month):

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    search_id = gen_id()
    c.execute('INSERT INTO favs VALUES (?, ?, ?, ?, ?)', (search_id, user, item, year, month,))

    db.commit()
    db.close()


# remove a favorite search
def remove_fav_search(search_id):
    remove_row("favs", search_id)


#=============================GROCERIES=============================#


# get all data pertaining to a certain item
def get_item_data(item):
    keys = ["country", "name", "price", "month", "year"]
    2d_values = get_row_list("groceries", "name", item)
    return 2d_list_to_dict_list(keys, 2d_values)


# filter a list of data on an item to only contain data from a specific year and month
def filter_time(itemdata, year, month):
    time_data = []
    for line in item_data:
        if (line["year"] == year or year == "any") and (line["month"] == month or month == "any"):
            time_data += [line]
    return time_data


# return a sorted list of good deals for a specific item
def best_deals(item):
    itemdata = get_item_data(item)
    # sort based on price
    for cur in range(len(itemdata)-1):
        bestind = cur
        bestprice = itemdata[cur]["price"]
        for i in range(len(itemdata, cur+1):
            if itemdata[i]["price"] < bestprice:
                bestind = i
                bestprice = itemdata[i]["price"]
        tmp = itemdata[cur]
        itemdata[cur] = itemdata[i]
        itemdata[i] = tmp
    return best_deals


# return a sorted list of good deals for a specific item at a specific time
def best_deals_at(item, year, month):
    all_deals = best_deals(item)
    return filter_time(itemdata, year, month)


# return a list of all items in the database
def available_items():
    items = get_field_list("groceries", "name")
    # remove duplicates
    return items



#=============================HELPERS=============================#


# turn a list of tuples (returned by .fetchall()) into a 1d list
def clean_list(raw_output):
    clean_output = []
    for lst in raw_output:
        for item in lst:
            if str(item) != 'None' and item != "":
                clean_output += [item]
    return clean_output


# turn a list of tuples (returned by .fetchall()) into a 2d list
def clean_list_2d(raw_output):
    clean_output = []
    for lst in raw_output:
        clean_1d = []
        for item in lst:
            if str(item) != 'None' and item != '':
                clean_1d += [item]
        if len(lst) > 0:
            clean_output += [lst]
    return clean_output


# convert a list of data into a dictionary
def list_to_dict(keys, values):
    if len(keys) != len(values):
        print("list_to_dict: length keys != length values")
        return {}
    dict = {}
    for i in range(len(keys)):
        dict[keys[i]] = values[i]
    return dict


# convert a 2d list of data to a list of dictionaries
def 2d_list_to_dict_list(keys, 2d_values):
    lst = []
    for vals in 2d_values:
        lst += [list_to_dict(keys, 2d_values)
    return lst


# get_field: return one value from the table based on another value in that row (an "id")
def get_field(table, ID_fieldname, ID, field):
    lst = get_field_list(table, ID_fieldname, ID, field)
    if (len(lst) == 0):
        return 'None'
    return lst[0]


# get_field_list: return all values in a specific field (column) in a row with a matching "id" item
def get_field_list(table, col_name, ID, field):

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # use ? for unsafe/user provided variables
    data = c.execute(f'SELECT {field} FROM {table} WHERE {col_name} = ?', (ID,)).fetchall()

    db.commit()
    db.close()

    return clean_list(data)


# get_row_list: return all rows that have an "id" field matching the given argument
def get_row_list(table, col_name, ID):

    db = sqlite3.connet(DB_FILE)
    c = db.cursor()

    # use ? for unsafe/user provided variables
    data = c.execute('SELECT * FROM {table} WHERE {col_name} = ?', (ID,)).fetchall()

    db.commit()
    db.close()

    return clean_list_2d(data)


# delete_row: delete a row of data from the table
def delete_row(table, ID_fieldname, id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # use ? for unsafe/user provided variables
    c.execute(f'DELETE FROM {table} WHERE {ID_fieldname} = ?', (id,))

    db.commit()
    db.close()


# generate an id
def gen_id():
    # use secrets module to generate a random 32-byte string
    return secrets.token_hex(32)
