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

    @classmethod
    def find_author(cls, author):
        """
        find_author()
        :param author:
        :return: returns a list of Post objects for all posts by the author
        """
        posts = Database.find(collection='posts',query={"author" : author})
        #posts will contain a dictionary of posts by the author
        if posts is not None:
            return [Post.__dict_to_cls(post) for post in posts]
        else:
            return None

    @classmethod
    def find_post_id(cls, post_id):
        """
        :param post_id:
        :return: Post object corresponding to the post_id
        """
        data = Database.find_one(collection='posts', query={"post_id" : post_id}) #I only expect to find one since the 'id' is unique
        if data is not None:
            return Post.__dict_to_cls(data)
        else:
            return None

    @classmethod
    def find_posts_for_blog_id(cls, blog_id):
        """
        :param blog_id:
        :return: Post object with the first match to blog_id
        """
        data = Database.find(collection='posts', query={"blog_id" : blog_id}) #There will be many posts associated with a blog_id
        #data will be a cursor. How do I deal with that?

        if data is not None:
            return [Post.__dict_to_cls(post) for post in data]
        else:
            return None

    def __json(self):
        """
        JSONify's the class objects so they can be put in the dictionary
        :return:
        """
        return {
            'blog_id' : self.blog_id,
            'title' : self.title,
            'content' : self.content,
            'author' : self.author,
            'post_id' : self.post_id,
            'created_date' : self.created_date
        }
    @classmethod
    def __dict_to_cls(cls,dict):
        """
        Returns a Post() object from a dictionary
        :param dict:
        :return:
        """
        if dict is not None:
            return cls(blog_id=dict['blog_id'],
                       title=dict['title'],
                       content=dict['content'],
                       author=dict['author'],
                       date=dict['created_date'],
                       post_id=dict['post_id'])
        else:
            return None