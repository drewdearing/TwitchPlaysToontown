import socket
import pyautogui
import threading
import time
from auth import login

SERVER = "irc.twitch.tv"
PORT = 6667
PASS = login()
BOT = "PeachBot"
CHANNEL = "itspeachtea"
OWNER = "itspeachtea"

messageList = []

irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send((
	"PASS "+ PASS + "\n" + 
	"NICK " + BOT + "\n" +
	"JOIN #" + CHANNEL + "\n"
	).encode())

def gameControl():

	inGags = False
	inTasks = False
	monitorSize = pyautogui.size()
	sinceLastInput = time.time()

	unsafeBounds = [{
		"xMin": 1072,
		"xMax": 1334,
		"yMin": 777,
		"yMax": 843
	},
	{
		"xMin": 1069,
		"xMax": 1229,
		"yMin": 608,
		"yMax": 666
	}]

	movement = {
		"up": {
			"key": "up",
			"down": False
		},
		"back": {
			"key": "down",
			"down": False
		},
		"right": {
			"key": "right",
			"down": False
		},
		"left": {
			"key": "left",
			"down": False
		},
		"jump": {
			"key": "ctrl",
			"down": False
		}
	}

	def controlMovement(args, size, message):
		if(size > 0):
			direction = args[0]
			key = movement[args[0]]["key"]
			if(size > 1):
				try:
					t = float(msgSplit[1])
				except:
					t = 0.0
				if(t > 0):
					newThread = threading.Thread(target = holdKey, args=(key, t))
					newThread.start()
					return
			pyautogui.keyDown(key)
			pyautogui.keUp(key)
		else:
			sendMessage(message)

	def holdKey(key, seconds):
		seconds = min(seconds, 30.0)
		pyautogui.keyDown(key)
		time.sleep(seconds)
		pyautogui.keyUp(key)

	def walkForward():
		pyautogui.keyDown('up')
		pyautogui.keyUp('up')

	def walkForwardFor(message):
		msgSplit = message.split(" ")
		if(len(msgSplit) == 2 and msgSplit[0] == "forward"):
			try:
				t = float(msgSplit[1])
			except:
				t = 0.0
			if(t <= 0):
				walkForward()
			else:
				newThread = threading.Thread(target = holdKey, args=('up', t))
				newThread.start()

	def walkBackward():
		pyautogui.keyDown('down')
		pyautogui.keyUp('down')

	def walkBackwardFor(message):
		msgSplit = message.split(" ")
		if(len(msgSplit) == 2 and msgSplit[0] == "backward"):
			try:
				t = float(msgSplit[1])
			except:
				t = 0.0
			if(t <= 0):
				walkBackward()
			else:
				newThread = threading.Thread(target = holdKey, args=('down', t))
				newThread.start()

	def turnRight():
		pyautogui.keyDown('right')
		pyautogui.keyUp('right')

	def turnRightFor(message):
		msgSplit = message.split(" ")
		if(len(msgSplit) == 2 and msgSplit[0] == "right"):
			try:
				t = float(msgSplit[1])
			except:
				t = 0.0
			if(t <= 0):
				turnRight()
			else:
				newThread = threading.Thread(target = holdKey, args=('right', t))
				newThread.start()

	def turnLeft():
		pyautogui.keyDown('left')
		pyautogui.keyUp('left')

	def turnLeftFor(message):
		msgSplit = message.split(" ")
		if(len(msgSplit) == 2 and msgSplit[0] == "left"):
			try:
				t = float(msgSplit[1])
			except:
				t = 0.0
			if(t <= 0):
				turnLeft()
			else:
				newThread = threading.Thread(target = holdKey, args=('left', t))
				newThread.start()

	def isHoldFor(direction, message):
		msgSplit = message.split(" ")
		if(direction in message and len(msgSplit) == 2 and msgSplit[0] == direction):
			try:
				t = float(msgSplit[1])
			except:
				return False
			return True
		else:
			return False

	def jump():
		pyautogui.keyDown('ctrl')
		pyautogui.keyUp('ctrl')

	def jumpFor(message):
		msgSplit = message.split(" ")
		if(len(msgSplit) == 2 and msgSplit[0] == "jump"):
			try:
				t = float(msgSplit[1])
			except:
				t = 0.0
			if(t <= 0):
				jump()
			else:
				newThread = threading.Thread(target = holdKey, args=('ctrl', t))
				newThread.start()

	def gags():
		global inGags
		if (inGags):
			pyautogui.keyUp('home')
			inGags = False
		else:
			if(inTasks):
				tasks()
			pyautogui.keyDown('home')
			inGags = True

	def tasks():
		global inTasks
		if (inTasks):
			pyautogui.keyUp('end')
			inTasks = False
		else:
			if(inGags):
				gags()
			pyautogui.keyDown('end')
			inTasks = True

	def inUnsafeClickBounds():
		global unsafeBounds
		posx, posy = pyautogui.position()
		for bound in unsafeBounds:
			if (posx >= bound["xMin"] and
				posx <= bound["xMax"] and
				posy >= bound["yMin"] and
				posy <= bound["yMax"]):
				return True
		return False

	def clickMouse():
		if(inUnsafeClickBounds()):
			print("WARNING: unsafe click detected")
		else:
			pyautogui.click()

	def map():
		pyautogui.keyDown('alt')
		pyautogui.keyUp('alt')

	def friends():
		pyautogui.keyDown('f7')
		pyautogui.keyUp('f7')

	def book():
		pyautogui.keyDown('f8')
		pyautogui.keyUp('f8')

	def delete():
		pyautogui.keyDown('del')
		pyautogui.keyUp('del')

	def moveMouseUp():
		pyautogui.moveRel(None, -1)
		print(pyautogui.position())

	def moveMouseDown():
		pyautogui.moveRel(None, 1)
		print(pyautogui.position())

	def moveMouseRight():
		pyautogui.moveRel(1, None)
		print(pyautogui.position())

	def moveMouseLeft():
		pyautogui.moveRel(-1, None)
		print(pyautogui.position())

	def typeMessage(message):
		pyautogui.typewrite(message, interval=0.01)
		pyautogui.keyDown("enter")
		pyautogui.keyUp("enter")

	def feather():
		pyautogui.moveTo(650, 316)
		clickMouse()

	def megaphone():
		pyautogui.moveTo(739, 316)
		clickMouse()

	def lipstick():
		pyautogui.moveTo(828, 316)
		clickMouse()

	def bambooCane():
		pyautogui.moveTo(913, 316)
		clickMouse()

	def pixieDust():
		pyautogui.moveTo(1000, 316)
		clickMouse()

	def jugglingBalls():
		pyautogui.moveTo(1090, 316)
		clickMouse()

	def highDive():
		pyautogui.moveTo(1177, 316)
		clickMouse()

	def bananaPeel():
		pyautogui.moveTo(650, 375)
		clickMouse()

	def rake():
		pyautogui.moveTo(739, 375)
		clickMouse()

	def marbles():
		pyautogui.moveTo(828, 375)
		clickMouse()

	def quicksand():
		pyautogui.moveTo(913, 375)
		clickMouse()

	def trapdoor():
		pyautogui.moveTo(1000, 375)
		clickMouse()

	def tnt():
		pyautogui.moveTo(1090, 375)
		clickMouse()

	def railroad():
		pyautogui.moveTo(1177, 375)
		clickMouse()

	def oneBill():
		pyautogui.moveTo(650, 433)
		clickMouse()

	def smallMagnet():
		pyautogui.moveTo(739, 433)
		clickMouse()

	def fiveBill():
		pyautogui.moveTo(828, 433)
		clickMouse()

	def bigMagnet():
		pyautogui.moveTo(913, 433)
		clickMouse()

	def Tenbill():
		pyautogui.moveTo(1000, 433)
		clickMouse()

	def hypnoGoggles():
		pyautogui.moveTo(1090, 433)
		clickMouse()

	def presentation():
		pyautogui.moveTo(1177, 433)
		clickMouse()

	def bikeHorn():
		pyautogui.moveTo(650, 492)
		clickMouse()

	def whistle():
		pyautogui.moveTo(739, 492)
		clickMouse()

	def bugle():
		pyautogui.moveTo(828, 492)
		clickMouse()

	def aoogah():
		pyautogui.moveTo(913, 492)
		clickMouse()

	def elephantTrunk():
		pyautogui.moveTo(1000, 492)
		clickMouse()

	def foghorn():
		pyautogui.moveTo(1090, 492)
		clickMouse()

	def operaSinger():
		pyautogui.moveTo(1177, 492)
		clickMouse()

	def cupcake():
		pyautogui.moveTo(650, 548)
		clickMouse()

	def fruitPieSlice():
		pyautogui.moveTo(739, 548)
		clickMouse()

	def creamPieSlice():
		pyautogui.moveTo(828, 548)
		clickMouse()

	def wholeFruitPie():
		pyautogui.moveTo(913, 548)
		clickMouse()

	def wholeCreamPie():
		pyautogui.moveTo(1000, 548)
		clickMouse()

	def birthdayCake():
		pyautogui.moveTo(1090, 548)
		clickMouse()

	def weddingCake():
		pyautogui.moveTo(1177, 548)
		clickMouse()

	def squirtingFlower():
		pyautogui.moveTo(650, 608)
		clickMouse()

	def glassOfWater():
		pyautogui.moveTo(739, 608)
		clickMouse()

	def squirtGun():
		pyautogui.moveTo(28, 608)
		clickMouse()

	def seltzerBottle():
		pyautogui.moveTo(913, 608)
		clickMouse()

	def fireHose():
		pyautogui.moveTo(1000, 608)
		clickMouse()

	def stormCloud():
		pyautogui.moveTo(1090, 608)
		clickMouse()

	def geyser():
		pyautogui.moveTo(1177, 608)
		clickMouse()

	def flowerPot():
		pyautogui.moveTo(650, 664)
		clickMouse()

	def sandbag():
		pyautogui.moveTo(739, 664)
		clickMouse()

	def anvil():
		pyautogui.moveTo(828, 664)
		clickMouse()

	def bigWeight():
		pyautogui.moveTo(913, 664)
		clickMouse()

	def safe():
		pyautogui.moveTo(1000, 664)
		clickMouse()

	def grandPiano():
		pyautogui.moveTo(1090, 675)
		clickMouse()

	def toontanic():
		pyautogui.moveTo(1177, 675)
		clickMouse()

	def buyFeather():
		pyautogui.moveTo(780, 288)
		clickMouse()

	def buyMegaphone():
		pyautogui.moveTo(859, 288)
		clickMouse()

	def buyLipstick():
		pyautogui.moveTo(938, 288)
		clickMouse()

	def buyBambooCane():
		pyautogui.moveTo(1017, 288)
		clickMouse()

	def buyPixieDust():
		pyautogui.moveTo(1096, 288)
		clickMouse()

	def buyJugglingBalls():
		pyautogui.moveTo(1175, 288)
		clickMouse()

	def buyHighDive():
		pyautogui.moveTo(1254, 288)
		clickMouse()

	def buyBananaPeel():
		pyautogui.moveTo(780, 341)
		clickMouse()

	def buyRake():
		pyautogui.moveTo(859, 341)
		clickMouse()

	def buyMarbles():
		pyautogui.moveTo(938, 341)
		clickMouse()

	def buyQuicksand():
		pyautogui.moveTo(1017, 341)
		clickMouse()

	def buyTrapdoor():
		pyautogui.moveTo(1096, 341)
		clickMouse()

	def buyTnt():
		pyautogui.moveTo(1175, 341)
		clickMouse()

	def buyRailroad():
		pyautogui.moveTo(1254, 341)
		clickMouse()

	def buyOneBill():
		pyautogui.moveTo(780, 394)
		clickMouse()

	def buySmallMagnet():
		pyautogui.moveTo(859, 394)
		clickMouse()

	def buyFiveBill():
		pyautogui.moveTo(938, 394)
		clickMouse()

	def buyBigMagnet():
		pyautogui.moveTo(1017, 394)
		clickMouse()

	def buyTenbill():
		pyautogui.moveTo(1096, 394)
		clickMouse()

	def buyHypnoGoggles():
		pyautogui.moveTo(1175, 394)
		clickMouse()

	def buyPresentation():
		pyautogui.moveTo(1254, 394)
		clickMouse()

	def buyBikeHorn():
		pyautogui.moveTo(780, 447)
		clickMouse()

	def buyWhistle():
		pyautogui.moveTo(859, 447)
		clickMouse()

	def buyBugle():
		pyautogui.moveTo(938, 447)
		clickMouse()

	def buyAoogah():
		pyautogui.moveTo(1017, 447)
		clickMouse()

	def buyElephantTrunk():
		pyautogui.moveTo(1096, 447)
		clickMouse()

	def buyFoghorn():
		pyautogui.moveTo(1175, 447)
		clickMouse()

	def buyOperaSinger():
		pyautogui.moveTo(1254, 447)
		clickMouse()

	def buyCupcake():
		pyautogui.moveTo(780, 500)
		clickMouse()

	def buyFruitPieSlice():
		pyautogui.moveTo(859, 500)
		clickMouse()

	def buyCreamPieSlice():
		pyautogui.moveTo(938, 500)
		clickMouse()

	def buyWholeFruitPie():
		pyautogui.moveTo(1017, 500)
		clickMouse()

	def buyWholeCreamPie():
		pyautogui.moveTo(1096, 500)
		clickMouse()

	def buyBirthdayCake():
		pyautogui.moveTo(1175, 500)
		clickMouse()

	def buyWeddingCake():
		pyautogui.moveTo(1254, 500)
		clickMouse()

	def buySquirtingFlower():
		pyautogui.moveTo(780, 553)
		clickMouse()

	def buyGlassOfWater():
		pyautogui.moveTo(859, 553)
		clickMouse()

	def buySquirtGun():
		pyautogui.moveTo(938, 553)
		clickMouse()

	def buySeltzerBottle():
		pyautogui.moveTo(1017, 553)
		clickMouse()

	def buyFireHose():
		pyautogui.moveTo(1096, 553)
		clickMouse()

	def buyStormCloud():
		pyautogui.moveTo(1175, 553)
		clickMouse()

	def buyGeyser():
		pyautogui.moveTo(1254, 553)
		clickMouse()

	def buyFlowerPot():
		pyautogui.moveTo(780, 606)
		clickMouse()

	def buySandbag():
		pyautogui.moveTo(859, 606)
		clickMouse()

	def buyAnvil():
		pyautogui.moveTo(938, 606)
		clickMouse()

	def buyBigWeight():
		pyautogui.moveTo(1017, 606)
		clickMouse()

	def buySafe():
		pyautogui.moveTo(1096, 606)
		clickMouse()

	def buyGrandPiano():
		pyautogui.moveTo(1175, 606)
		clickMouse()

	def buyToontanic():
		pyautogui.moveTo(1254, 606)
		clickMouse()

	def doneShopping():
		pyautogui.moveTo(1454, 582)
		clickMouse()

	def deleteGag():
		pyautogui.moveTo(709, 705)
		clickMouse()

	def blamCanyon():
		pyautogui.moveTo(584,294)
		clickMouse()

	def boingbury():
		pyautogui.moveTo(584,334)
		clickMouse()

	def bounceboro():
		pyautogui.moveTo(584,369)
		clickMouse()

	def fizzlefield():
		pyautogui.moveTo(584,401)
		clickMouse()

	def gulpGulch():
		pyautogui.moveTo(584,439)
		clickMouse()

	def hiccupHills():
		pyautogui.moveTo(584,473)
		clickMouse()

	def kaboomCliffs():
		pyautogui.moveTo(584,512)
		clickMouse()

	def splashport():
		pyautogui.moveTo(584,543)
		clickMouse()

	def splatSummit():
		pyautogui.moveTo(584,576)
		clickMouse()

	def thwackville():
		pyautogui.moveTo(584,615)
		clickMouse()

	def whooshRapids():
		pyautogui.moveTo(584,647)
		clickMouse()

	def zoinkFalls():
		pyautogui.moveTo(584,685)
		clickMouse()

	def welcomeValley():
		pyautogui.moveTo(584,720)
		clickMouse()

	def teleportHere():
		pyautogui.moveTo(1184,745)
		clickMouse()

	def goHome():
		pyautogui.moveTo(1033,835)
		clickMouse()

	def backToPlayGround():
		pyautogui.moveTo(1133,853)
		clickMouse()

	def goofySpeedway():
		pyautogui.moveTo(650,442)
		clickMouse()

	def toontownCentral():
		pyautogui.moveTo(960,496)
		clickMouse()

	def donaldsDreamland():
		pyautogui.moveTo(916,212)
		clickMouse()

	def theBrrrgh():
		pyautogui.moveTo(1224,310)
		clickMouse()

	def daisyGardens():
		pyautogui.moveTo(798,682)
		clickMouse()

	def minniesMelodyland():
		pyautogui.moveTo(999,356)
		clickMouse()

	def donaldsDock():
		pyautogui.moveTo(1259,488)
		clickMouse()

	def chipNDales():
		pyautogui.moveTo(1068,661)
		clickMouse()

	def closeFriends():
		pyautogui.moveTo(1800,453)
		clickMouse()

	def friendsUp():
		pyautogui.moveTo(1800,186)
		clickMouse()

	def friendsDown():
		pyautogui.moveTo(1800,414)
		clickMouse()

	def friendsNext():
		pyautogui.moveTo(1881,453)
		clickMouse()

	def friendsPrev():
		pyautogui.moveTo(1720,453)
		clickMouse()

	def friends1():
		pyautogui.moveTo(1720,212)
		clickMouse()

	def friends2():
		pyautogui.moveTo(1720,235)
		clickMouse()

	def friends3():
		pyautogui.moveTo(1720,260)
		clickMouse()

	def friends4():
		pyautogui.moveTo(1720,284)
		clickMouse()

	def friends5():
		pyautogui.moveTo(1720,311)
		clickMouse()

	def friends6():
		pyautogui.moveTo(1720,335)
		clickMouse()

	def friends7():
		pyautogui.moveTo(1720,359)
		clickMouse()

	def friends8():
		pyautogui.moveTo(1720,383)
		clickMouse()

	def toonFriends():
		pyautogui.moveTo(1744,181)
		clickMouse()

	def toonGoTo():
		pyautogui.moveTo(1744,230)
		clickMouse()

	def toonWhisper():
		pyautogui.moveTo(1744,276)
		clickMouse()

	def toonClose():
		pyautogui.moveTo(1886,459)
		clickMouse()

	def acceptRequest():
		pyautogui.moveTo(1158,200)
		clickMouse()

	def rejectRequest():
		pyautogui.moveTo(1248,200)
		clickMouse()

	def switchDistrict():
		pyautogui.moveTo(1293,270)
		clickMouse()

	def dontSwitchDistrict():
		pyautogui.moveTo(1455,270)
		clickMouse()

	while True:
		if(len(messageList) > 0):
			sinceLastInput = time.time()
			timeoutStalling = False
			msg = messageList.pop(0)
			user = msg["user"]
			message = msg["message"].lower()

			print("reading " + message)

			if message == "forward":
				walkForward()
			elif isHoldFor("forward", message):
				walkForwardFor(message)
			elif message == "backward":
				walkBackward()
			elif isHoldFor("backward", message):
				walkBackwardFor(message)
			elif message == "right":
				turnRight()
			elif isHoldFor("right", message):
				turnRightFor(message)
			elif message == "left":
				turnLeft()
			elif isHoldFor("left", message):
				turnLeftFor(message)
			elif message == "jump":
				jump()
			elif isHoldFor("jump", message):
				jumpFor(message)
			elif message == "gags":
				gags()
			elif message == "tasks":
				tasks()
			elif message == "map":
				map()
			elif message == "friends":
				friends()
			elif message == "book":
				book()
			elif message == "delete":
				delete()
			elif message == "use feather":
				feather()
			elif message == "use megaphone":
				megaphone()
			elif message == "use lipstick":
				lipstick()
			elif message == "use bamboo cane":
				bambooCane()
			elif message == "use pixie dust":
				pixieDust()
			elif message == "use juggling balls":
				jugglingBalls()
			elif message == "use high dive":
				highDive()
			elif message == "use banana peel":
				bananaPeel()
			elif message == "use rake":
				rake()
			elif message == "use marbles":
				marbles()
			elif message == "use quicksand":
				quicksand()
			elif message == "use trapdoor":
				trapdoor()
			elif message == "use tnt":
				tnt()
			elif message == "use railroad":
				railroad()
			elif message == "use $1 bill":
				oneBill()
			elif message == "use small magnet":
				smallMagnet()
			elif message == "use $5 bill":
				fiveBill()
			elif message == "use big magnet":
				bigMagnet()
			elif message == "use $10 bill":
				Tenbill()
			elif message == "use hypno goggles":
				hypnoGoggles()
			elif message == "use presentation":
				presentation()
			elif message == "use bike horn":
				bikeHorn()
			elif message == "use whistle":
				whistle()
			elif message == "use bugle":
				bugle()
			elif message == "use aoogah":
				aoogah()
			elif message == "use elephant trunk":
				elephantTrunk()
			elif message == "use foghorn":
				foghorn()
			elif message == "use opera singer":
				operaSinger()
			elif message == "use cupcake":
				cupcake()
			elif message == "use fruit pie slice":
				fruitPieSlice()
			elif message == "use cream pie slice":
				creamPieSlice()
			elif message == "use whole fruit pie":
				wholeFruitPie()
			elif message == "use whole cream pie":
				wholeCreamPie()
			elif message == "use birthday cake":
				birthdayCake()
			elif message == "use wedding cake":
				weddingCake()
			elif message == "use squirting flower":
				squirtingFlower()
			elif message == "use glass of water":
				glassOfWater()
			elif message == "use squirt gun":
				squirtGun()
			elif message == "use seltzer bottle":
				seltzerBottle()
			elif message == "use fire hose":
				fireHose()
			elif message == "use storm cloud":
				stormCloud()
			elif message == "use geyser":
				geyser()
			elif message == "use flower pot":
				flowerPot()
			elif message == "use sandbag":
				sandbag()
			elif message == "use anvil":
				anvil()
			elif message == "use big weight":
				bigWeight()
			elif message == "use safe":
				safe()
			elif message == "use grand piano":
				grandPiano()
			elif message == "use toontanic":
				toontanic()
			elif message == "buy feather":
				buyFeather()
			elif message == "buy megaphone":
				buyMegaphone()
			elif message == "buy lipstick":
				buyLipstick()
			elif message == "buy bamboo cane":
				buyBambooCane()
			elif message == "buy pixie dust":
				buyPixieDust()
			elif message == "buy juggling balls":
				buyJugglingBalls()
			elif message == "buy high dive":
				buyHighDive()
			elif message == "buy banana peel":
				buyBananaPeel()
			elif message == "buy rake":
				buyRake()
			elif message == "buy marbles":
				buyMarbles()
			elif message == "buy quicksand":
				buyQuicksand()
			elif message == "buy trapdoor":
				buyTrapdoor()
			elif message == "buy tnt":
				buyTnt()
			elif message == "buy railroad":
				buyRailroad()
			elif message == "buy $1 bill":
				buyOneBill()
			elif message == "buy small magnet":
				buySmallMagnet()
			elif message == "buy $5 bill":
				buyFiveBill()
			elif message == "buy big magnet":
				buyBigMagnet()
			elif message == "buy $10 bill":
				buyTenbill()
			elif message == "buy hypno goggles":
				buyHypnoGoggles()
			elif message == "buy presentation":
				buyPresentation()
			elif message == "buy bike horn":
				buyBikeHorn()
			elif message == "buy whistle":
				buyWhistle()
			elif message == "buy bugle":
				buyBugle()
			elif message == "buy aoogah":
				buyAoogah()
			elif message == "buy elephant trunk":
				buyElephantTrunk()
			elif message == "buy foghorn":
				buyFoghorn()
			elif message == "buy opera singer":
				buyOperaSinger()
			elif message == "buy cupcake":
				buyCupcake()
			elif message == "buy fruit pie slice":
				buyFruitPieSlice()
			elif message == "buy cream pie slice":
				buyCreamPieSlice()
			elif message == "buy whole fruit pie":
				buyWholeFruitPie()
			elif message == "buy whole cream pie":
				buyWholeCreamPie()
			elif message == "buy birthday cake":
				buyBirthdayCake()
			elif message == "buy wedding cake":
				buyWeddingCake()
			elif message == "buy squirting flower":
				buySquirtingFlower()
			elif message == "buy glass of water":
				buyGlassOfWater()
			elif message == "buy squirt gun":
				buySquirtGun()
			elif message == "buy seltzer bottle":
				buySeltzerBottle()
			elif message == "buy fire hose":
				buyFireHose()
			elif message == "buy storm cloud":
				buyStormCloud()
			elif message == "buy geyser":
				buyGeyser()
			elif message == "buy flower pot":
				buyFlowerPot()
			elif message == "buy sandbag":
				buySandbag()
			elif message == "buy anvil":
				buyAnvil()
			elif message == "buy big weight":
				buyBigWeight()
			elif message == "buy safe":
				buySafe()
			elif message == "buy grand piano":
				buyGrandPiano()
			elif message == "buy toontanic":
				buyToontanic()
			elif message == "done shopping":
				doneShopping()
			elif message == "delete gag":
				deleteGag()
			elif message == "blam canyon":
				blamCanyon()
			elif message == "boingbury":
				boingbury()
			elif message == "bounceboro":
				bounceboro()
			elif message == "fizzlefield":
				fizzlefield()
			elif message == "gulp gulch":
				gulpGulch()
			elif message == "hiccup hills":
				hiccupHills()
			elif message == "kaboom cliffs":
				kaboomCliffs()
			elif message == "splashport":
				splashport()
			elif message == "splat summit":
				splatSummit()
			elif message == "thwackville":
				thwackville()
			elif message == "whoosh rapids":
				whooshRapids()
			elif message == "zoink falls":
				zoinkFalls()
			elif message == "welcome valley":
				welcomeValley()
			elif message == "teleport here":
				teleportHere()
			elif message == "go home":
				goHome()
			elif message == "back to playground":
				backToPlayGround()
			elif message == "goofy speedway":
				goofySpeedway()
			elif message == "toontown central":
				toontownCentral()
			elif message == "donalds dreamland":
				donaldsDreamland()
			elif message == "the brrrgh":
				theBrrrgh()
			elif message == "daisy gardens":
				daisyGardens()
			elif message == "minnies melodyland":
				minniesMelodyland()
			elif message == "donalds dock":
				donaldsDock()
			elif message == "chip n dales acorn acres":
				chipNDales()
			elif message == "friends close":
				closeFriends()
			elif message == "friends up":
				friendsUp()
			elif message == "friends down":
				friendsDown()
			elif message == "friends back":
				friendsPrev()
			elif message == "friends next":
				friendsNext()
			elif message == "friends 1":
				friends1()
			elif message == "friends 2":
				friends2()
			elif message == "friends 3":
				friends3()
			elif message == "friends 4":
				friends4()
			elif message == "friends 5":
				friends5()
			elif message == "friends 6":
				friends6()
			elif message == "friends 7":
				friends7()
			elif message == "friends 8":
				friends8()
			elif message == "toon friends":
				toonFriends()
			elif message == "toon go to":
				toonGoTo()
			elif message == "toon whisper":
				toonWhisper()
			elif message == "toon close":
				toonClose()
			elif message == "accept request":
				acceptRequest()
			elif message == "reject request":
				rejectRequest()
			elif message == "switch":
				switchDistrict()
			elif message == "dont switch":
				dontSwitchDistrict()
			else:
				typeMessage(message)
		else:
			if(time.time() - sinceLastInput >= 30.0):
				messageList.append({"user": "itspeachtea", "message": "jump"})




