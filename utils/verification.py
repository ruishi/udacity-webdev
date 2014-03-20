#!/usr/bin/env python
################################################################################
#Lesson 4
#author: RD Galang
#Handles salting and hashing passwords, cookie hashing, and cookie and 
#password verification.
################################################################################
import re
from Crypto.Random.random import StrongRandom
from Crypto.Hash import SHA256
import secret as secret

def validusername(username):
    user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return user_re.match(username)

def validpw(pw):
    pw_re = re.compile(r"^.{3,20}$")
    return pw_re.match(pw)

def validemail(email):
    email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    return not email or email_re.match(email)

def generate_salt():
    rand = StrongRandom()
    return str(rand.getrandbits(256))

def hashpw(pw, salt=None):
    if not salt:
        salt = generate_salt()
    hasher = SHA256.new()
    hasher.update(salt + pw)
    pw_hash = hasher.hexdigest()
    return pw_hash, salt

def hash_cookie(cookie_val):
    hasher = SHA256.new()
    secretcookie = cookie_val + secret.SECRET
    hasher.update(secretcookie)
    return "%s|%s" % (cookie_val, hasher.hexdigest())

def verify_cookie(cookie):
    if cookie:
        cookie_val = cookie.split('|')[0]
        return cookie == hash_cookie(cookie_val)
    else:
        return False
