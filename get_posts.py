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
        if "Body" in post and post["Body"] != "" and "PostHashHex" in post:
            post_list.append(post)
    return post_list


if __name__ == "__main__":
    my_posts = get_posts()
    for my_post in my_posts:
        if not "Body" in my_post:
            continue
        print("----------------------------")
        print(my_post["Body"])
