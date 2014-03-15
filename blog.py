#!usr/bin/env python
################################################################################
#author: RD Galang
#Lessons 3,4
#An exercise in using google's datastore as well as more complex URL handling
#and cookies
#TODO: 
################################################################################
import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db
import json
import logging, time

from handler import BaseHandler
from entities import BlogPost, User
from verification import CookieAuthentication

def get_latest(update = False):
    posts = memcache.get('latest')
    if not posts or update:
        logging.info("hit the DB")
        posts = db.GqlQuery('SELECT * '
                            'FROM BlogPost '
                            'ORDER BY created '
                            'DESC LIMIT 10')
        posts = list(posts)
        memcache.set('latest', posts)
        memcache.set('lastquery:blog', time.time())
    return posts

class Blog(BaseHandler):
    def get(self):
        posts = get_latest()
        cookie = self.get_cookie('user_id')
        if cookie:
            authenticator = CookieAuthentication()
            user = authenticator.authenticate(cookie)
        else:
            user = None
        seconds = '{0:.2f}'.format(time.time() - memcache.get('lastquery:blog'))
        self.render('blog.html', posts=posts, user=user, seconds=seconds)

class WritePost(BaseHandler):
    def get(self):
        cookie = self.get_cookie('user_id')
        if cookie:
            authenticator = CookieAuthentication()
            user = authenticator.authenticate(cookie)
        else:
            user = None
        if user:
            self.render('newpost.html', user=user)
        else:
            self.render('newpost.html', 
                        user=user, 
                        error="You must be logged in to post")

    def post(self):
        title = self.request.get('subject')
        post = self.request.get('content')

        cookie = self.get_cookie('user_id')
        authenticator = CookieAuthentication()
        user = authenticator.authenticate(cookie)
        if not title or not post:
            self.render('newpost.html', 
                        title=title,
                        post=post,
                        user=user,
                        error="A post requires both a title and content.")
        else: 
            blogpost = BlogPost(title=title, 
                                post=post,
                                author_id=user.key().id())

            blogpost.put()
            get_latest(True)
            self.redirect('/blog/%s' % str(blogpost.key().id()))
            
class Post(BaseHandler):
    def get(self, blog_id):
        blog_id = int(blog_id)
        post = self.get_post(blog_id)
        cookie = self.get_cookie('user_id')
        if cookie:
            authenticator = CookieAuthentication()
            user = authenticator.authenticate(cookie)
        else:
            user = None
        querykey = 'lastquery:%s' % blog_id
        seconds = '{0:.2f}'.format(time.time() - memcache.get(querykey))
        self.render('permalink.html', 
                    post=post, 
                    user=user,
                    seconds=seconds)

    def get_post(self, blog_id):
        post = memcache.get('post:%s' % blog_id)
        if not post:
            post = BlogPost.get_by_id(blog_id)
            memcache.set('post:%s' % blog_id, post)
            memcache.set('lastquery:%s' % blog_id, time.time())
        return post
                
                
class JSONHandler(BaseHandler):
    def get(self, blog_id = None):
        self.response.headers['Content-Type'] = 'application/json'
        if blog_id:
            blog_id = int(blog_id)
            post = BlogPost.get_by_id(blog_id)
            self.write(post.to_json())
        else:
            query = "SELECT * FROM BlogPost ORDER BY created DESC LIMIT 10"
            posts = db.GqlQuery(query)
            posts = list(posts)
            self.write(json.dumps([post.to_json() for post in posts]))

class FlushCache(BaseHandler):
    def get(self):
        memcache.flush_all()
        self.redirect('/blog')


app = webapp2.WSGIApplication([(r'/blog/?', Blog),
                               (r'/blog/newpost', WritePost),
                               (r'/blog/(\d+)', Post),
                               (r'/blog/(\d+)\.json|/blog/\.json', JSONHandler),
                               (r'/blog/flush/?', FlushCache)], debug=True)
