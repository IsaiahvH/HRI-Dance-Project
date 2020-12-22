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
		self.VID_y = 0.03*self.height
		self.VID_height = 0.45*self.height
		self.VID_width = 0.45*self.width
		self.VID_duration = 4
		self.current_video_order = []

		# Icon
		self.ICON_xOffset = 0.05*self.width
		self.ICON_width = 0.1*self.width

	def loadResources(self, baseFolder):
		pyg.init()
		self.keywordFont = pyg.font.SysFont("monospace", 28)
		self.keywordOrderFont = pyg.font.SysFont("monospace", 60, bold=True)

		self.images = []
		for _ in range(len(self.keywords)):
			# TODO: Change to actual filename
			imagePath = f"{baseFolder}/poses/demo.png"
			fullImage = pyg.image.load(imagePath)
			resizedImage = pyg.transform.smoothscale(fullImage, (round(self.PI_width), round(self.PI_width*(fullImage.get_height()/fullImage.get_width()))))
			self.images.append(resizedImage.convert_alpha())

		self.icons = {}
		for iconName in ["ear", "eye"]:
			fullImage = pyg.image.load(f"{baseFolder}/icons/{iconName}.png")
			resizedImage = pyg.transform.smoothscale(fullImage, (round(self.ICON_width), round(self.ICON_width*(fullImage.get_height()/fullImage.get_width()))))
			self.icons[iconName] = resizedImage.convert_alpha()

		image_names = ["air guitar", "clap your hands", "raise the roof", "hands on hips", "do the disco", "give a box"]
		self.image_video = {}
		for image in image_names:
			full_image = pyg.image.load(f"{baseFolder}/icons/{image}.png")
			resized_image = pyg.transform.smoothscale(full_image, (round(self.VID_width), round(self.VID_width*(full_image.get_height()/full_image.get_width()))))
			self.image_video[image] = resized_image.convert_alpha()

		pose_names = ["air guitar", "clap your hands", "raise the roof", "hands on hips", "do the disco", "give a box"]
		self.videos = {}
		# from: https://www.codegrepper.com/code-examples/python/python+split+video+into+frames
		for pose_name in pose_names:
			full_video = f"C:/Users/lizzy/PycharmProjects/HRI-Dance-Project/Experiment/__pool__/poses/{pose_name}.mp4"
			vidcap = cv2.VideoCapture(full_video)
			success, frame = vidcap.read()
			count = 0
			while success:
				success, frame = vidcap.read()
				count += 1
				#frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				if success:
					frame = np.reshape(frame, (632, 578, 3))
					frame = im.fromarray(frame, 'RGB')
					if pose_name in self.videos:
						self.videos[pose_name].append(frame)
					else:
						self.videos[pose_name] = [frame]

		# Prepare static background
		self.trialBGCanvas = pyg.Surface((self.width, self.height), flags=pyg.SRCALPHA)

		self.drawKeywords(self.trialBGCanvas)
		self.drawPoseImages(self.trialBGCanvas)
		self.drawVideoPlaceholder(self.trialBGCanvas)
		self.resetOverlays()



	def createCanvas(self, order, symbol):
		self.drawKeywordOrder(self.keywordOrderverlay, order)
		self.drawIcon(self.iconOverLayCanvas, symbol)
		self.markRecognitionInactive()

	def resetOverlays(self):
		self.iconOverLayCanvas = pyg.Surface((self.width, self.height), flags=pyg.SRCALPHA)
		self.keywordOrderverlay = pyg.Surface((self.width, self.height), flags=pyg.SRCALPHA)
		self.keywordStatusOverlay = pyg.Surface((self.width, self.height), flags=pyg.SRCALPHA)
		self.iconShown = False
		self.isPresentingITI = False

	def show(self):
		assert self.trialBGCanvas is not None, "Trial canvas uninitialised"
		self.experimentCanvas.fill((255, 255, 255))
		self.experimentCanvas.blit(self.trialBGCanvas, (0, 0))
		if not self.isPresentingITI:
			self.experimentCanvas.blit(self.keywordOrderverlay, (0,0))
			self.experimentCanvas.blit(self.keywordStatusOverlay, (0,0))
		if self.iconShown:
			self.experimentCanvas.blit(self.iconOverLayCanvas, (0,0))
		pyg.display.flip()

	def drawVideoPlaceholder(self, canvas):
		rect = pyg.Rect(self.width/2-self.VID_width/2, self.VID_y, self.VID_width, self.VID_height)
		canvas.fill((0, 0, 0), rect = rect)

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

	def presentITI(self):
		self.isPresentingITI = True

	def temporary_video_updater_image(self, image):
		image_video = self.image_video[image]
		self.trialBGCanvas.blit(image_video, (self.width/2-self.VID_width/2, self.VID_y, self.VID_width, self.VID_height))

	# runs when new video should be played after word is recognised
	def updateVideo(self, orderIndex, image):
		image_arrays = self.videos[image]

		for array in image_arrays:
			mode = array.mode
			size = array.size
			data = array.tobytes()
			py_image = pyg.image.fromstring(data, size, mode)
			self.trialBGCanvas.blit(py_image, (self.width/2-self.VID_width/2, self.VID_y, self.VID_width, self.VID_height))

# --- Manager of trial --- #
class TrialManager:

	def __init__(self, order, keywords, _UImanager):
		self.order = order
		self.progress = 0
		self.keywords = keywords
		self.keywordAmount = len(self.keywords)
		self.UIManager = _UImanager

		# --- TRIAL PARAMETERS --- #
		self.ITI = 3 # seconds


	def prepare(self, icon):
		# Draw static image
		self.UIManager.createCanvas(self.order, icon)

	def run(self, recognizer, timeoutPerCommand):
		startTime = time.time()

		# Main loop
		while self.progress != len(self.order): 
			self.UIManager.markRecognitionActive()
			self.UIManager.show()

			moveIndex = recognizer.recognize(timeout = timeoutPerCommand)
			self.UIManager.markRecognitionInactive()

			if moveIndex is None:
				print("No keyword detected, ending trial")
				break
			
			self.processRecognisedMove(moveIndex)
		
		endTime = time.time()
		if self.progress == len(self.order):
			print("Completed trial successfully")
		else:
			print("Failed trial")

		print("Presenting inter-trial-interval")
		self.UIManager.presentITI()
		self.UIManager.show()
		time.sleep(self.ITI)


		self.UIManager.resetOverlays()

		# TODO: Determine which information needs to be logged / returned
		return self.progress, (startTime - endTime)

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
			print(", but not in current trial; ignoring")
			return
		elif moveIndex != self.order[self.progress]:
			print(", but not the next keyword; ignoring")
			return

		print(", advancing progress")
		self.progress += 1

		transformedIndex = self.order.index(moveIndex)
		self.UIManager.markCorrectKeyword(transformedIndex, self.order)
		self.UIManager.updateVideo(orderIndex = transformedIndex, image = self.keywords[moveIndex])
		# self.UIManager.temporary_video_updater_image(image = self.keywords[moveIndex])
		self.UIManager.show()

		# Halt until video completes
		time.sleep(self.UIManager.VID_duration)
		# self.UIManager.updateVideo(orderIndex = None)
		self.UIManager.show()
