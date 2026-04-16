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
    keys = ["id", "user", "name", "month", "year"]
    values = get_row_list("favs", "user", user)
    return list_2d_to_dict_list(keys, values)


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
    delete_row("favs", "search_id", search_id)


#=============================GROCERIES=============================#


# get all data pertaining to a certain item
def get_item_data(item):
    keys = ["country", "name", "price", "month", "year"]
    values = get_row_list("groceries", "name", item)
    return list_2d_to_dict_list(keys, values)


# filter a list of data on an item to only contain data from a specific year and month
def filter_time(item_data, year, month):
    time_data = []
    for line in item_data:
        i_year = str(line["year"])
        i_month = str(line["month"])
        if (i_year == str(year) or year == "") and (i_month == str(month) or month == ""):
            time_data += [line]
    return time_data


# return a sorted list of good deals for a specific item
def best_deals(item):

    item_data = get_item_data(item)
    
    # sort based on price -- selection sort (i think?)
    for cur in range(len(item_data)-1):
    
        lowest_ind = cur
        lowest_price = item_data[cur]["price"]

        # find the next lowest value
        for i in range(cur+1, len(item_data)):
            item = item_data[i]
            if item["price"] < lowest_price:
                lowest_price = item["price"]
                lowest_ind = i

        # move the lowest to the front of the unsorted section
        tmp = item_data[cur]
        item_data[cur] = item_data[lowest_ind]
        item_data[lowest_ind] = tmp
        
    return item_data


# return a sorted list of good deals for a specific item at a specific time
def best_deals_at(item, year, month):
    return filter_time(best_deals(item), year, month)


# return a list of all items in the database
def get_all_items():
    items = get_col_list("groceries", "name")
    # remove duplicates
    for item in items:
        while items.count(item) > 1:
            items.remove(item)
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
def list_2d_to_dict_list(keys, values):
    lst = []
    for val_sublst in values:
        lst += [list_to_dict(keys, val_sublst)]
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

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # use ? for unsafe/user provided variables
    data = c.execute(f'SELECT * FROM {table} WHERE {col_name} = ?', (ID,)).fetchall()

    db.commit()
    db.close()

    return clean_list_2d(data)


# return a list of all items in a column of the table
def get_col_list(table, col_name):

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # no unsafe/user-provided vars here, safe to use f-strings
    data = c.execute(f'SELECT {col_name} FROM {table}').fetchall()

    db.commit()
    db.close()

    return clean_list(data)


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
