#!/usr/bin/env python
from __future__ import with_statement

import os
import logging
import urllib2

CACHE_DIR = os.path.sep + os.path.join('tmp', 'imageServer')

import urllib2


def __url(url):
    buf = None
    # improvement - set timeout here for objects not found in fedora
    try:
        buf = opener.open(url)
        return buf.read()
    finally:
        if buf:
            buf.close()

def __cacheFile(url):
    # Doing a basic hash for now, might get more complicated later
    return os.path.join(CACHE_DIR, str(hash(url)))

def __cachedBuffer(url):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    cached = __cacheFile(url)
    if not os.path.exists(cached):
        return None

    with open(cached, 'r') as fd:
        return fd.read()    

def __cacheBuffer(url, data):
    path = __cacheFile(url)
    with open(path, 'w') as fd:
        fd.write(data)

def fetchBuffer(url, cache=True):
    if cache:
        cached = __cachedBuffer(url)
        if cached:
            logging.debug('Cache hit for: %s' % url)                       
            return_dict = {
                "img_binary":cached                
            }
            return return_dict            
        logging.debug('Cache miss for: %s' % url)

    # Fetch image 
    rc = __url(url)
    if cache:
        __cacheBuffer(url, rc)                        
    return_dict = {
                "img_binary":rc                
            }
    return return_dict
    
    

