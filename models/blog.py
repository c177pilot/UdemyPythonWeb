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
        """
        Return a list of post objects
        """
        return Post.find_posts_for_blog_id(self.blog_id) #this will return a list of posts objects

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
    def get_blog_from_ID(cls, blog_id): #we won't have access to this 'self' unless we create an object first
        """
        Returns the blog object associated with a blog_id
        """
        blog_dict = Database.find_one(collection='blogs',
                                      query={'blog_id':blog_id})
        return Blog.__dict_to_class(blog_dict)
        # return cls(author = blog_dict['author'],
        #             title = blog_dict['title'],
        #             description = blog_dict['description'],
        #             blog_id = blog_dict['blog_id']
        #            )

    @staticmethod
    def find_author_id(author):
        """
        Returns the blog_id associated to an author name CAVEAT: assumes only one blog_id per author name
        """
        blog_dict = Database.find_one(collection='blogs',
                                      query={'author':author})
        return blog_dict['blog_id'] if blog_dict is not None else None

    @classmethod
    def get_all_blogs(cls):
        """
        Returns a list of blog objects for each blog in the database
        """
        blogs = Database.find(collection='blogs',
                              query={})
        #blogs will be a dictionary of blogs at this point
        return [cls.__dict_to_class(blog) for blog in blogs] #return a list of blog objects

    @classmethod
    def __dict_to_class(cls, dict):
        return cls(author=dict['author'],
                   title=dict['title'],
                   description=dict['description'],
                   blog_id=dict['blog_id']
                   )