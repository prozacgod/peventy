from peventy import PEventYModule, PEventYModuleThread, peventy
import time

class FileReadThread(PEventYModuleThread):
	def __init__(self, pe, event_id, fname):
		super(FileReadThread, self).__init__(pe, event_id)
		self.fname = fname
		self.event_id = event_id
		
	def run (self):
		data = open(self.fname, 'r').read()
		self.mod.postEvent(self.event_id, data)


class FileSystem(PEventYModule):
	def readFile(self, fname):
		def readFileProxy(callback):	
			print "reading file:", fname
			self.createListenerThread(callback, FileReadThread, fname)
		return readFileProxy

fs = peventy.registerLibrary('fs', FileSystem)
readFile = fs.readFile

