import time
import numpy as np
import pygame as pyg
import cv2
from PIL import Image as im


# --- Manager of OpenSesame UI --- #
class UIManager:
	def __init__(self, keywords, experimentCanvas):
		self.keywords = keywords
		self.experimentCanvas = experimentCanvas

		self.width = self.experimentCanvas.get_width()
		self.height = self.experimentCanvas.get_height()
		self.trialCanvas = None

		# --- UI PARAMETERS --- #
		# Keyword
		self.KW_y = 0.75*self.height
		self.KW_xDistance = 0.17*self.width
		self.KW_xRange = np.arange(len(self.keywords))*self.KW_xDistance + 0.5*self.width - self.KW_xDistance*(len(self.keywords)-1)/2

		# Keyword order
		self.KWO_yOffset = 0.05*self.height

		# Pose image
		self.PI_yOffset = -0.15*self.height
		self.PI_width = 0.05*self.width

		# Video
		self.VID_y = 0.01*self.height
		self.VID_height = 0.45*self.height
		self.VID_width = (578.0/632.0)*self.VID_height
		self.VID_frameDelay = 0.01
		self.VID_RECT = pyg.Rect(round(self.width/2-self.VID_width/2), round(self.VID_y), round(self.VID_width), round(self.VID_height))

		# Icon
		self.ICON_xOffset = 0.05*self.width
		self.ICON_width = 0.1*self.width

	def loadResources(self, baseFolder):
		print("Loading experiment resources")
		pyg.init()
		print("    Preloading fonts")
		self.keywordFont = pyg.font.SysFont("monospace", 28)
		self.keywordOrderFont = pyg.font.SysFont("monospace", 60, bold=True)
		keywordsUnderscored = list(keyword.replace(' ', '_') for keyword in self.keywords)

		print("    Preloading poses")
		self.images = []
		for i in range(len(self.keywords)):
			# TODO: Change to actual filename
			imagePath = f"{baseFolder}/poses/static/{keywordsUnderscored[i]}.png"
			fullImage = pyg.image.load(imagePath)
			resizedImage = pyg.transform.smoothscale(fullImage, (round(self.PI_width), round(self.PI_width*(fullImage.get_height()/fullImage.get_width()))))
			self.images.append(resizedImage.convert_alpha())

		print("    Preloading icons")
		self.icons = {}
		for iconName in ["ear", "eye"]:
			fullImage = pyg.image.load(f"{baseFolder}/icons/{iconName}.png")
			resizedImage = pyg.transform.smoothscale(fullImage, (round(self.ICON_width), round(self.ICON_width*(fullImage.get_height()/fullImage.get_width()))))
			self.icons[iconName] = resizedImage.convert_alpha()

		print("    Preloading video streams")
		self.videos = {}
		VID_PIXELS = (578, 632)
		VID_DIM = ((int(self.VID_width), int(self.VID_height)))
		# from: https://www.codegrepper.com/code-examples/python/python+split+video+into+frames
		for i in range(len(self.keywords)):
			full_video = f"{baseFolder}/poses/movies/{keywordsUnderscored[i]}.mp4"
			capture = cv2.VideoCapture(full_video)
			frameCount = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

			self.videos[i] = [] #np.zeros((frameCount, VID_DIM[0], VID_DIM[1], 3))
			success, frame = capture.read()
			assert (frame.shape[1],frame.shape[0]) == VID_PIXELS, "Video stream of unexpected resolution."
			while success:
				frame = cv2.resize(frame, VID_DIM)
				frame = cv2.transpose(frame)
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
				self.videos[i].append(frame)
				success, frame = capture.read()

		fullImage = pyg.image.load(f"{baseFolder}/poses/idle.jpg")
		self.idleImage = pyg.transform.smoothscale(fullImage, VID_DIM)

		# Prepare static background
		self.trialBGCanvas = pyg.Surface((self.width, self.height), flags=pyg.SRCALPHA)

		# Prepare video background
		self.videoCanvas = pyg.surface.Surface(VID_DIM)

		self.drawKeywords(self.trialBGCanvas)
		self.drawPoseImages(self.trialBGCanvas)
		self.drawVideoPlaceholder(self.trialBGCanvas)
		self.resetOverlays()
		print("Loading resources complete!")

	def createCanvas(self, order, symbol):
		self.drawKeywordOrder(self.keywordOrderverlay, order)
		self.drawIcon(self.iconOverLayCanvas, symbol)
		self.drawCross(self.crossOverLayCanvas)
		self.markRecognitionInactive()

	def resetOverlays(self):
		self.iconOverLayCanvas = pyg.Surface((self.width, self.height), flags=pyg.SRCALPHA)
		self.keywordOrderverlay = pyg.Surface((self.width, self.height), flags=pyg.SRCALPHA)
		self.keywordStatusOverlay = pyg.Surface((self.width, self.height), flags=pyg.SRCALPHA)
		self.crossOverLayCanvas = pyg.Surface((self.width, self.height), flags=pyg.SRCALPHA)
		self.iconShown = False
		self.isPresentingITI = False
		self.crossIsShown = False

	def show(self):
		assert self.trialBGCanvas is not None, "Trial canvas uninitialised"
		self.experimentCanvas.fill((255, 255, 255))
		self.experimentCanvas.blit(self.trialBGCanvas, (0, 0))
		if not self.isPresentingITI:
			self.experimentCanvas.blit(self.keywordOrderverlay, (0,0))
			self.experimentCanvas.blit(self.keywordStatusOverlay, (0,0))
		if self.iconShown:
			self.experimentCanvas.blit(self.iconOverLayCanvas, (0,0))
		if self.crossIsShown:
			self.experimentCanvas.blit(self.crossOverLayCanvas, (0,0))
		pyg.display.flip()

	def drawVideoPlaceholder(self, canvas):
		# canvas.fill((0, 0, 0), rect = self.VID_RECT)
		canvas.blit(self.idleImage, self.VID_RECT)

	def drawPoseImages(self, canvas):
		for i in range(len(self.keywords)):
			image = self.images[i]
			canvas.blit(image, (self.KW_xRange[i]-image.get_width()/2, self.KW_y + self.PI_yOffset))

	def drawKeywords(self, canvas):
		for i in range(len(self.keywords)):
			label = self.keywordFont.render(self.keywords[i], True, (0,0,0))
			canvas.blit(label, (self.KW_xRange[i]-label.get_width()/2, self.KW_y))

	def drawKeywordOrder(self, canvas, order):
		for i in range(len(order)):
			label = self.keywordOrderFont.render(f"{i+1}", True, (0,0,0))
			canvas.blit(label, (self.KW_xRange[order[i]]-label.get_width()/2, self.KW_y+self.KWO_yOffset))

	def drawCross(self, canvas):
		label = self.keywordOrderFont.render("x", True, (255,0,0))
		canvas.blit(label, (self.width/2-self.VID_width/2-self.ICON_xOffset-label.get_width()/2, self.VID_y+self.VID_height/2-label.get_height()/2))

	def drawIcon(self, canvas, symbol):
		assert symbol in ["eye", "ear"], "Requested symbol not preloaded"
		icon = self.icons[symbol]
		canvas.blit(icon, (self.width/2+self.VID_width/2+self.ICON_xOffset-icon.get_width()/2, self.VID_y+self.VID_height/2-icon.get_height()/2))

	def markCorrectKeyword(self, orderIndex, order):
		label = self.keywordOrderFont.render(f"{orderIndex+1}", True, (0, 255, 0))
		self.keywordStatusOverlay.blit(label, (self.KW_xRange[order[orderIndex]]-label.get_width()/2, self.KW_y+self.KWO_yOffset))

	def markRecognitionActive(self):
		self.iconShown = True

	def markRecognitionInactive(self):
		self.iconShown = False

	def markCrossActive(self):
		self.crossIsShown = True

	def markCrossInactive(self):
		self.crossIsShown = False

	def presentITI(self):
		self.isPresentingITI = True

	# runs when new video should be played after word is recognised
	def playVideo(self, index):
		frameArray = self.videos[index]

		for frame in frameArray:
			pyg.surfarray.blit_array(self.videoCanvas, frame)
			self.experimentCanvas.blit(self.videoCanvas, self.VID_RECT)
			pyg.display.flip()
			time.sleep(self.VID_frameDelay)

