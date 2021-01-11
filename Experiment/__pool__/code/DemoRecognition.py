import time
import struct
from pynput.keyboard import keyboard

class DemoRecognizer:

	def __init__(self, keywords):
		''' Initialise demo recognizer
		- keywords: an array of strings of the keywords used
		'''
		assert keywords.size() <= 10, "More keywords than numeric keys available"
		self.keywordLength = keywords.size()

	def startEngine(self):
		''' Start demo engine
		'''
		print("DemoRecognizer engine started")

	def restartEngine(self):
		''' Restart demo engine
		'''
		self.shutDownEngine()
		self.startEngine()

	def shutDownEngine(self):
		''' Shut down demo engine
		'''
		print("DemoRecognizer engine shut down")

	def getEngineStatus(self):
		''' Get demo engine status
		Returns: True if engine is running normally, False otherwise
		'''
		return True

	def recognize(self, timeout):
		''' Await for keystroke commands.
		- timeout: the amount of seconds before waiting stops

		Returns: an Int being the index of the keyword corresponding to the received keystroke, or
				None if the timeout expired before a keystroke was received
		'''

		try:
			with keyboard.Events() as events:
				event = events.get(timeout)
				if event is None or event.key == keyboard.Key.esc:
					return None
				else:
					for i in range(self.keywords.size()):
						if event.key == keyboard.KeyCode(char = f'{i+1}'):
							return i
		except Exception as e:
			print("DemoRecognizer encountered an error upon awaiting keystrokes")
