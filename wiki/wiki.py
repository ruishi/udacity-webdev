################################################################################
#author: RD Galang
#classes for handling the wiki front page, wiki pages, and wiki edit pages
################################################################################

from utils.handler import BaseHandler

class Front(BaseHandler):
    def get(self):
        self.render('wiki.html');
