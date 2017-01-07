from database import Database
import uuid
import datetime
Database.initialize() #do I have an instance of the Database at this point?

class Post(object):

    def __init__(self, blog_id ,title, content, author, date=None, id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.id = uuid.uuid4().hex if id is None else id
        self.created_date = datetime.datetime.utcnow() if date is None else date

    def save_to_mongo(self):
        data = self.__json()
        Database.insert(collection='posts', data=data)

    def __json(self):
        return {
            'id' : self.id,
            'blog_id' : self.blog_id,
            'author' : self.author,
            'content' : self.content,
            'title' : self.title,
            'created_date' : self.created_date
        }
    @staticmethod
    def find_author(author):
        cursor = Database.find(collection='posts',query={"author" : author})
        return [ post for post in cursor] #return a list of posts

    @staticmethod
    def find_uuid(id):
        return Database.find_one(collection='posts', query={"id" : id}) #I only expect to find one since the 'id' is unique
        # return cls(blog_id = data['blog_id'],
        #            title = data['title'],
        #            content = data['content'],
        #            author = data['author'],
        #            date = data['date'],
        #            id = data['id'])

    @staticmethod
    def find_blog_ids(id):
        cursor = Database.find(collection='posts', query={"blog_id" : id})
        return [ post for post in cursor] #return a list of posts
