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
from verification import CookieAuthentication
import json

from google.appengine.ext import db

class Blog(BaseHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC LIMIT 10")
        cookie = self.get_cookie('user_id')
        if cookie:
            authenticator = CookieAuthentication()
            user = authenticator.authenticate(cookie)
        else:
            user = None
        self.render('blog.html', posts=posts, user=user)

class WritePost(BaseHandler):
    def get(self):
        cookie = self.get_cookie('user_id')
        if cookie:
            authenticator = CookieAuthentication()
            user = authenticator.authenticate(cookie)
        else:
            user = None
        self.render('newpost.html', user=user)

    def post(self):
        title = self.request.get('subject')
        post = self.request.get('content')

        cookie = self.get_cookie('user_id')
        authenticator = CookieAuthentication()
        user = authenticator.authenticate(cookie)
        blogpost = BlogPost(title=title, 
                            post=post,
                            author_id=user.key().id())

        blogpost.put()
        self.redirect('/blog/%s' % str(blogpost.key().id()))

class Post(BaseHandler):
    def get(self, blog_id):
        blog_id = int(blog_id)
        cookie = self.get_cookie('user_id')
        if cookie:
            authenticator = CookieAuthentication()
            user = authenticator.authenticate(cookie)
        else:
            user = None
        self.render('permalink.html', 
                    post=BlogPost.get_by_id(blog_id), 
                    user=user)

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
