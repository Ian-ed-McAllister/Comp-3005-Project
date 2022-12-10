import psycopg2
import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2.extras
import random

con = None
cur = None
WAREHOUSES = ["bookHouse", "Big Book House", "Other warehouse"]


# simple call to get the books, users and genres and return them to the front end
def get_books():
    try:
        # connects to teh database
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # returns data in form of dict if needed.
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # runs the queries and saves them to variables
        cur.execute("SELECT * FROM books")
        values = cur.fetchall()
        cur.execute("SELECT * FROM genres")
        genres = cur.fetchall()
        cur.execute("SELECT * FROM authors")
        authors = cur.fetchall()

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()

    return values, genres, authors

# function make an order takes the billing/shipping info as parameters to make the order


def make_order(user, card_num, ccv, expiry, country, province, city, address, postal, order):
    try:
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # query to be made to add the order to the orders relation
        insert_script_orders = 'INSERT INTO orders (cid,shippedFrom,currentLocation,cardNum,expDate,ccv,country,province,streetAddress,city,postalCode) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        warehouse_index = random.randrange(len(WAREHOUSES))

        cur.execute(insert_script_orders, (user, WAREHOUSES[warehouse_index],
                    "in transit", card_num, expiry, ccv, country, province, address, city, postal))

        # used to get the newest order id to use in the following query
        cur.execute("SELECT * FROM orders ORDER BY oid DESC LIMIT 1")
        order_number = cur.fetchall()[0]["oid"]

        # query used to add to the contains table so that books can be added to the order
        insert_script_contains = 'INSERT INTO contains (oid,bid,quantity) Values (%s,%s,%s)'
        print(order)
        # used to loop over the all of the books in the cart to then run with the query
        for item in order:
            cur.execute(insert_script_contains,
                        (order_number, item[0], item[1]))

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()


# used to check if the user with username and password exists
def login_check(username, password):
    try:
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # query to check to see if the user exists, the {} will be replaced by the username and password
        login_script = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(
            username, password)
        cur.execute(login_script)
        user = cur.fetchall()[0]
        # retunrs the user afterwards if it exsists
        return user

    except Exception as error:
        print(error)
        return None
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()

# used to get the orders for a specific user


def get_orders(uid):
    try:
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        select_orders_script = '''SELECT * FROM orders WHERE cid = %s'''
        cur.execute(select_orders_script, (uid,))
        return cur.fetchall()
    except Exception as error:
        print(error)
        return None
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()

# used to update the users information


def update_user(user, cardnum, ccv, expdate, country, province, street_address, city, postal):
    try:
        # checking to see if any non nessesary information was ommited
        if cardnum == '':
            cardnum = None
        if ccv == '':
            ccv = None
        if expdate == '':
            expdate = None
        if country == '':
            country = None
        if province == '':
            province = None
        if street_address == '':
            street_address = None
        if city == '':
            city = None
        if postal == '':
            postal = None

        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # query to update the users inftormation based on a specific uid
        update_user_script = '''UPDATE users
                                SET cardnum = %s , ccv = %s, expdate = %s, country = %s, province = %s, streetaddress = %s, city = %s, postalcode = %s
                                WHERE uid = %s
                            '''
        cur.execute(update_user_script, (cardnum, ccv, expdate, country,
                    province, street_address, city, postal, user['uid']))

        # get the updated user
        cur.execute('SELECT * FROM users WHERE uid = %s', (user['uid'],))
        res = cur.fetchall()
        print(res)
        return res[0]
    except Exception as error:
        print("in error")
        print(error)
        return None
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()


# used to create a new users account with the information returns the new user to the frontend
def register_user(username, password, cardnum, ccv, expdate, country, province, street_address, city, postal):
    try:
        # chainging the parameters to work with null values
        if cardnum == '':
            cardnum = None
        if ccv == '':
            ccv = None
        if expdate == '':
            expdate = None
        if country == '':
            country = None
        if province == '':
            province = None
        if street_address == '':
            street_address = None
        if city == '':
            city = None
        if postal == '':
            postal = None

        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # create a new user witht he passed in information
        insert_user_script = 'INSERT INTO users (username,password,type,cardNum,ccv,expDate,country,province,streetAddress,city,postalCode) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        cur.execute(insert_user_script, (username, password, "U", cardnum,
                    ccv, expdate, country, province, street_address, city, postal))

        # log in to the user
        select_user_script = 'SELECT * FROM users WHERE username = %s AND password = %s'
        cur.execute(select_user_script, (username, password))
        return cur.fetchone()

    except Exception as error:
        print("in error")
        print(error)
        return None
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()

# gets all of the publishers


def get_publishers():
    try:
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # gets all of the publishers with all of their information
        cur.execute(
            "SELECT * FROM publisher")
        return cur.fetchall()
    except Exception as error:
        print(error)
        return None
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()


# used to update if the book will be shown in the book store
def update_shown(bid, val):
    try:
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # updates the book with the correct bid to be the opposite of waht it was originally
        cur.execute("UPDATE books SET show = %s WHERE bid = %s ",
                    (int(not val), int(bid)))

    except Exception as error:
        print(error)
        return None
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()


# used to get all of the financial information such as the money needed to pay out and the profits made retunrs a string with the information
def sum_costs_and_sales():
    try:
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # used to get all of the compensation cuts needed to pay out
        cur.execute("SELECT sum(compensation) AS costs FROM publisher")
        costs = cur.fetchall()[0]['costs']

        # first creates a new table that is one column that is the books sold multiplied by their price, these columns are later summed
        cur.execute('''SELECT sum(total_cost)
                    FROM (SELECT b.quantity*a.price AS total_cost
                        FROM books a, contains b
                        WHERE a.bid = b.bid) AS my_table''')
        rev = cur.fetchall()[0]['sum']
        print("Revenue: {}, Costs: {}, of the shop".format(rev, costs))
        return "Revenue: {}, Costs: {}, of the shop".format(rev, costs)

    except Exception as error:
        print("in error")
        print(error)
        return None
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()

# adds a new book to the books relation also adds genres and authors


def add_book(title, publisher, isbn, pages, price, cut, quantity, authors, genres):
    try:
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # adds the new book
        insert_script_books = 'INSERT INTO books (title,publisherName,isbn,numPages,price,percentage, quantity,show) Values (%s,%s,%s,%s,%s,%s,%s,%s)'
        cur.execute(insert_script_books, (title, publisher,
                    isbn, pages, price, cut, quantity, 1))

        # gets the books id
        cur.execute("SELECT bid FROM books ORDER BY bid DESC LIMIT 1 ")
        bid = cur.fetchall()[0]['bid']

        # adds the genre specified to the genre table with the book id of the new book
        insert_script_genres = 'INSERT INTO genres (bid,genre) Values (%s,%s)'
        for genre in genres:
            cur.execute(insert_script_genres, (bid, genre))

        # adds the new authors to the new books id in teh authours reation
        insert_script_authors = 'INSERT INTO authors (bid,authname) Values (%s,%s)'
        for auth in authors:
            cur.execute(insert_script_authors, (bid, auth))

    except Exception as error:
        print("in error")
        print(error)
        return None
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()
# cur.execute(
#     'INSERT INTO contains (oid,bid,quantity) Values (%s,%s,%s)', ("1", "3", "2"))
