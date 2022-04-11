""" Get posts from database and blockchain
"""
import logging
import sqlite3

from modules.deso_v2 import Posts


def __db_connect(database_name="data/posts.db"):
    """create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(database=database_name, timeout=30)
    except sqlite3.Error as sql_error:
        logging.error(f"PostProcessor: db_connect: {sql_error}")
        return None
    return conn


def __close_db(conn):
    """Close the database connection"""
    conn.close()


def get_post_from_deso(post_hash):
    """Get post from the DeSo blockchain"""
    try:
        post = Posts.getPostInfo(postHash=post_hash)
    except Exception:  # pylint: disable=broad-except
        logging.error("get_posts: Failed to read posts from blockchain")
        return None
    if "PostFound" not in post or post["PostFound"] is None:
        return None
    return post["PostFound"]


def get_post_hash_from_db(db_query):
    """Get posts from database based on query"""
    db_connection = __db_connect()
    if not db_connection:
        return None
    posts = []
    for row in db_connection.execute(db_query):
        post_hash = row[0]
        post = get_post_from_deso(post_hash)
        if post:
            posts.append(post)
    __close_db(db_connection)
    return posts


if __name__ == "__main__":
    QUERY = "SELECT posthash FROM filterreason LIMIT 10;"
    my_posts = get_post_hash_from_db(QUERY)
    for my_post in my_posts:
        if "Body" not in my_post:
            continue
        print(my_post["Body"])