class ExperimentLogger:
	def __init__(self, var):
		self.var = var

	def reset(self):
		# TODO: Test effect of column / log name addition later in experiment on .CSV file
		# TODO: implement reset of logging, set all to-log variables to "-"
		for varname in self.var.vars():
			if varname.startswith("LL_"):
				self.var.set(varname, "NA")


	def log(self, name, value):
		self.var.set(name, value)

# --- Manager of trial --- #
class TrialManager:

	def __init__(self, order, keywords, _UImanager, logger):
		self.order = order
		self.progress = 0
		self.attempts = 0
		self.keywords = keywords
		self.keywordAmount = len(self.keywords)
		self.UIManager = _UImanager
		self.logger = logger

		# For storing the variables in before finally logging them:
		self.recognized_commands = []
		self.start_times_listening = []
		self.end_times_listening = []
		self.keyword_detection_times = []
		self.correct_keywords = []

		# --- TRIAL PARAMETER --- #
		self.ITI = 3 # seconds


	def prepare(self, icon):
		# Draw static image
		self.UIManager.createCanvas(self.order, icon)

	def run(self, recognizer, timeoutPerCommand):
		self.logger.reset()
		self.logger.log("LL_TimeTrialStart", time.time())

		# Main loop
		while self.progress != len(self.order): 
			self.UIManager.markRecognitionActive()
			self.UIManager.show()

			# self.logger.log(f"LL_TimeStartListeningForProgress_{self.progress}_Attempt_{self.attempts}", time.time())
			self.start_times_listening.append(time.time())

			moveIndex = recognizer.recognize(timeout = timeoutPerCommand)

			# self.logger.log(f"LL_TimeStoppedListeningForProgress_{self.progress}_Attempt_{self.attempts}", time.time())
			self.end_times_listening.append(time.time())

			# Automatic advancement, if you can't be loud in the room for debugging
			# time.sleep(1)
			# moveIndex = self.order[self.progress]

			self.UIManager.markRecognitionInactive()

			if moveIndex is None:
				print("No keyword detected, ending trial")
				self.logger.log("LL_TimeTrialEnd", time.time())
				self.logger.log("LL_TrialStatus", "failed")
				self.logger.log("LL_ProgressTrialFailedAt", self.progress)
				break
			
			self.processRecognisedMove(moveIndex)
		
		self.logger.log("LL_TimeTrialEnd", time.time())

		self.logger.log("LL_DetectedCommands", self.recognized_commands)
		self.logger.log("LL_TimeStartListening", self.start_times_listening)
		self.logger.log("LL_TimeStopListening", self.end_times_listening)
		self.logger.log("LL_TimeKeywordDetection", self.keyword_detection_times)
		self.logger.log("LL_CorrectKeyword", self.correct_keywords)

		self.logger.log("LL_TrialStatus", "success")
		if self.progress == len(self.order):
			print("Completed trial successfully")
		else:
			print("Failed trial")

		print("Presenting inter-trial-interval")
		self.logger.log("LL_TimeITIStart", time.time())
		self.UIManager.presentITI()
		self.UIManager.show()
		time.sleep(self.ITI)

		self.logger.log("LL_TimeITIEnd", time.time())
		self.UIManager.resetOverlays()

	# store the videos already when the order is known
	def loadVideos(self, order):
		# TODO use this function
		print("order is something like this")
		print(order)
		for i in self.videos:
			if i.index() + 1 in order:
				UIManager.current_video_order.append(i)

	def processRecognisedMove(self, moveIndex):
		print(f"Detected {self.keywords[moveIndex]}", end = '')

		if moveIndex not in self.order:

			self.keyword_detection_times.append(time.time())
			self.correct_keywords.append(0)

			print(", but not in current trial; ignoring")
			# self.logger.log(f"LL_TimeInvalidContextKeywordDetectedAtProgress_{self.progress}_Attempt_{self.attempts}", time.time())
			# self.logger.log(f"LL_InvalidContextKeywordDetectedAtProgress_{self.progress}_Attempt_{self.attempts}", moveIndex)
			self.attempts += 1

			self.UIManager.markCrossActive()
			self.UIManager.show()
			self.UIManager.playVideo(moveIndex)
			self.UIManager.markCrossInactive()

			self.recognized_commands.append(moveIndex)

			return
		elif moveIndex != self.order[self.progress]:

			self.keyword_detection_times.append(time.time())
			self.correct_keywords.append(0)

			print(", but not the next keyword; ignoring")
			# self.logger.log(f"LL_TimeInvalidOrderKeywordDetectedAtProgress_{self.progress}_Attempt_{self.attempts}", time.time())
			# self.logger.log(f"LL_InvalidOrderKeywordDetectedAtProgress_{self.progress}_Attempt_{self.attempts}", moveIndex)
			self.attempts += 1

			self.UIManager.markCrossActive()
			self.UIManager.show()
			self.UIManager.playVideo(moveIndex)
			self.UIManager.markCrossInactive()

			self.recognized_commands.append(moveIndex)

			return

		print(", advancing progress")
		#self.logger.log(f"LL_TimeValidKeywordDetectedAtProgress_{self.progress}", time.time())
		#self.logger.log(f"LL_KeywordDetectedAtProgress_{self.progress}", moveIndex)

		self.keyword_detection_times.append(time.time())
		self.correct_keywords.append(1)

		self.logger.log(f"LL_AttemptsForProgress_{self.progress}", self.attempts+1)
		self.progress += 1
		self.attempts = 0

		transformedIndex = self.order.index(moveIndex)
		self.UIManager.markCorrectKeyword(transformedIndex, self.order)

		# self.UIManager.temporary_video_updater_image(image = self.keywords[moveIndex])
		self.UIManager.show()
		self.UIManager.playVideo(moveIndex)

		# Halt until video completes
		self.UIManager.show()

		self.recognized_commands.append(moveIndex)

