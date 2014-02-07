#!usr/bin/env python
################################################################################
#author: RD Galang
#Lesson 3
#An exercise in using google's datastore as well as more complex URL handling
################################################################################

import webapp2
from handler import BaseHandler

from google.appengine.ext import db

class Blog(BaseHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC")
        self.render('blog.html', posts=posts)

    def post(self):
        pass

class WritePost(BaseHandler):
    def get(self):
        self.render('newpost.html')

    def post(self):
        title = self.request.get('title')
        post = self.request.get('post')

        blogpost = BlogPost(title=title, 
                            post=post,
                            permalink='1')

        blogpost.put()
        self.redirect('/blog')

class BlogPost(db.Model):
    """Datastore entity holding blog posts"""
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    permalink = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add = True)

app = webapp2.WSGIApplication([('/blog', Blog),
                               ('/blog/newpost', WritePost)], debug=True)
