#!/usr/bin/env python
import threading
from Queue import Queue
import time
import uuid

class PEventYModuleThread(threading.Thread):
	"""Python doesn't really have "job" control AFAIK, this helps"""
	mainThread = threading.currentThread()
	
	def __init__(self, module, event_id):
		threading.Thread.__init__(self)
		self.running = True
		
		self.mod = module
		self.event_id = event_id
		
	def is_running(self):
		return self.running and self.mainThread.isAlive()
		
	def stop(self):
		self.running = False


class PEventYModule(object):
	def __init__(self, pe):
		self.pe = pe
		self.threads = {}

	def createListenerThread(self, callback, thread, *args):
		event_id = self.pe.addListener(callback)
		self.threads[event_id] = thread(self.pe, event_id, *args)
		self.threads[event_id].start()
		
	def postEvent(self, event_id, *args):
		self.pe.postEvent(self.event_id, *args)
		self.threads[event_id].join()
		del self.threads[event_id]


class PEventY(object):
	def __init__(self):
		self.events = Queue()
		self.listeners = {}
		self.libraries = {}

	# should this only ever be called by the main thread ???
	def addListener(self, callback):
		event_id = str(uuid.uuid4())
		self.listeners[event_id] = callback
		return event_id
		
	# Must be thread safe!!!
	def postEvent(self, *args):
		self.events.put(args)
		
	def registerLibrary(self, name, klass):
		self.libraries[name] = klass(self)
		return self.libraries[name]
		
	def run(self):
		while len(self.listeners):
			event = self.events.get()
			print event
			
			event_id = event[0]
			args = event[1:]
			
			if event_id in self.listeners:
				self.listeners[event_id](*args)
			else:
				print "Event missfire"


peventy = PEventY()
def run():
	peventy.run()
