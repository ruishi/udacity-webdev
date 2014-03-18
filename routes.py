################################################################################
#author: RD Galang
#all the URL routing done here.
################################################################################

from webapp2 import WSGIApplication

import rot13.rot13 as rot13
import blog.register as r
import blog.blog as b
import main

app = WSGIApplication([('/', main.MainPage)], debug=True)
r13app = WSGIApplication([(r'/rot13', rot13.Rot13)], debug=True)
blogapp = WSGIApplication([(r'/blog/welcome', r.Welcome),
                           (r'/blog/signup', r.SignUp),
                           (r'/blog/login', r.Login),
                           (r'/blog/logout', r.Logout),
                           (r'/blog/?', b.Blog),
                           (r'/blog/newpost', b.WritePost),
                           (r'/blog/(\d+)', b.Permalink),
                           (r'/blog/(\d+)\.json|/blog/\.json', b.JSONHandler),
                           (r'/blog/flush/?', b.FlushCache)], debug=True)
