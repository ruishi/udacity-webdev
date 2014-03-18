#!/usr/bin/env python
################################################################################
#author: RD Galang
#Lesson 2, Part 1
#An exercise in retrieving submitted text from a form, manipulating it, and
#posting it to the user.
################################################################################

import string

from utils.handler import BaseHandler

class Rot13(BaseHandler):
    """Handles '/rot13' which creates a rot13 converter."""
    def get(self):
        self.render('rot13.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = self.rot13(text)
        self.render('rot13.html', text = rot13)

    def rot13(self, s):
        final = ""
        upperalpha = string.uppercase
        loweralpha = string.lowercase
        for c in s:
            if c.isalpha():
                if c in upperalpha:
                    c = upperalpha[(upperalpha.find(c) + 13) % 26]
                else:
                    c = loweralpha[(loweralpha.find(c) + 13) % 26]
            final += c
        return final
