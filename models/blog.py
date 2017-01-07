import uuid
from models.post import Post
from database import Database
from datetime import datetime

class Blog(object):

    def __init__(self,author, title, description, blog_id=None):
        self.author = author
        self.title = title
        self.description = description
        self.blog_id = uuid.uuid4().hex if blog_id is None else blog_id

    def new_post(self):
        title = input("Enter blog title: ")
        content = input("Enter blog content: ")
        date = input("Enter date in ddmmYYYY format or leave blank for today: ")
        post = Post(blog_id=self.blog_id,
                    title=title,
                    content=content,
                    author=self.author,
                    date=datetime.utcnow() if date is '' else datetime.strptime(date,"%d%m%Y")
                    )
        post.save_to_mongo() #create a post with the blog_id referencing back to the blogs collection via the blog_id

    def get_posts(self): #return list of posts that are associated with this blog_id
        return Post.find_blog_ids(self.blog_id) #this will return a list of posts

    def save_to_mongo(self):
        data = self.__json()
        Database.insert(collection='blogs', data=data)

    def __json(self):
        return {
            'author':self.author,
            'title':self.title,
            'description':self.description,
            'blog_id':self.blog_id
        }

    @classmethod
    def get_from_mongo(cls,blog_id): #we won't have access to this 'self' unless we create an object first
        blog_data = Database.find_one(collection='blogs',
                                      query={'blog_id':blog_id})
        return cls(author = blog_data['author'],
                    title = blog_data['title'],
                    description = blog_data['description'],
                    blog_id = blog_data['blog_id']
                   )
