################################################################################
#author: RD Galang
#Wiki-specific datastore entities
################################################################################

from google.appengine.ext import db

class Page(db.Model):
    """Datastore entity for wiki pages"""
    content = db.TextProperty(required = True)
    author_id = db.IntegerProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class HistoryItem(db.Model):
    """Datastore entity for wiki page histories"""
    page_name = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    creation_date = db.DateTimeProperty(required = True)
    author_id = db.IntegerProperty(required = True)
