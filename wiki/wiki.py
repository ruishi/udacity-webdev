################################################################################
#author: RD Galang
#classes for handling the wiki front page, wiki pages, and wiki edit pages
################################################################################

from utils.handler import BaseHandler
from entities import Page, HistoryItem

class EditPage(BaseHandler):
    def get(self, page_name):
        user = self.check_login_status()
        if not page_name:
            page = Page.get_by_key_name('/')
        else:
            page = Page.get_by_key_name(page_name)
        self.render('wiki_edit.html', page=page, user=user)

    def post(self, page_name):
        user = self.check_login_status() 
        content = self.request.get('content')
        if not page_name:
            page_name='/'
            page = Page(key_name=page_name,
                        content=content,
                        author_id = user.key().id())
            page.put()
            self.redirect('/wiki')
        else:
            page = Page(key_name=page_name,
                        content=content, 
                        author_id = user.key().id())
            page.put()
            self.redirect('/wiki/%s' % page_name)

class WikiPage(BaseHandler):
    def get(self, page_name):
        user = self.check_login_status()
        if not page_name:
            page = Page.get_by_key_name('/')
        else:
            page = Page.get_by_key_name(page_name)

        if not page and page_name:
            self.redirect('/wiki/_edit/%s' % page_name)
        elif not page:
            self.redirect('/wiki/_edit')
        else:
            self.render('wiki.html', user=user, page=page)
