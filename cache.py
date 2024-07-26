import mysql.connector
import pickle
from post import PostHeap, Post
from likes import LinkedList

def fetch_data_from_database():
    # Connect to MySQL database
    db_connection = mysql.connector.connect(
        host='localhost',
        port=3308,
        user='root',
        password='root',
        database='dsa'
    )
    cursor = db_connection.cursor()

    users_posts = {}
    cursor.execute("SELECT username, post_id, contents, time FROM posts")
    rows = cursor.fetchall()
    for row in rows:
        username, post_id, contents, time = row
        if username not in users_posts:
            users_posts[username] = PostHeap()
        users_posts[username].push(Post(username, post_id, contents, time))


    posts_likes = {}
    cursor.execute("SELECT post_id, liked_by FROM likes")
    rows = cursor.fetchall()
    for row in rows:
        post_id, liked_by = row
        if post_id not in posts_likes:
            posts_likes[post_id] = LinkedList()
        posts_likes[post_id].insert(liked_by)

    cursor.close()
    db_connection.close()

    return users_posts, posts_likes

def save_data_to_file(users_posts, posts_likes, filename):
    with open(filename, 'wb') as file:
        pickle.dump((users_posts, posts_likes), file)

def load_data_from_file(filename):
    with open(filename, 'rb') as file:
        users_posts, posts_likes = pickle.load(file)
    return users_posts, posts_likes

# Example usage:
# Fetch data from the database
users_posts, posts_likes = fetch_data_from_database()

print(users_posts,posts_likes)
save_data_to_file(users_posts, posts_likes, 'data_cache.pkl')

# Later, when initializing your program:
# Load data from the file
loaded_users_posts, loaded_posts_likes = load_data_from_file('data_cache.pkl')

def update_database(users_posts, posts_likes):

    db_connection = mysql.connector.connect(
        host='localhost',
        port=3308,
        user='root',
        password='root',
        database='dsa'
    )
    cursor = db_connection.cursor()

    # Update posts in the database
    for username, post_heap in users_posts.items():
        cursor.execute("DELETE FROM posts WHERE username = %s", (username,))
        for post in post_heap.heap:
            insert_query = "INSERT INTO posts (post_id, username, contents, time) VALUES (%s, %s, %s, %s)"
            post_data = (post.post_id, post.username, post.content, post.timestamp)
            cursor.execute(insert_query, post_data)

    # Update likes in the database
    cursor.execute("DELETE FROM likes")
    for post_id, likes_list in posts_likes.items():
        for like_node in likes_list:
            insert_query = "INSERT INTO likes (post_id, liked_by) VALUES (%s, %s)"
            like_data = (post_id, like_node.data)
            cursor.execute(insert_query, like_data)

    # Commit changes and close database connection
    db_connection.commit()
    cursor.close()
    db_connection.close()