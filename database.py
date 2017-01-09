import pymongo

class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None
    __DB = 'fullstack'

#    def __init__(self): #We do not want an __init__ method because we don't want individual instances of Database, we want Singletons
    @staticmethod
    def initialize():
        # Connection to Mongo DB
        try:
            client = pymongo.MongoClient(Database.URI)
            Database.DATABASE = client[Database.__DB]
            print ("Connected successfully!!!")
        except pymongo.errors.ConnectionFailure:
            print ("Could not connect to MongoDB")

    @staticmethod
    def insert(collection, data):
        return Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        cursor = Database.DATABASE[collection].find(query).limit(2)
        #adding the limit(2) here allowed the find() method to return dictionaries and not cursors.
        return cursor

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)