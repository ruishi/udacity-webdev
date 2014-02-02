#!/usr/bin/env python
################################################################################
#Lesson 2, Part 2
#author: RD Galang
#An exercise in conserving submitted user data in case of invalid input for
#user convenience.
################################################################################

import re
import webapp2
from handler import BaseHandler

def validusername(username):
    user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return user_re.match(username)

def validpw(pw):
    pw_re = re.compile(r"^.{3,20}$")
    return pw_re.match(pw)

def validemail(email):
    email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    return not email or email_re.match(email)

class Welcome(BaseHandler):
    """Handles '/welcome'. Welcomes user with their username, redirects
    if there is no username value."""
    def get(self):
        username = self.request.get('username')
        """Why check if the username is valid AGAIN after you already did it 
        in signup?! Because just because you have a form doesn't mean that 
        people are using it and they can send junk to your server, so always 
        validate!"""
        if validusername(username):
            self.render('welcome.html', username = username)
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
            self.redirect('/welcome?username=' + username)
        else:
            self.render('signup.html', **signup_params)

app = webapp2.WSGIApplication([('/welcome', Welcome),
                               ('/signup', SignUp)], debug=True)
