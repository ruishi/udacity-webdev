################################################################################
#Lesson 2, Part 2
#author: RD Galang
#An exercise in conserving submitted user data in case of invalid input for
#user convenience.
################################################################################
import re
from google.appengine.ext import db
from utils.handler import BaseHandler
from entities import User
import utils.verification as v

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
        user = self.check_login_status()
        if user:
            self.render('welcome.html', user = user)
        else:
            self.redirect('/blog/signup')

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
            pw_hash, salt = v.hashpw(password)
            if email:
                new_user = User(username = username,
                                pw_hash = pw_hash, 
                                salt = salt, 
                                email = email)
            else:
                new_user = User(username = username, 
                                pw_hash = pw_hash, 
                                salt = salt)
            new_user.put()
            user_id = str(new_user.key().id())
            self.set_cookie(user_id=v.hash_cookie(user_id))
            self.redirect('/blog/welcome')
        else:
            self.render('signup.html', **signup_params)

class Login(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        user = db.GqlQuery("SELECT * FROM User where username = :1", 
                           username).get()
        if user:
            authenticator = UserAuthentication()
            if authenticator.authenticate(user, password): 
                user_id = str(user.key().id())
                self.set_cookie(user_id=v.hash_cookie(user_id))
                self.redirect('/blog/welcome')
            else:
                self.render('login.html', 
                            error="Incorrect password.", 
                            username = username)
        else:
            self.render('login.html', 
                        error="Incorrect username.", 
                        username = username)

class Logout(BaseHandler):
    def get(self):
        self.set_cookie(user_id="")
        self.redirect('/blog/login')
