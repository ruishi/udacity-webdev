################################################################################
#author: RD Galang
#Wiki-specific datastore entities
################################################################################

from google.appengine.ext import db
from utils.entities import User
import time;

class Page(db.Model):
    """Datastore entity for wiki pages"""
    page_name = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    author_id = db.IntegerProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class HistoryItem(db.Model):
    """Datastore entity for wiki page histories"""
    page_name = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    creation_date = db.DateTimeProperty(required = True)
    author_id = db.IntegerProperty(required = True)

    @classmethod
    def get_by_page_name(cls, page_name):
        q = cls.gql('WHERE page_name = :1 '
                    'ORDER BY creation_date DESC', page_name)
        return list(q)

    def get_author(self):
        user = User.get_by_id(self.author_id)
        return user.username

    def format_date(self):
        return self.creation_date.strftime('%m/%d/%Y %H:%M:%S')
