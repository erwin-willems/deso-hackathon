"""Stream and process posts from the DeSo Blockchain
"""
import time
import logging
import threading
from modules.deso_v2 import Posts

class DesoPostsStream:
    """Stream posts from DeSo blockchain
    """
    def __init__(self):
        self.process_post_subscribers = []
        self.post_watch_window = 10
        self.hashlist_size = 20

    def get_posts(self, last_post_hash = ""):
        """Get posts from DeSo blockchain
            Arguments:
                last_post_hash: Hash of last post to use as pointer (default "")
            Returns:
                list: List of posts in JSON format
        """
        post_list = []
        num_to_fetch = self.post_watch_window
        try:
            posts = Posts.getPostsStateless(postHash=last_post_hash, numToFetch=num_to_fetch, orderBy="newest")
        except:
            logging.error("get_posts: Failed to read posts from blockchain")
            return None
        if 'PostsFound' not in posts:
            return None
        if posts['PostsFound'] is None:
            return None
        for post in posts['PostsFound']:
            if 'Body' in post and post['Body'] != "" and 'PostHashHex' in post:
                post_list.append(post)
        return post_list

    def stream_posts(self):
        """Stream posts from DeSo blockchain
            Arguments:
                None
            Returns:
                None
        """
        hash_list = []
        while True:
            post_list = self.get_posts()
            if post_list is None:
                time.sleep(5)
                continue
            for post in post_list:
                if not "PostHashHex" in post:
                    logging.warn("stream_posts: PostHashHex not found in post")
                    continue
                if post["PostHashHex"] in hash_list:
                    continue
                hash_list.append(post['PostHashHex'])

                # itterate over the callback subscribers
                for subscriber in self.process_post_subscribers:
                    # Run the callback function
                    subscriber(post)
            old_len = len(hash_list)
            while len(hash_list) > self.hashlist_size:
                hash_list.pop(0)
            current_len = len(hash_list)
            if old_len != current_len:
                logging.debug(f"Stream Posts: Cleaned up hash_list: {old_len} -> {current_len}")
            time.sleep(2)

    def start(self):
        """Start the stream in a thread
            Arguments:
                None
            Returns:
                None
        """
        stream_thread = threading.Thread(target=self.stream_posts)
        logging.info("stream start : Start stream thread")
        stream_thread.start()
