#!usr/bin/env python
################################################################################
#author: RD Galang
#Lesson 4
#An exercise in setting/getting cookies as well as cookie and password hashing.
################################################################################
from google.appengine.ext import db
from handler import BaseHandler

class BlogPost(db.Model):
    """Datastore entity holding blog posts"""
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        handle = BaseHandler()
        self._render_post = self.post.replace('\n', '<br>')
        return handle.render_str('post.html', post=self)

class User(db.Model):
    """Datastore entity holding user information"""
    username = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
