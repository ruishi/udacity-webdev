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

page_re = r'([a-zA-Z0-9_-]+/?)*'
wikiapp = WSGIApplication([(r'/wiki/welcome', wr.Welcome),
                           (r'/wiki/signup', wr.Register),
                           (r'/wiki/login', wr.Login),
                           (r'/wiki/logout', wr.Logout),
                           (r'/wiki/_edit/?' + page_re, w.EditPage), 
                           (r'/wiki/?' + page_re, w.WikiPage)],
                          debug=True)
