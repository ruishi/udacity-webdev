#!/usr/bin/env python
################################################################################
#Lesson 2, Part 2
#author: RD Galang
#An exercise in conserving submitted user data in case of invalid input for
#user convenience.
################################################################################

import re
import webapp2
from Crypto.Random.random import StrongRandom
from Crypto.Hash import SHA256
from handler import BaseHandler
from entities import User

def validusername(username):
    user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return user_re.match(username)

def validpw(pw):
    pw_re = re.compile(r"^.{3,20}$")
    return pw_re.match(pw)

def validemail(email):
    email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    return not email or email_re.match(email)

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

def verifypw(correct_hash, pw, salt):
    return correct_hash == hashpw(pw, salt)

def hash_cookie(cookie_val):
    hasher = SHA256.new()
    hasher.update(cookie_val)
    return "%s|%s" % (cookie_val, hasher.hexdigest())

def verify_cookie(cookie):
    if cookie:
        cookie_val = cookie.split('|')[0]
        return cookie == hash_cookie(cookie_val)
    else:
        return False

class Welcome(BaseHandler):
    """Handles '/welcome'. Welcomes user with their username, redirects
    if there is no username value."""
    def get(self):
        id_cookie = self.request.cookies.get('user_id')
        if verify_cookie(id_cookie):
            user_id = int(id_cookie.split('|')[0])
            user = User.get_by_id(user_id)
            self.render('welcome.html', username = user.username)
        else:
            self.redirect('/signup')

class SignUp(BaseHandler):
    """Handles '/signup'. Form ensures a valid username, password and ensures 
    both password entries match."""
    def get(self):
        self.render('signup.html')

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        
        signup_params = dict(username = username, email = email)
        form_error = False

        if not validusername(username):
            signup_params['uname_error'] = "That's not a valid username!"
            form_error = True
        if not validemail(email):
            signup_params['email_error'] = "That's not a valid email!"
            form_error = True
        if not validpw(password):
            signup_params['pw_error'] = "That's not a valid password!"
            form_error = True
        elif password != verify:
            signup_params['verify_error'] = "Your passwords don't match!"
            form_error = True

        if not form_error:
            pw_hash, salt = hashpw(password)
            if email:
                new_user = User(username = username,
                                pw_hash = pw_hash, 
                                salt = str(salt), 
                                email = email)
            else:
                new_user = User(username = username, 
                                pw_hash = pw_hash, 
                                salt = str(salt))
            new_user.put()
            user_id = str(new_user.key().id())
            id_cookie = hash_cookie(user_id)
            self.response.headers.add_header('Set-Cookie', 
                                             'user_id=%s' % id_cookie)
            self.redirect('/welcome')
        else:
            self.render('signup.html', **signup_params)

app = webapp2.WSGIApplication([('/welcome', Welcome),
                               ('/signup', SignUp)], debug=True)
