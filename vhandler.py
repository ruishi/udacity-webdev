#!/usr/bin/env python
################################################################################
#Lesson 4
#author: RD Galang
#Handles salting and hashing passwords, cookie hashing, and cookie and 
#password verification.
################################################################################

from Crypto.Random.random import StrongRandom
from Crypto.Hash import SHA256

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

def verifypw(correct_hash, salt, pw):
    new_hash = hashpw(pw, salt)[0]
    return correct_hash == new_hash

def hash_cookie(cookie_val):
    hasher = SHA256.new()
    hasher.update(cookie_val)
    return "%s|%s" % (cookie_val, hasher.hexdigest())

def verify_cookie(cookie):
    if cookie:
        cookie_val = cookie.split('|')[0]
        return cookie == hash_cookie(cookie_val)
    else:
        return False

