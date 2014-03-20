################################################################################
#author: RD Galang
#general signup class to allow signup to multiple apps. This is pretty much
#verbatim from Steve Huffman's solution, which was way better than my original
#one. Note, I'm fairly positive that solution was never pushed to this repo.
################################################################################

from verification import validusername, validemail, validpw
from handler import BaseHandler
from entities import User

class Signup(BaseHandler):
    """Handles '/signup'. Form ensures a valid username, password and ensures 
    both password entries match."""
    def get(self):
        self.render('signup.html')

    def post(self):
        self.username = self.request.get("username")
        self.password = self.request.get("password")
        self.verify = self.request.get("verify")
        self.email = self.request.get("email")
        
        self.signup_params = dict(username = self.username, email = self.email)
        form_error = False

        if not validusername(self.username):
            self.signup_params['uname_error'] = "That's not a valid username!"
            form_error = True
        if not validemail(self.email):
            self.signup_params['email_error'] = "That's not a valid email!"
            form_error = True
        if not validpw(self.password):
            self.signup_params['pw_error'] = "That's not a valid password!"
            form_error = True
        elif self.password != self.verify:
            self.signup_params['verify_error'] = "Your passwords don't match!"
            form_error = True

        if form_error:
            self.render('signup.html', **self.signup_params)
        else:
            user = User.get_by_name(self.username)
            if user:
                self.signup_params['uname_error'] = "That username already exists"
                self.render('signup.html', **self.signup_params)
            else:
                new_user = User.register(self.username, self.password, self.email)
                new_user.put()
                self.set_login_cookie(new_user)
                self.done()
            
    def done(self):
        raise NotImplementedError
