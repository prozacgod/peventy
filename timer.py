from peventy import PEventYModule,PEventYModuleThread, peventy
import time

class TimerThread(PEventYModuleThread):
	def __init__(self, pe, event_id, interval):
		super(TimerThread, self).__init__(pe, event_id)
		self.interval = interval/1000.0
		
	def run (self):
		while self.is_running():
			time.sleep(self.interval)
			self.mod.postEvent(self.event_id, self)

class Timer(PEventYModule):
	def onTimer(self, delay):
		def onTimerProxy(func):	
			self.createListenerThread(func, TimerThread, delay)
						
		return onTimerProxy

timer = peventy.registerLibrary('timer', Timer)
onTimer = timer.onTimer
