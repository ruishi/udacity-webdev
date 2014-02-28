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

class JSONHandler(BaseHandler):
    def get(self, blog_id = None):
        self.response.headers['Content-Type'] = 'application/json'
        if blog_id:
            blog_id = int(blog_id)
            post = BlogPost.get_by_id(blog_id)
            self.write(post.to_json())
        else:
            posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC LIMIT 10")
            blog_list = []
            for post in posts:
                blog_list.append(post.to_json())
            self.write(json.dumps(blog_list))


app = webapp2.WSGIApplication([(r'/blog/?', Blog),
                               (r'/blog/newpost', WritePost),
                               (r'/blog/(\d+)', Post),
                               (r'/blog/(\d+)\.json|/blog/\.json', JSONHandler)], debug=True)
