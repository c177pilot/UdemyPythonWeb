from models.post import Post
import pprint
#from models.blog import Blog
import datetime

"""
blog = Blog(author='blog author',
            title='blog title',
            description='blog description')

blog.new_post()

#blog.save_to_mongo() #why is this needed if the new_post method

from_database = Blog.get_from_mongo(blog.id)
print(blog.get_posts())
"""


#create an instance of a post
post = Post(blog_id="123",title="Still not working",content="this is some content",author="jose")
post.save_to_mongo()

print("finding my own author")
print(post.author)

print("finding my own uuid")
print(post.id)

print("find my own UUID in the Database")
uuid_post = Post.find_uuid(post.id)
pprint.pprint(uuid_post)

print("find all entries that match my author in the Database")
author_post = Post.find_author(post.author)
pprint.pprint(author_post)

print("find all entries that match my own blog_ID in the Database")
blog_ID = Post.find_blog_ids(post.blog_id)
pprint.pprint(blog_ID)