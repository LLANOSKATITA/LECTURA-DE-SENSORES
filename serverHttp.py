#!/usr/bin/python
#from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
#from os import curdir, sep
#from urlparse import urlparse
#from urlparse import urlparse, parse_qs
#PORT_NUMBER = 5000

try:
	from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
except:
	from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
try:
	from urlparse import urlparse
	from urlparse import urlparse, parse_qs
except:
	from urllib.parse import urlparse, parse_qs

import os
port = int(os.environ.get("PORT", 5000))	
PORT_NUMBER = port  

sensor=0
#This class will handles any incoming request from
#the browser
SensorPrimero=0
SensorSegundo=0

def getArguments(path):
	global SensorPrimero,SensorSegundo 
	try:
		print (path)
		query = urlparse(path).query
		query_components = dict(qc.split("=") for qc in query.split("&"))
		print (query_components)
		try:
			SensorPrimero= query_components['sensor']
		except:
			pass
		try:
			SensorSegundo= query_components['sensor1']
		except:
			pass
		
		print (SensorPrimero,SensorSegundo)
		#imsi = query_components["imsi"]
	except:
		print ('No argumentos')
def action(path):
	getArguments(path)
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"
		if self.path.find('?'):
			print (self.path)
			query_components = parse_qs(urlparse(self.path).query)
			#imsi = query_components["imsi"] 
			action(self.path)
			self.path="/index.html"
			#print query_components

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				data=f.read()
				data= data.replace('SensorPrimero',str(SensorPrimero)).replace('SensorSegundo',str(SensorSegundo))
				#self.wfile.write(data)
				#f.close()
				try:
					self.wfile.write(data)
				except:
					self.wfile.write(bytes(data,'UTF-8'))
				f.close()
			return


		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print ('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()
	

