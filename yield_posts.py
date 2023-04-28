""" Example to get a batch of posts from the DeSo blockchain
"""
import logging

from modules.deso_v2 import Posts


def get_posts(num_to_fetch=10, last_post_hash=""):
    """Get posts from DeSo blockchain
    Arguments:
        last_post_hash: Hash of last post to use as pointer (default "")
    Returns:
        list: List of posts in JSON format
    """
    post_list = []
    try:
        posts = Posts.getPostsStateless(
            postHash=last_post_hash, numToFetch=num_to_fetch, orderBy="newest"
        )
    except Exception:  # pylint: disable=broad-except
        logging.error("get_posts: Failed to read posts from blockchain")
        return None
    if "PostsFound" not in posts:
        return None
    if posts["PostsFound"] is None:
        return None
    for post in posts["PostsFound"]:
        if post.get("Body", None) and post["Body"] != "" and "PostHashHex" in post:
            post_list.append(post)
    return post_list


def yield_posts():
    last_post_hash = ""
    while True:
        posts = get_posts(num_to_fetch=1000, last_post_hash=last_post_hash)
        for post in posts:
            yield post
            last_post_hash = post['PostHashHex']

if __name__ == "__main__":
    for my_post in yield_posts():
        print("----------------------------")
        print(my_post["Body"])
