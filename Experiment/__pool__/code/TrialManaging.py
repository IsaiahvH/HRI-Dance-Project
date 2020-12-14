import time
import numpy as np

# --- Holder for OpenSesame classes --- #
class OSHolder:
	def __init__(self, Canvas, Text, Image, baseFolder):
		self.Canvas = Canvas
		self.Text = Text
		self.Image = Image
		self.baseFolder = baseFolder

# --- Manager of OpenSesame UI --- #
class UIManager:
	def __init__(self, order, keywords, OSH):
		self.order = order
		self.keywords = keywords
		self.OSH = OSH
		self.trialCanvas = self.OSH.Canvas()
		self.trialCanvas.set_font('mono', 18)

		# --- UI PARAMETERS --- #

		# Keyword parameters
		self.KW_y = 280
		self.KW_xDistance = 400
		self.KW_xRange = np.linspace(-self.KW_xDistance, self.KW_xDistance, len(self.keywords))

		# Keyword order parameters
		self.KWO_yOffset = 50
		self.KWO_fontSize = 40

		# Pose image parameters
		self.PI_yOffset = -70
		self.PI_scale = 0.2

	def show(self):
		self.trialCanvas.show()

	def drawPoseImages(self):
		for i in range(len(self.keywords)):
			# TODO: Change to actual filename
			imagePath = f"{self.OSH.baseFolder}/poses/demo.png" #{keywords[i].title().replace(' ', '')}"
			self.trialCanvas[f"poseImage{i}"] = self.OSH.Image(imagePath, x = self.KW_xRange[i], y = self.KW_y + self.PI_yOffset, scale = self.PI_scale)

	def drawKeywords(self):
		for i in range(len(self.keywords)):
			self.trialCanvas[f"keywordText{i}"] = self.OSH.Text(self.keywords[i], x = self.KW_xRange[i], y = self.KW_y)

	def drawKeywordOrder(self):
		for i in range(len(self.order)):
			self.trialCanvas[f"orderText{i}"] = self.OSH.Text(f"{i+1}", x = self.KW_xRange[self.order[i]], y = self.KW_y+self.KWO_yOffset, font_size = self.KWO_fontSize)

	def markCorrectKeyword(self, orderIndex):
		self.trialCanvas[f"orderText{orderIndex}"].color = 'green'

	def unmarkCorrectKeyword(self, orderIndex):
		self.trialCanvas[f"orderText{orderIndex}"].color = 'black'

	def presentITI(self):
		for i in range(len(self.order)):
			self.trialCanvas[f"orderText{i}"].color = 'black'

# --- Manager of trial --- #
class TrialManager:

	def __init__(self, order, keywords, OSH):
		self.order = order
		self.progress = 0
		self.keywords = keywords
		self.keywordAmount = len(self.keywords)

		self.UIManager = UIManager(self.order, self.keywords, OSH)

		# --- TRIAL PARAMETERS --- #
		self.timePerKeywordRecognition = 4000


	def prepare(self):
		# Draw keywords
		self.UIManager.drawKeywords()
		self.UIManager.drawKeywordOrder()
		self.UIManager.drawPoseImages()

	def run(self, recognizer, timeout):
		self.UIManager.show()
		startTime = time.time()

		# Main loop
		while self.progress != len(self.order): 
			keywordIndex = recognizer.listen(timeout = self.timePerKeywordRecognition)

			if keywordIndex is None:
				print("No keyword detected, ending trial")
				break
			
			self.processRecognisedKeyword(keywordIndex)
		
		endTime = time.time()
		self.UIManager.presentITI()
		self.UIManager.show()

		# TODO: Determine which information needs to be logged / returned
		return self.progress, (startTime - endTime)


	def processRecognisedKeyword(self, keywordIndex):
		print(f"Detected {self.keywords[keywordIndex]}", end = '')
		if keywordIndex not in self.order:
			print(", but not in current trial; ignoring")
			return
		elif keywordIndex != self.order[self.progress]:
			print(", but not the next keyword; ignoring")
			return

		print(", advancing progress")
		self.progress += 1
		transformedIndex = self.order.index(keywordIndex)
		self.UIManager.markCorrectKeyword(transformedIndex)
		self.UIManager.show()