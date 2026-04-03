
# users

# grocery data

# get all data pertaining to a certain item
def get_item_data(item):
    keys = ["country", "name", "price", "month", "year"]
    2d_values = get_match_list("groceries", "name", item)
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

# helpers

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

# get_field_list: return all values in a specific field (column) in a row with a matching "id" item

# get_match_list: return all rows that have an "id" field matching the given argument
