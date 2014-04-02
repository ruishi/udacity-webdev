################################################################################
#author: RD Galang
#all the URL routing done here.
################################################################################
from webapp2 import WSGIApplication, Route, SimpleRoute
from webapp2_extras import routes

import rot13.rot13 as rot13
import blog.register as br
import blog.blog as b
import wiki.register as wr
import wiki.wiki as w
import main

app = WSGIApplication([('/', main.MainPage)], debug=True)

r13app = WSGIApplication([(r'/rot13', rot13.Rot13)], debug=True)

blogapp = WSGIApplication([
    routes.RedirectRoute('/blog', b.Blog, name="mainblog", strict_slash=True),
    routes.PathPrefixRoute('/blog', [
        Route('/signup', br.Register),
        Route('/welcome', br.Welcome),
        Route('/login', br.Login),
        Route('/logout', br.Logout),
        Route('/newpost', b.WritePost),
        Route(r'/<blog_id:\d+>', b.Permalink),
        SimpleRoute(r'/(\d+)\.json|/blog/\.json', b.JSONHandler),
        Route('/flush/?', b.FlushCache)
    ])], debug=True)

page_re = r'([a-zA-Z0-9_-]+/?)*'
wikiapp = WSGIApplication([
    routes.PathPrefixRoute('/wiki', [
        Route('/welcome', wr.Welcome),
        Route('/signup', wr.Register),
        Route('/login', wr.Login),
        Route('/logout', wr.Logout),
        SimpleRoute('/_edit/?' + page_re, w.EditPage),
        SimpleRoute('/_history/?' + page_re, w.PageHistory)]),
    ('/wiki/?' + page_re, w.WikiPage),
], debug=True)
