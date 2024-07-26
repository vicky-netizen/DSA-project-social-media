class Post:
    def __init__(self, post_id, content, timestamp, likes_count=0, comments_count=0):
        self.post_id = post_id
        self.content = content
        self.timestamp = timestamp
        self.likes_count = likes_count
        self.comments_count = comments_count

class AVLTreeNode:
    def __init__(self, key, post):
        self.key = key
        self.post = post
        self.height = 1
        self.left = None
        self.right = None

class UserPostManager:
    def __init__(self):
        self.root = None

    def _height(self, node):
        if node is None:
            return 0
        return node.height

    def _balance_factor(self, node):
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = max(self._height(y.left), self._height(y.right)) + 1
        x.height = max(self._height(x.left), self._height(x.right)) + 1

        return x

    def _left_rotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = max(self._height(x.left), self._height(x.right)) + 1
        y.height = max(self._height(y.left), self._height(y.right)) + 1

        return y

    def _insert(self, node, key, post):
        if node is None:
            return AVLTreeNode(key, post)

        if key < node.key:
            node.left = self._insert(node.left, key, post)
        else:
            node.right = self._insert(node.right, key, post)

        node.height = max(self._height(node.left), self._height(node.right)) + 1

        balance = self._balance_factor(node)

        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)

        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)

        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def add_post(self, key, post):
        self.root = self._insert(self.root, key, post)

    def _inorder_traversal(self, node, sorted_posts):
        if node is not None:
            self._inorder_traversal(node.left, sorted_posts)
            sorted_posts.append(node.post)
            self._inorder_traversal(node.right, sorted_posts)

    def get_sorted_posts(self):
        sorted_posts = []
        self._inorder_traversal(self.root, sorted_posts)
        return sorted_posts




user_posts_manager = UserPostManager()

#
user_posts_manager.add_post(100, Post("post001", "Hello World!", "2024-05-11 10:00:00", likes_count=5, comments_count=3))
user_posts_manager.add_post(800, Post("post002", "How is everyone doing?", "2024-05-11 11:00:00", likes_count=10, comments_count=7))
user_posts_manager.add_post(120, Post("post003", "Feeling great today!", "2024-05-11 12:00:00", likes_count=40, comments_count=2))

# Retrieving posts in sorted order by likes count
sorted_posts_by_likes = user_posts_manager.get_sorted_posts()
for post in sorted_posts_by_likes:
    print(f"Post ID: {post.post_id}, Likes: {post.likes_count}, Comments: {post.comments_count}, Content: {post.content}")
