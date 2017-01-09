from models.blog import Blog

class Menu(object):

    def __init__(self):
        self.user_blog = None
        self.user = input("Enter your author name: ")

        if self._user_has_account():
            print("Welcome back {}".format(self.user))
        else:
            self._setup_new_user()

    def _user_has_account(self):
        """
        This method will return True if a user exists and set the self.user_blog object for the user if the user exists.
        Otherwise the method will return False
        :return:
        """
        blog_id = Blog.find_author_id(self.user)
        if blog_id is not None:
            self.user_blog = Blog.get_blog_from_ID(blog_id)
            return True
        else:
            return False

    def _setup_new_user(self):
        """
        This prompts for the user for info required to setup a new account,
        adds the account to the database, and sets the self.user_blog to the users new blog
        :return:
        """
        title = input("Enter title for the new blog: ")
        description = input("Enter the description of the blog: ")
        self.user_blog = Blog(author=self.user,
                    title=title,
                    description=description)
        self.user_blog.save_to_mongo() #seems like the blog class should do this itself on create of a new blog

    def run_menu(self):
        """
        Allows the user to Read or Write blogs
        :return: True unless the user elects to Quit then returns False
        """
        rtnVal = True
        read_or_write = input("Do you want to (R)ead blogs, (W)rite blogs, or (Q)uit? ")
        if read_or_write == 'R':
            self._list_blogs()
            self._view_posts()
        elif read_or_write == 'W':
            self.user_blog.new_post()
        elif read_or_write =='Q':
            print("Thank you for blogging!")
            rtnVal = False
        else:
            print("I did not recognize the input, please try again.")
            self.run_menu()

        return rtnVal

    def _list_blogs(self):
        blog_list = Blog.get_all_blogs()
        for blog in blog_list:
            self.__print_blog(blog)

    def _view_posts(self):
        blog_to_see = input("Enter the blog_id you'd like to see: ")
        blog = Blog.get_blog_from_ID(blog_to_see) #get a blog associated with this blog_id
        posts = blog.get_posts() #get a list of all Post() objects in that blog
        if posts is not None:
            for post in posts:
                print("Date: {}\nTitle: {}\nContent: {}\n\n".format(post.created_date,
                                                       post.title, post.content))
        else:
            print("No posts found")


    def __print_blog(self,blog):
        print("blog_id: {}".format(blog.blog_id))
        print("Title: {}".format(blog.title))
        print("Author: {}".format(blog.author))
        print("Description: {}".format(blog.description))
        print("\n")
