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

        insert_script_orders = 'INSERT INTO orders (cid,shippedFrom,currentLocation,cardNum,expDate,ccv,country,province,streetAdress,city,postalCode) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        warehouse_index = random.randrange(len(WAREHOUSES))
        # change first index to the users uid
        cur.execute(insert_script_orders, ('1', WAREHOUSES[warehouse_index],
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

# cur.execute(
#     'INSERT INTO contains (oid,bid,quantity) Values (%s,%s,%s)', ("1", "3", "2"))