def twitch():
	def joinchat():
		Loading = True
		while Loading:
			readbuffer_join = irc.recv(1024)
			readbuffer_join = readbuffer_join.decode()
			for line in readbuffer_join.split("\n")[0:-1]:
				print(line)
				Loading = loadingComplete(line)

	def loadingComplete(line):
		if("End of /NAMES list" in line):
			print("Bot has joined " + CHANNEL + "'s channel!")
			sendMessage("room joined")
			return False
		else:
			return True

	def sendMessage(message):
		messageTemp = "PRIVMSG #" + CHANNEL + " :" + message + "\n"
		irc.send(messageTemp.encode())

	def getMessageDict(line):
		lineParts = line.split(":")
		message = lineParts[2]
		user = lineParts[1].split("!")[0]
		messageDict = {
			"user": user,
			"message": message
		}
		return messageDict

	def ifPing(line):
		return "PING" in line and "PRIVMSG" not in line

	joinchat()

	while True:
		try:
			readbuffer = irc.recv(1024).decode()
		except:
			readbuffer = ""
		for line in readbuffer.split("\r\n"):
			print(line)
			if line == "":
				continue
			elif(ifPing(line)):
				msg = "PONG tmi.twitch.tv\r\n".encode()
				irc.send(msg)
				print(msg)
				continue
			else:
				msg = getMessageDict(line)
				print(msg["user"] +": " +msg["message"])
				messageList.append(msg)

if __name__ == '__main__':
	thread1 = threading.Thread(target = twitch)
	thread2 = threading.Thread(target = gameControl)
	thread1.start()
	thread2.start()
