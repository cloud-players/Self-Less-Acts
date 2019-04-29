from flask import Flask, render_template, request, redirect, abort, jsonify
import threading
import requests
import time, signal, sys
import docker

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
ip = "http://127.0.0.1:"

apis =	['/api/v1/_count',
		'/api/v1/_health',
		'/api/v1/_crash',
		'/api/v1/categories',
		'/api/v1/categories/<categoryName>/acts/size',
		'/api/v1/categories/<categoryName>/acts',
		'/api/v1/categories/<categoryName>',  	
		'/api/v1/acts/count',
		'/api/v1/acts/upvote',
		'/api/v1/acts/<actId>',
		'/api/v1/acts']


app = Flask(__name__)

sem1 = threading.Semaphore()
sem2 = threading.Semaphore()

class roundrobin(object):
	"""docstring for roundrobin"""
	def __init__(self):
		super(roundrobin, self).__init__()
		self.containers = []
		self.next = -1
		self.size = 0
		self.tot_reqs = 0
		self.client = docker.from_env()

	def getnext(self):
		self.next = (self.next + 1) % self.size
		return self.containers[self.next]["port"]

	def startnewcontainer(self, port, idx):
		#self.next = -1
		cont = self.client.containers.run("acts", detach=True, ports={'80/tcp': port}, stop_signal="SIGINT")
		if idx < self.size:
			self.containers[idx] = {'id':cont.id, 'port':port}
		else:
			self.containers.append({'id':cont.id, 'port':port})
		print(self.containers)
		time.sleep(5)
		self.size += 1
		
	def stopcontainer(self, idx):
		self.size -= 1
		self.client.containers.get(self.containers[idx]['id']).stop()
		time.sleep(5)

	def __del__(self):
		print("\ndestroying containers")
		for ii, i in enumerate(self.containers):
			self.stopcontainer(ii)

r = roundrobin()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):
	global r, apis
	path = '/' + path
	if path == "/healthcheck":
		return jsonify(success=True)
	if (path not in apis) or r.size == 0:
		abort(404)
	if ((path != '/api/v1/_health') and (path != '/api/v1/_crash')):
		if (r.tot_reqs == 0):
			sem2.release()
			print("releasing sem2")
		r.tot_reqs += 1
		
	port = r.getnext()
	#return redirect("http://3.210.166.12:"+str(port)+path)
	if request.method == "POST":	
		ret = requests.post(ip+str(port)+path)
	elif request.method == "GET":
		ret = requests.get(ip+str(port)+path)
	else:
		ret = requests.delete(ip+str(port)+path)
	return jsonify(ret.text), ret.status_code


def fun1():
	sem1.acquire()
	sem2.acquire()
	#app.debug=True
	r.startnewcontainer(8000, 0)
	sem1.release()
	#app.run(host='0.0.0.0', port=80)

	http_server = HTTPServer(WSGIContainer(app))
	http_server.listen(80)
	IOLoop.instance().start()


def fun2():
	sem1.acquire()
	print("sem1 acquired by fun2")
	i = 1
	while True:
		time.sleep(10)
		print("health check batch : ", i)
		i += 1
		for c, cont in enumerate(r.containers):
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
			if requests.get(ip+str(cont['port'])+"/api/v1/_health", headers=headers).status_code != 200:
				print("container on : ", cont['port'], " crashed")
				r.stopcontainer(c)
				r.startnewcontainer(cont['port'], c)
	sem1.release()


def fun3():
	sem2.acquire()
	print("sem2 acquired by fun3")
	while True:
		time.sleep(120)
		print("orchestrating for : ", r.tot_reqs, " requests")
		while r.size > int(r.tot_reqs / 20)+1:
			r.stopcontainer(r.size-1)
		while r.size < int(r.tot_reqs / 20)+1:
			r.startnewcontainer(r.size+8000, r.size)
		r.tot_reqs = 0
	sem2.release()


def handler(sig, frame):
	global r
	r.__del__()
	sys.exit(0)


if  __name__ == "__main__":

	signal.signal(signal.SIGINT, handler)
	#signal.signal(signal.SIGTSTP, handler)
	print('press CTRL+C to exit')
	
	thread1 = threading.Thread(target = fun1)
	thread2 = threading.Thread(target = fun2)
	thread3 = threading.Thread(target = fun3)
	thread1.start()
	thread2.start()
	thread3.start()

