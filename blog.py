#!usr/bin/env python
################################################################################
#author: RD Galang
#Lessons 3,4
#An exercise in using google's datastore as well as more complex URL handling
#and cookies
#TODO: -Add error for leaving content and title blank in WritePost
#      -Add error if post does not exist in Post
################################################################################

import webapp2
from handler import BaseHandler
from entities import BlogPost, User
import json

from google.appengine.ext import db
import register

class Blog(BaseHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC LIMIT 10")
        user_cookie = self.get_cookie('user_id')
        self.render('blog.html', 
                    posts=posts, 
                    user=register.get_user(user_cookie))

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
        user_cookie = self.get_cookie('user_id')
        self.render('permalink.html', 
                    post=BlogPost.get_by_id(blog_id), 
                    user=register.get_user(user_cookie))

class JSONHandler(BaseHandler):
    def get(self, blog_id = None):
        self.response.headers['Content-Type'] = 'application/json'
        if blog_id:
            blog_id = int(blog_id)
            post = BlogPost.get_by_id(blog_id)
            self.write(post.to_json())
        else:
            posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC LIMIT 10")
            posts = list(posts)
            self.write(json.dumps([post.to_json() for post in posts]))


app = webapp2.WSGIApplication([(r'/blog/?', Blog),
                               (r'/blog/newpost', WritePost),
                               (r'/blog/(\d+)', Post),
                               (r'/blog/(\d+)\.json|/blog/\.json', JSONHandler)], debug=True)
