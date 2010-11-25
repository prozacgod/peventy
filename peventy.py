#!/usr/bin/env python
import threading
from Queue import Queue
import time
import uuid

class StopableThread(threading.Thread):
	"""Python doesn't really have "job" control AFAIK, this helps"""
	mainThread = threading.currentThread()
	
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = True
		
	def is_running(self):
		return self.running and self.mainThread.isAlive()
		
	def stop(self):
		self.running = False

class TimerThread(StopableThread):
	def __init__(self, pe, interval, event_id):
		StopableThread.__init__(self)
		self.pe = pe
		self.interval = interval
		self.event_id = event_id
		threading.Thread.__init__(self)
		
	def run (self):
		while self.is_running():
			time.sleep(self.interval)
			self.pe.postEvent(self.event_id, self)
					
	
class Timer():
	def __init__(self, pe):
		self.pe = pe
		self.timers = []
		
	def onTimer(self, delay):
		def onTimerProxy(func):	
			print "add timer:", delay
			event_id = self.pe.addListener(func)
			self.createTimerThread(delay, event_id)
						
		return onTimerProxy
		
	def createTimerThread(self, delay, event_id):
		self.timers += [TimerThread(self.pe, delay/1000.0, event_id)]
		self.timers[-1].start()
		

class PEventY(object):
	def __init__(self):
		self.events = Queue()
		self.listeners = {}
		
		self.lib = {}
		self.lib['timer'] = Timer(self)
	
	# should this only ever be called by the main thread ???
	def addListener(self, callback):
		event_id = str(uuid.uuid4())
		self.listeners[event_id] = callback
		return event_id
		
	# Must be thread safe!!!
	def postEvent(self, *args):
		self.events.put(args)
		
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
			

def main():
	peventy = PEventY()
	evented_code(peventy.lib['timer'])
	peventy.run()


def evented_code(timer):
	""" this code here more or less should act similarly to node.js in that everything is an event"""
	count = [0]
	@timer.onTimer(1000)
	def timerTest(event):
		print "Test", count[0]
		count[0] += 1
		return True

	
if __name__ == "__main__":
	main()
