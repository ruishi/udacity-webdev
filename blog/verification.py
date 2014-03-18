#!/usr/bin/env python
################################################################################
#Lesson 4
#author: RD Galang
#Handles salting and hashing passwords, cookie hashing, and cookie and 
#password verification.
################################################################################
from Crypto.Random.random import StrongRandom
from Crypto.Hash import SHA256
import utils.secret as secret
from entities import User

def generate_salt():
    rand = StrongRandom()
    return str(rand.getrandbits(256))

def hashpw(pw, salt=None):
    if not salt:
        salt = generate_salt()
    hasher = SHA256.new()
    hasher.update(salt + pw)
    pw_hash = hasher.hexdigest()
    return pw_hash, salt

def hash_cookie(cookie_val):
    hasher = SHA256.new()
    secretcookie = cookie_val + secret.SECRET
    hasher.update(secretcookie)
    return "%s|%s" % (cookie_val, hasher.hexdigest())

def verify_cookie(cookie):
    if cookie:
        cookie_val = cookie.split('|')[0]
        return cookie == hash_cookie(cookie_val)
    else:
        return False

class CookieAuthentication():
    def authenticate(self, cookie):
        """Checks for and verifies session cookie

        Keyword arguments:
        cookie -- user_id cookie
        
        Returns User object if a user is logged in 
        or None if no user is logged in"""

        if cookie and verify_cookie(cookie):
            user_id = int(cookie.split('|')[0])
            user = User.get_by_id(user_id)
            return user
        return None

class UserAuthentication():
    """Handles user authentication based on uesrname and password"""

    def authenticate(self, user, password):
        """Verifies password against password hash in database.

        Keyword arguments:
        user - User datastore object
        password - password entered by user

        Returns bool"""
        salt = user.salt
        correct_hash = user.pw_hash
        new_hash = hashpw(password, salt)[0]
        return correct_hash == new_hash

