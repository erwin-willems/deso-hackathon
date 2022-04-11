""" Example for a stream of posts.
"""
import logging

from modules.deso_stream import DesoPostsStream


def print_post(post):
    """Callback function to print the post"""
    print(
        f"""
---------------------------------------------------------------
{post['PostHashHex']}
---------------------------------------------------------------
{post['Body']}
    """
    )


logging.basicConfig(
    format="%(asctime)s %(levelname)-3s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
    obj_stream_posts = DesoPostsStream()
    obj_stream_posts.process_post_subscribers.append(print_post)
    obj_stream_posts.start()
