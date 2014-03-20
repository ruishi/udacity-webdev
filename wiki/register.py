##################################################################################
#author: RD Galang
#Registration/login/logout pages for wiki. It's pretty much the same as the 
#registration code in blog. The only difference is the redirect. It also uses 
#the same Datastore entity. Currently I'm not sure if I want to create a different
#usertype (by adding a field in user called "type" or "app"). Most sites with
#different services tend to sign you up for all of them if you sign up for one
#(e.g., Google). For now that will be true here as well.
##################################################################################
from utils.registration import Signup
from utils.handler import BaseHandler
from utils.entities import User

class Welcome(BaseHandler):
    def get(self):
        user = self.check_login_status()
        if user:
            self.render('welcome.html', user=user, app="wiki")
        else:
            self.redirect('/wiki/signup')

class Register(Signup):
    def done(self):
        self.redirect('/wiki/welcome')

class Login(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        user = User.login(username, password)
        if user:
            self.set_login_cookie(user)
            self.redirect('/wiki/welcome')
        else:
            self.render('login.html',
                        error="Incorrect username or password.",
                        username = username)

class Logout(BaseHandler):
    def get(self):
        self.set_cookie(user_id="")
        self.redirect('/wiki/login')
