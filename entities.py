#!usr/bin/env python
################################################################################
#author: RD Galang
#Lessons 3, 4
#An exercise in setting/getting cookies as well as cookie and password hashing.
################################################################################
from google.appengine.ext import db
from handler import BaseHandler
import json
import datetime

class BlogPost(db.Model):
    """Datastore entity holding blog posts"""
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        handle = BaseHandler()
        self._render_post = self.post.replace('\n', '<br>')
        return handle.render_str('post.html', post=self)

    def to_json(self):
        post_dict = {}
        post_dict['subject'] = self.title
        post_dict['content'] = self.post
        post_dict['created'] = self.format_time('%a %b %d %I:%M%p %Y')
        return json.dumps(post_dict)

    def format_time(self, fmt):
        return self.created.strftime(fmt)
class User(db.Model):
    """Datastore entity holding user information"""
    username = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    salt = db.StringProperty(required = True)
    email = db.StringProperty()
