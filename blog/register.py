################################################################################
#Lesson 2, Part 2
#author: RD Galang
#An exercise in conserving submitted user data in case of invalid input for
#user convenience.
################################################################################
from google.appengine.ext import db
from utils.handler import BaseHandler
from utils.entities import User
from utils.registration import Signup
        
class Welcome(BaseHandler):
    """Handles '/welcome'. Welcomes user with their username, redirects
    if there is no username value."""
    def get(self):
        user = self.check_login_status()
        if user:
            self.render('welcome.html', user = user)
        else:
            self.redirect('/blog/signup')

class Register(Signup):
    def done(self):
        user = User.get_by_name(self.username)
        if user:
            self.signup_params['uname_error'] = "That username already exists"
            self.render('signup.html', **self.signup_params)
        else:
            new_user = User.register(self.username, self.password, self.email)
            new_user.put()
            self.set_login_cookie(new_user)
            self.redirect('/blog/welcome')


class Login(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        user = User.login(username, password)
        if user:
            self.set_login_cookie(user)
            self.redirect('/blog/welcome')
        else:
            self.render('login.html', 
                        error="Incorrect username or password.", 
                        username = username)

class Logout(BaseHandler):
    def get(self):
        self.set_cookie(user_id="")
        self.redirect('/blog/login')
