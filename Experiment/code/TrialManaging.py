# import importlib
# importlib.import_module("/usr/lib/python3/dist-packages/libopensesame/python_workspace_api")

class ClassHolder:
	def __init__(self, Canvas, Text):
		self.Canvas = Canvas
		self.Text = Text


class TrialManager:

	def __init__(self, order, keywords, ClassHolder):
		self.order = order
		self.keywordAmount = len(self.order)

		self.keywords = keywords
		self.keywordOrder = [self.keywords[i] for i in self.order]

		self.trialCanvas = None
		self.CH = ClassHolder

	def prepare(self):
		yTop = -80
		yStep = 30

		# Prepare canvas with text
		self.trialCanvas = self.CH.Canvas()
		self.trialCanvas.set_font('mono', 24)
		for i in range(self.keywordAmount):
			self.trialCanvas[f"keywordText{i}"] = self.CH.Text(self.keywordOrder[i], y = yTop + i*yStep)

	def run(self, recognizer, timeout):
		assert(self.trialCanvas is not None)
		self.trialCanvas.show()

		# Start recognizer
		keywordIndex = recognizer.listen(timeout = timeout)

		if keywordIndex is not None and keywordIndex in self.order:
			self.processRecognisedKeyword(keywordIndex)
		else:
			print("No keyword detected, moving on")

	def processRecognisedKeyword(self, keywordIndex):
		transformedIndex = self.order.index(keywordIndex)
		print(f"Detected {self.keywordOrder[transformedIndex]}")

		# Update color
		self.trialCanvas[f"keywordText{transformedIndex}"].color = 'green'

		# Update canvas
		self.trialCanvas.show()