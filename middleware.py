import psycopg2
import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2.extras
import random

con = None
cur = None
WAREHOUSES = ["bookHouse", "Big Book House", "Other warehouse"]


def get_books():
    try:
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # returns data in form of dict if needed.
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

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


def make_order(user, card_num, ccv, expiry, country, province, city, address, postal, order):
    try:
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        insert_script_orders = 'INSERT INTO orders (cid,shippedFrom,currentLocation,cardNum,expDate,ccv,country,province,streetAddress,city,postalCode) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        warehouse_index = random.randrange(len(WAREHOUSES))
        # change first index to the users uid
        cur.execute(insert_script_orders, (user, WAREHOUSES[warehouse_index],
                    "in transit", card_num, expiry, ccv, country, province, address, city, postal))

        cur.execute("SELECT * FROM orders ORDER BY oid DESC LIMIT 1")
        order_number = cur.fetchall()[0]["oid"]

        print("HERE")

        insert_script_contains = 'INSERT INTO contains (oid,bid,quantity) Values (%s,%s,%s)'
        print(order)
        for item in order:
            print(item[0])
            print(item[1])
            print("HERE 2")
            cur.execute(insert_script_contains,
                        (order_number, item[0], item[1]))

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()


# get_books()


con = psycopg2.connect(host=config.HOSTNAME,
                       dbname=config.DATABASE,
                       user=config.USERNAME,
                       password=config.PWD,
                       port=config.PORT_ID)
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)


def login_check(username, password):
    try:
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        login_script = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(
            username, password)
        cur.execute(login_script)
        user = cur.fetchall()[0]
        return user

    except Exception as error:
        print(error)
        return None
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()


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


def update_user(user, cardnum, ccv, expdate, country, province, street_address, city, postal):
    try:
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

        update_user_script = '''UPDATE users
                                SET cardnum = %s , ccv = %s, expdate = %s, country = %s, province = %s, streetaddress = %s, city = %s, postalcode = %s
                                WHERE uid = %s
                            '''
        cur.execute(update_user_script, (cardnum, ccv, expdate, country,
                    province, street_address, city, postal, user['uid']))

        cur.execute('SELECT * FROM users WHERE uid = %s', (user['uid'],))
        print("done here")
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


def register_user(username, password, cardnum, ccv, expdate, country, province, street_address, city, postal):
    try:
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

        insert_user_script = 'INSERT INTO users (username,password,type,cardNum,ccv,expDate,country,province,streetAddress,city,postalCode) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        cur.execute(insert_user_script, (username, password, "U", cardnum,
                    ccv, expdate, country, province, street_address, city, postal))

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


def get_publishers():
    try:
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute(
            "SELECT * FROM publisher")
        return cur.fetchall()
    except Exception as error:
        print("in error")
        print(error)
        return None
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()


def update_shown(bid, val):
    try:
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute("UPDATE books SET show = %s WHERE bid = %s ",
                    (int(not val), int(bid)))

    except Exception as error:
        print("in error")
        print(error)
        return None
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()


def sum_costs_and_sales():
    try:
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute("SELECT sum(compensation) AS costs FROM publisher")
        costs = cur.fetchall()[0]['costs']

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


def add_book(title, publisher, isbn, pages, price, cut, quantity, authors, genres):
    try:
        con = psycopg2.connect(host=config.HOSTNAME,
                               dbname=config.DATABASE,
                               user=config.USERNAME,
                               password=config.PWD,
                               port=config.PORT_ID)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        insert_script_books = 'INSERT INTO books (title,publisherName,isbn,numPages,price,percentage, quantity,show) Values (%s,%s,%s,%s,%s,%s,%s,%s)'
        cur.execute(insert_script_books, (title, publisher,
                    isbn, pages, price, cut, quantity, 1))

        cur.execute("SELECT bid FROM books ORDER BY bid DESC LIMIT 1 ")
        bid = cur.fetchall()[0]['bid']

        insert_script_genres = 'INSERT INTO genres (bid,genre) Values (%s,%s)'
        for genre in genres:
            cur.execute(insert_script_genres, (bid, genre))

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
