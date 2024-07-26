import hash
import post
import graph
import likes
from datetime import datetime


hashtable=hash.gethash()


u=input("Give username : ")
p=input("Password : ")

if hash.checkpass(hashtable,u,p):
    while True:
        
        graph2=graph.graph2
        command = input().strip()
        if command == "End":
            break
        
        operation = command.split()
        cmd_type = operation[0]

        if cmd_type == "ShowMyPosts":
            s=post.showpost(u)
            post.printheap(s)

        elif cmd_type == "ShowFollowers":
            l=graph2.show_followers(u)
            print(f"Followers of '{u}': {l}")
            
            
        elif cmd_type == "ShowFollowing":
            l=graph2.show_following(u)
            print(f"Following of '{u}': {l}")
            
            
        elif cmd_type=="See_feed":
            following = graph2.show_following(u)
            postheap1 = post.showpost(following[0])
            for post_heap in following[1:]:
                print(post_heap)
                postheap1.merge_heaps(post.showpost(post_heap))
            post.printheap(postheap1)
            
            
        elif cmd_type == "Showlikes":
            post_heap=post.showpost(u)
            while not post_heap.is_empty():
                post1 = post_heap.pop()
                print(f"Post ID: {post1.post_id}, Liked by:",end="")
                likes.likedby(post1.post_id)
                
        elif cmd_type == "AddPost":
            current_time = datetime.now()
            text=input()
            post1=post.Post(u,"10",text, current_time)
            post.add_post(post1)
        
        elif cmd_type == "Addlike":
            id=int(input("Post to like:"))
            likes.insert_like(id,u)
            likes.likedby(id)
        
        elif cmd_type =="showgraph":
            if u=="sujan":
                graph.showgraph(graph2)
        
else:
    print("wrong password")