#!/usr/bin/env python
import logging
import os
import re
from StringIO import StringIO
import fetch
import transforms
import requests
import json

# getParams from Twisted Server
def imageWork(getParams):       

    #URL for image
    if 'obj' in getParams and "ds" in getParams:  

        # come in through "front-door" with domain name to help enforce XACML policies (as server IP not included)     	
        imgURL = "http://127.0.0.1/fedora/objects/"+getParams['obj'][0]+"/datastreams/"+getParams['ds'][0]+"/content"

    else:
        print "No image URL found! Aborting imageServer API call."        
        imgURL = "http://127.0.0.1/fedora/objects/wayne:WSUDORThumbnails/datastreams/NoPhoto/content"        

    # Fetch a dictionary containing the string buffer representing the image, this is the image binary    
    image_dict = fetch.fetchBuffer(imgURL)      

    # Determine mime and file extension with WSUAPI mimetypeDictionary
    mimeDictURL = "http://digital.library.wayne.edu/WSUAPI-dev?functions[]=mimetypeDictionary&direction=DS2extension&PID={obj}&DS={ds}".format(obj=getParams['obj'][0],ds=getParams['ds'][0])
    r = requests.get(mimeDictURL)
    r_dict = json.loads(r.content)
    image_dict['mime'] = r_dict['mimetypeDictionary']['input_mimetype']
    image_dict['ext'] = r_dict['mimetypeDictionary']['extension']

    # Chain commands together
    for param in getParams:
        if not param:
            continue

        # pull in args, must be present with GET based parameters
        args = getParams[param][0]

        # 1st "command" is instantiated class from transforms.py, consider renaming for clarity
        transformAction = transforms.commands.get(param)
        if not transformAction:
            continue               
        
        image_dict['img_binary'] = transformAction().execute(StringIO(image_dict['img_binary']), args)
    
    return image_dict
    

