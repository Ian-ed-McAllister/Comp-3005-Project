import psycopg2
import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2.extras

con = None
cur = None


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


get_books()
