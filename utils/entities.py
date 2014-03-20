##################################################################################
#author: RD Galang
#Datastore entities common to all apps
#I either pulled or modeled the class methods in User after Steve Huffman's 
#example code
##################################################################################

from google.appengine.ext import db
from verification import hashpw

class User(db.Model):
    """Datastore entity holding user information"""
    username = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    salt = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def get_by_name(cls, username):
        q = db.GqlQuery('SELECT * '
                        'FROM User '
                        'WHERE username = :1', username )
        return q.get()
    
    @classmethod
    def register(cls, username, password, email = None):
        pw_hash, salt = hashpw(password)
        return User(username = username,
                    pw_hash = pw_hash,
                    salt = salt,
                    email = email)

    @classmethod
    def login(cls, username, password):
        user = cls.get_by_name(username)
        if user:
            salt = user.salt
            correct_hash = user.pw_hash
            new_hash = hashpw(password, salt)[0]
            if correct_hash == new_hash:
                return user
