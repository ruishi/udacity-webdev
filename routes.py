################################################################################
#author: RD Galang
#all the URL routing done here.
################################################################################

from webapp2 import WSGIApplication

import rot13.rot13 as rot13
import blog.register as br
import blog.blog as b
import wiki.register as wr
import wiki.wiki as w
import main

app = WSGIApplication([('/', main.MainPage)], debug=True)

r13app = WSGIApplication([(r'/rot13', rot13.Rot13)], debug=True)

blogapp = WSGIApplication([(r'/blog/welcome', br.Welcome),
                           (r'/blog/signup', br.Register),
                           (r'/blog/login', br.Login),
                           (r'/blog/logout', br.Logout),
                           (r'/blog/?', b.Blog),
                           (r'/blog/newpost', b.WritePost),
                           (r'/blog/(\d+)', b.Permalink),
                           (r'/blog/(\d+)\.json|/blog/\.json', b.JSONHandler),
                           (r'/blog/flush/?', b.FlushCache)], debug=True)

wikiapp = WSGIApplication([(r'/wiki/?', w.Front),
                           (r'/wiki/welcome', wr.Welcome),
                           (r'/wiki/signup', wr.Register),
                           (r'/wiki/login', wr.Login),
                           (r'/wiki/logout', wr.Logout)], debug=True)
