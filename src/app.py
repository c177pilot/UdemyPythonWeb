from models.blog import Blog
import pprint

#create a blog for an author
blog = Blog(author='blog author',
            title='blog title',
            description='blog description')

blog.save_to_mongo() #update the database of blog for this author

blog.new_post() #create a new post for the blog


from_database = Blog.get_from_mongo(blog.blog_id)
print(from_database)

pprint.pprint(blog.get_posts())
