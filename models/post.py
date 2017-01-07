from database import Database
import uuid
import datetime
Database.initialize() #do I have an instance of the Database at this point?

class Post(object):

    def __init__(self, blog_id ,title, content, author, date=None, post_id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.post_id = uuid.uuid4().hex if post_id is None else post_id
        self.created_date = datetime.datetime.utcnow() if date is None else date

    def save_to_mongo(self):
        data = self.__json()
        Database.insert(collection='posts', data=data)

    def __json(self):
        return {
            'blog_id' : self.blog_id,
            'title' : self.title,
            'content' : self.content,
            'author' : self.author,
            'post_id' : self.post_id,
            'created_date' : self.created_date
        }
    @staticmethod
    def find_author(author):
        cursor = Database.find(collection='posts',query={"author" : author})
        return [ post for post in cursor] #return a list of posts

    @classmethod
    def find_post_id(cls, post_id):
        data = Database.find_one(collection='posts', query={"post_id" : post_id}) #I only expect to find one since the 'id' is unique
        return cls(blog_id = data['blog_id'],
                   title = data['title'],
                   content = data['content'],
                   author = data['author'],
                   post_id = data['post_id'],
                   created_date = data['created_date']
                   )

    # @classmethod
    # def find_blog_id(cls, blog_id):
    #     data = Database.find_one(collection='posts', query={"blog_id" : blog_id}) #I only expect to find one since the 'id' is unique
    #     return cls(blog_id = data['blog_id'],
    #                title = data['title'],
    #                content = data['content'],
    #                author = data['author'],
    #                date = data['created_date'],
    #                post_id = data['post_id'])

    @staticmethod
    def find_blog_ids(blog_id):
        cursor = Database.find(collection='posts', query={"blog_id" : blog_id})
        return [ post for post in cursor] #return a list of posts
