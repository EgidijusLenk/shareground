import sqlite3
from sqlite3 import Error

from scrape import metadata_tags

con = sqlite3.connect("db.sqlite", check_same_thread=False)
cur = con.cursor()
# cur.execute("CREATE TABLE lists(unique_string TEXT NOT NULL UNIQUE, url TEXT NOT NULL);")
# cur.execute("ALTER TABLE lists ADD metadata TEXT;")



shortened_links: dict = {}


#--------random id generator---------
from enum import unique
import string
import random
def id_generator(size=7, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))
#------------------------------------


def shortener(long_url):
    """creates unique string for long_url,
    adds it to db (to "shortened_links" dict far)
    """
    metadata_tags_list = metadata_tags(long_url) # sita reikia prideti prie sql i nauja column
    unique_string = id_generator()
    # f.read()
    while unique_string in shortened_links:
        print(f"{unique_string} is already set")
        unique_string = id_generator()
    shortened_links[unique_string] = long_url
    

    try:
        cur.execute("""INSERT INTO lists
                            (unique_string, url, metadata) 
                            VALUES 
                            (?, ?, ?)""", (unique_string, long_url, str(metadata_tags_list)))
        con.commit()
    except Error as error:
        print("Failed to insert data into sqlite table:", error)
        shortener(long_url)
    return (unique_string, metadata_tags_list)

# shortener("domain.com") #for test

print(shortened_links)


def db_metadata_grabber(unique_string):
    metadata = []
    try:
        cur.execute(f"""SELECT metadata FROM lists WHERE unique_string = '{unique_string}'""")
        con.commit()
        metadata = cur.fetchone()
    except Error as error:
        print("Failed:", error)
    print(metadata)
    return metadata

