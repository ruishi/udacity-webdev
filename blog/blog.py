################################################################################
#author: RD Galang
#Lessons 3,4
#An exercise in using google's datastore as well as more complex URL handling
#and cookies
#TODO: 
################################################################################
from google.appengine.api import memcache
from google.appengine.ext import db
import json
import logging, time

from utils.handler import BaseHandler
from entities import BlogPost, User

def get_latest(update = False):
    key = 'latest'
    query_key = 'lastquery:blog'
    posts = memcache.get(key)
    if not posts or update:
        posts = db.GqlQuery('SELECT * '
                            'FROM BlogPost '
                            'ORDER BY created '
                            'DESC LIMIT 10')
        posts = list(posts)
        memcache.set(key, posts)
        memcache.set(query_key, time.time())
    return posts

class Blog(BaseHandler):
    def get(self):
        query_key = 'lastquery:blog'
        posts = get_latest()
        user = self.check_login_status()
        querytime = memcache.get(query_key)
        if querytime:
            seconds = '{0:.2f}'.format(time.time() - memcache.get(query_key))
        else:
            seconds = 0
        self.render('blog.html', posts=posts, user=user, seconds=seconds)

class WritePost(BaseHandler):
    def get(self):
        user = self.check_login_status()
        if user:
            self.render('newpost.html', user=user)
        else:
            self.render('newpost.html', 
                        user=user, 
                        error="You must be logged in to post")

    def post(self):
        user = self.check_login_status()
 
        title = self.request.get('subject')
        post = self.request.get('content')
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
            
class Permalink(BaseHandler):
    def get(self, blog_id):
        blog_id = int(blog_id)
        post = self.get_post(blog_id)
        user = self.check_login_status()
        query_key = 'lastquery:%s' % blog_id
        seconds = '{0:.2f}'.format(time.time() - memcache.get(query_key))
        self.render('permalink.html', 
                    post=post, 
                    user=user,
                    seconds=seconds)

    def get_post(self, blog_id):
        perma_key = 'post:%s' % blog_id
        query_key = 'lastquery:%s' % blog_id
        post = memcache.get(perma_key)
        if not post:
            post = BlogPost.get_by_id(blog_id)
            memcache.set(perma_key, post)
            memcache.set(query_key, time.time())
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
