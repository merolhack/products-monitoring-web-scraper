import os
import logging
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

logging.basicConfig(filename='web-scraper-sql.log', level=logging.DEBUG)

PGSQL_HOST = os.getenv('PGSQL_HOST')
PGSQL_USER = os.getenv('PGSQL_USER')
PGSQL_PASSWORD = os.getenv('PGSQL_PASSWORD')
PGSQL_DB = os.getenv('PGSQL_DB')
PGSQL_PORT = os.getenv('PGSQL_PORT')

# Establish connection
def connect():
    with psycopg2.connect(database="products_monitoring_db",
        host=PGSQL_HOST,
        user=PGSQL_USER,
        password=PGSQL_PASSWORD,
        port=PGSQL_PORT) as conn:
        conn.set_session(autocommit=True)
    return conn

def find_uri(product_id):
    conn = connect()
    result = None
    try:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT    *  
                FROM    products
                WHERE
                    id = %(id)s
                """, {
                    'id': product_id
                })
            columns_descr = cur.description
            # If the SQL command is a SELECT statement, fetch the results
            if columns_descr:
                result = cur.fetchone()
                return result
            else:
                return None
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            # close communication with the database
            cur.close()

def update_product(product_id, name = None, sku = None, price = None, description = None, star_rating = None, review_counter = None, availability = None):
    conn = connect()
    # Format the price string
    if price != None:
        price = int(price)
    try:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                UPDATE    products
                SET 
                        name = %(name)s, 
                        sku = %(sku)s, 
                        price = %(price)s, 
                        description = %(description)s, 
                        star_rating = %(star_rating)s, 
                        review_counter = %(review_counter)s, 
                        availability = %(availability)s
                WHERE
                    id = %(id)s
                """, {
                    'id': product_id,
                    'name': name,
                    'sku': sku,
                    'price': price,
                    'description': description,
                    'star_rating': star_rating,
                    'review_counter': review_counter,
                    'availability': availability
                })
            columns_descr = cur.description
            # If the SQL command is a SELECT statement, fetch the results
            if columns_descr:
                result = cur.fetchone()
                return result
            else:
                return None
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            # close communication with the database
            cur.close()
