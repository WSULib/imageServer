# library
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site
from twisted.internet import reactor, defer
from twisted.internet.task import deferLater
from twisted.web.server import NOT_DONE_YET
from twisted.web import server, resource
from twisted.python import log
import logging
import json

# local
from imageServer.imageServerMain import imageWork
from localConfig import *


'''
Prod: Listening on :61618, reverseproxy in Apache to :80/imageServer
Dev: Listening on :61620, reverseproxy in Apache to :80/imageServer-dev
'''

class imageServerListener(resource.Resource):
	isLeaf = True

	def _delayedImageServer(self,request):
		getParams = request.args

		# send to clerkRouter
		worker = mainRouter()
		image_dict = worker.imageServer(getParams=getParams)

		if image_dict[0] == True:
			# response 
			request.setHeader('Access-Control-Allow-Origin', '*')
			request.setHeader('Access-Control-Allow-Methods', 'GET, POST')
			request.setHeader('Access-Control-Allow-Headers','x-prototype-version,x-requested-with')
			request.setHeader('Access-Control-Max-Age', 2520)                
			request.setHeader('Content-Type', 'image/{mime}'.format(mime=image_dict[1]['mime']))
			request.setHeader('Connection', 'Close')
			request.write(image_dict[1]['img_binary'])
			request.finish()

		else:
			# response 
			request.setHeader('Access-Control-Allow-Origin', '*')
			request.setHeader('Access-Control-Allow-Methods', 'GET, POST')
			request.setHeader('Access-Control-Allow-Headers','x-prototype-version,x-requested-with')
			request.setHeader('Access-Control-Max-Age', 2520)                
			request.setHeader('Content-Type', 'application/json')
			request.setHeader('Connection', 'Close')
			request.write(image_dict[1])
			request.finish()

	def render_GET(self, request):                
		d = deferLater(reactor, .01, lambda: request)
		d.addCallback(self._delayedImageServer)
		return NOT_DONE_YET


class mainRouter:

	# handles image requests
	def imageServer(self,**kwargs):		
		getParams = kwargs['getParams']

		try:
			PILServ_response = imageWork(getParams)
			return (True,PILServ_response)
		except Exception,e:
			print "imageServer call unsuccessful.  Error:",str(e)
			return (False,'{{"imageServerstatus":{exceptionErrorString}}}'.format(exceptionErrorString=json.dumps(str(e))))



# twisted liseners
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':	
	
	# imageServer
	if IMAGESERVER_FIRE == True:
		print "Starting imageServer..."
		reactor.listenTCP(IMAGESERVER_LISTENER_PORT, server.Site(imageServerListener()))	
	
	
	print '''             
	       ____
	  _[]_/____\__n_
	 |_____.--.__()_|
	 |LI  //# \\\    |
	 |    \\\__//    |
	 |     '--'     |
	 '--------------'
	'''
	print "<--WSUDOR_imageServer started-->"

	reactor.run()
