import psycopg2
import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2.extras

con = None
cur = None
# NEED TO CHANGE USER AND PASSWORD TO ALLOW IT TO CONNECT TO YOUR LOCAL POSTGRES ISNTANCE
connection = psycopg2.connect(
    user=config.USERNAME,
    password=config.PWD)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = connection.cursor()


try:
    # USED TO INIT THE DATABASE IF IT DOES NOT ALREADY EXSIST
    name_Database = "MyTestDb"
    sqlCreateDatabase = "create database "+name_Database+";"
    #cur.execute("DROP DATABASE IF EXISTS mytestdb")
    cur.execute(sqlCreateDatabase)

except Exception as error:
    print(error)

cur.close()
connection.close()

try:
    con = psycopg2.connect(host=config.HOSTNAME,
                           dbname=config.DATABASE,
                           user=config.USERNAME,
                           password=config.PWD,
                           port=config.PORT_ID)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # returns data in form of dict if needed.
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("DROP TABLE IF EXISTS orders CASCADE")
    cur.execute("DROP TABLE IF EXISTS authors")
    cur.execute("DROP TABLE IF EXISTS genres")
    cur.execute("DROP TABLE IF EXISTS contains")
    cur.execute("DROP TABLE IF EXISTS books CASCADE")
    cur.execute("DROP TABLE IF EXISTS publisher CASCADE")
    cur.execute("DROP TABLE IF EXISTS users CASCADE")

    create_user = '''CREATE TABLE IF NOT EXISTS Users(
        username varchar(20) PRIMARY KEY,
        uid SERIAL UNIQUE,
        password varchar(20) NOT NULL,
        type char(1) NOT NULL,
        cardNum char(16),
        ccv char(3),
        expDate char(5),
        country varchar(22),
        province varchar(22),
        streetAdress varchar(30),
        city varchar(15),
        postalCode varchar(6)
        );'''
    cur.execute(create_user)

    # INIT THE users table with values
    insert_script_user = 'INSERT INTO users (username,password,type,cardNum,ccv,expDate,country,province,streetAdress,city,postalCode) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    insert_value_user = [("test3", "1", "A", "1234567891234567", "123", "12/24",
                          "CA", "Ontario", "1 west str.", "OTTAWA", "A1B1C1"), ("test4", "1", "U", "1234567891234567", "123", "11/24",
                                                                                "CA", "Alberta", "1 west str.", "OTTAWA", "A1B1C1"), ("Small", "big", "U", None, None, None, None, None, None, None, None)]
    for record in insert_value_user:
        cur.execute(insert_script_user, record)

    # create orders table.
    create_orders = '''CREATE TABLE IF NOT EXISTS orders(
        oid SERIAL PRIMARY KEY,
        cid int NOT NULL,
        shippedFrom varchar(20) NOT NULL,
        currentLocation varchar(20) NOT NULL,
        cardNum char(16) NOT NULL,
        expDate char(5) NOT NULL,
        ccv char(3) NOT NULL,
        country varchar(22) NOT NULL,
        province varchar(22) NOT NULL,
        streetAdress varchar(30) NOT NULL,
        city varchar(15) NOT NULL,
        postalCode char(6) NOT NULL,


        FOREIGN KEY (cid) REFERENCES users(uid)
        );'''
    cur.execute(create_orders)

    # insert values into the orders table
    insert_script_orders = 'INSERT INTO orders (cid,shippedFrom,currentLocation,cardNum,expDate,ccv,country,province,streetAdress,city,postalCode) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    WAREHOUSE = "bookHouse"
    insert_value_orders = [("1", WAREHOUSE, "in transit",
                            "1234567890123456", "07/12", "123", "CA", "Ontario", "123 Street", "Ottawa", "A1B2C3")]
    for record in insert_value_orders:
        cur.execute(insert_script_orders, record)

    create_publisher = '''CREATE TABLE IF NOT EXISTS publisher(
        pid SERIAL PRIMARY KEY,
        name varchar(20) UNIQUE NOT NULL,
        email varchar(40) NOT NULL,
        country varchar(22) NOT NULL,
        province varchar(22) NOT NULL,
        streetAdress varchar(20) NOT NULL,
        city varchar(20) NOT NULL,
        postalcode char(6) NOT NULL,
        bankid varchar(10) NOT NULL,
        compensation numeric (10,2) NOT NULL
        );'''
    cur.execute(create_publisher)

    # INIT THE publisher table
    insert_script_publisher = 'INSERT INTO publisher (name,email,country,province,streetAdress,city,postalcode,bankid,compensation) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    insert_value_publisher = [
        ("Best Books", "bestbooks@email.com", "CA", "Ontario", "1 Book street", "Ottawa", "K2L4F5", "1125634596", "0"), ("Better Books", "BetterBooks@email.com", "CA", "Ontario", "2 Book street", "Ottawa", "K2L4F5", "1125634596", "0")]
    for record in insert_value_publisher:
        cur.execute(insert_script_publisher, record)

    create_books = '''CREATE TABLE IF NOT EXISTS books(
        bid SERIAL PRIMARY KEY,
        title varchar(100) NOT NULL,
        publisherName varchar(20) NOT NULL,
        isbn char(13) NOT NULL,
        numPages int NOT NULL,
        price numeric (5,2),
        percentage numeric (3,2),
        quantity int,
        show int NOT NULL,
        FOREIGN KEY (publisherName) REFERENCES publisher(name)
        );'''
    cur.execute(create_books)

    # INIT THE books table
    insert_script_books = 'INSERT INTO books (title,publisherName,isbn,numPages,price,percentage, quantity,show) Values (%s,%s,%s,%s,%s,%s,%s,%s)'
    insert_value_books = [
        ("Book about books", "Best Books", "1111111111111", "112", "12.99", "0.3", "15", "1"), ("Another Great book", "Better Books", "1112111111111", "444", "20.99", "0.2", "15", "1"), ("NOT SHOWN BOOK", "Best Books", "1111115555551", "222", "12.99", "0.3", "15", "0")]
    for record in insert_value_books:
        cur.execute(insert_script_books, record)

    create_authors = '''CREATE TABLE IF NOT EXISTS authors(
        bid int,
        authName varchar(20),
        FOREIGN KEY (bid) REFERENCES books(bid),
        PRIMARY KEY (bid, authName)
        );'''
    cur.execute(create_authors)

    # INIT THE books table
    insert_script_books = 'INSERT INTO authors (bid,authname) Values (%s,%s)'
    insert_value_books = [
        ("1", "Phil"), ("1", "Bill"), ("2", "Jill"), ("3", "MANAGER")]
    for record in insert_value_books:
        cur.execute(insert_script_books, record)

    create_genres = '''CREATE TABLE IF NOT EXISTS genres(
        bid int,
        genre varchar(20),
        FOREIGN KEY (bid) REFERENCES books(bid),
        PRIMARY KEY (bid, genre)
        );'''
    cur.execute(create_genres)

    # INIT THE books table
    insert_script_genres = 'INSERT INTO genres (bid,genre) Values (%s,%s)'
    insert_value_genres = [
        ("1", "Science"), ("1", "Fiction"), ("2", "Non Fiction"), ("3", "Not shown")]
    for record in insert_value_genres:
        cur.execute(insert_script_genres, record)

    create_contains = '''CREATE TABLE IF NOT EXISTS contains(
        oid int,
        bid int,
        quantity int,
        
        FOREIGN KEY  (oid) REFERENCES orders(oid),
        FOREIGN KEY (bid) REFERENCES books(bid),
        PRIMARY KEY (oid, bid)
        );'''
    cur.execute(create_contains)

    # INIT THE books table
    insert_script_contains = 'INSERT INTO contains (oid,bid,quantity) Values (%s,%s,%s)'
    insert_value_contains = [
        ("1", "1", "1")]
    for record in insert_value_contains:
        cur.execute(insert_script_contains, record)

    # triggers/ functions will be below this line

    # used to reduce the stock of the books purchased in the books table
    cur.execute('''CREATE OR REPLACE FUNCTION reduce_quantity()
                    RETURNS TRIGGER
                    LANGUAGE plpgsql
                    AS
                    $$
                    BEGIN
                        RAISE NOTICE '%s', NEW.quantity;
                        UPDATE books
                        SET quantity = quantity - NEW.quantity
                        WHERE books.bid = NEW.bid;
                        RETURN NEW;
                    END;
                    $$
                ''')
    # used to trigger the above function on a insert (a new purchace) in the contains table
    cur.execute('''CREATE OR REPLACE TRIGGER contains_trigger
                AFTER INSERT
                ON contains
                FOR EACH ROW
                EXECUTE PROCEDURE reduce_quantity()
                
                ''')
    # used to add to the compensation
    cur.execute('''CREATE OR REPLACE FUNCTION compensation_add()
                RETURNS TRIGGER
                LANGUAGE plpgsql
                    AS
                    $$
                    BEGIN
                        IF NEW.quantity < OLD.quantity then
                        UPDATE publisher
                        SET compensation = compensation + ((OLD.price * (OLD.quantity - NEW.quantity))*OLD.percentage)
                        WHERE publisher.name = NEW.publishername;
                        END IF;
                        RETURN NEW;
                    END;
                    $$
                
                ''')

    cur.execute('''CREATE OR REPLACE TRIGGER compensation_trigger
                AFTER UPDATE
                ON books
                FOR EACH ROW
                EXECUTE PROCEDURE compensation_add()
                ''')

    cur.execute('''CREATE OR REPLACE FUNCTION reorder_check()
                RETURNS TRIGGER
                LANGUAGE plpgsql
                    AS
                    $$
                    BEGIN
                        IF NEW.quantity < 10 then
                        UPDATE books
                        SET quantity = quantity  + (SELECT sum(quantity) FROM contains WHERE bid = NEW.bid)
                        WHERE books.bid = NEW.bid;
                        END IF;
                        RETURN NEW;
                    END;
                    $$
                
                ''')

    cur.execute('''CREATE OR REPLACE TRIGGER reorder_trigger
                AFTER UPDATE
                ON books
                FOR EACH ROW
                EXECUTE PROCEDURE reorder_check()
                ''')


except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if con is not None:
        con.close()
