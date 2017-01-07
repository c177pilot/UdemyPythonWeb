from models.blog import Blog
import pprint

blog = Blog(author='blog author',
            title='blog title',
            description='blog description')

blog.new_post()

blog.save_to_mongo() #why is this needed if the new_post method

from_database = Blog.get_from_mongo(blog.blog_id)
print(from_database)

pprint.pprint(blog.get_posts())
