#!usr/bin/env python
################################################################################
#author: RD Galang
#Lesson 3
#An exercise in using google's datastore as well as more complex URL handling
#TODO: -Add error for leaving content and title blank in WritePost
#      -Add error if post does not exist in Post
################################################################################

import webapp2
from handler import BaseHandler

from google.appengine.ext import db

class Blog(BaseHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC LIMIT 10")
        self.render('blog.html', posts=posts)

    def post(self):
        pass

class WritePost(BaseHandler):
    def get(self):
        self.render('newpost.html')

    def post(self):
        title = self.request.get('subject')
        post = self.request.get('content')

        blogpost = BlogPost(title=title, 
                            post=post)

        blogpost.put()
        self.redirect('/blog/%s' % str(blogpost.key().id()))

class Post(BaseHandler):
    def get(self, blog_id):
        blog_id = int(blog_id)
        self.render('permalink.html', post=BlogPost.get_by_id(blog_id))

class BlogPost(db.Model):
    """Datastore entity holding blog posts"""
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        handle = BaseHandler()
        self._render_post = self.post.replace('\n', '<br>')
        return handle.render_str('post.html', post=self)

app = webapp2.WSGIApplication([(r'/blog/?', Blog),
                               (r'/blog/newpost', WritePost),
                               (r'/blog/(\d+)', Post)], debug=True)
