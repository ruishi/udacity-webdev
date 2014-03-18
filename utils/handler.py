#!usr/bin/env python
################################################################################
#author: Steve Huffman/RD Galang
#Steve Huffman's basehandler code, in a separate file for importing into
#other applications
#added by me: set_cookie(), get_cookie()
################################################################################
import os

import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 
                            os.path.pardir,
                            'templates')
jinja_env = jinja2.Environment(loader = 
                               jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class BaseHandler(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def set_cookie(self, **kw):
        formatted_cookie = ';'.join([key + '=' + val 
                                     for key, val in kw.items()])
        self.response.headers.add_header('Set-Cookie', '%s' % formatted_cookie)

    def get_cookie(self, name):
        return self.request.cookies.get(name)

    
