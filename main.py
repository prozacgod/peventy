import peventy
import timer
import filesystem

count = [0]
@timer.onTimer(1000)
def timerTest(event):
	print "Test", count[0]
	count[0] += 1
	
	if ((count[0] % 5) == 4):
		@filesystem.readFile("test.bin")
		def readFileTest(data):
			c = len(data.split('\n'))
			print "Read %d lines from test.bin" % c 
		
	return True

peventy.run()
