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
		"inputs":{
			"up": {
				"key": "up"
			},
			"back": {
				"key": "down"
			},
			"right": {
				"key": "right"
			},
			"left": {
				"key": "left"
			},
			"jump": {
				"key": "ctrl"
			}
		}
	}

	gags = {
		"feather": {
			"buy": {
				"x": 780,
				"y": 288
			},
			"use": {
				"x": 650,
				"y": 316
			}
		},
		"megaphone": {
			"buy": {
				"x": 859,
				"y": 288
			},
			"use": {
				"x": 739,
				"y": 316
			}
		},
		"lipstick": {
			"buy": {
				"x": 938,
				"y": 228
			},
			"use": {
				"x": 828,
				"y": 316
			}
		},
		"bamboo cane": {
			"buy": {
				"x": 1017,
				"y": 288
			},
			"use": {
				"x": 913,
				"y": 316
			}
		},
		"pixie dust": {
			"buy": {
				"x": 1096,
				"y": 288
			},
			"use": {
				"x": 1000,
				"y": 316
			}
		},
		"juggling balls": {
			"buy": {
				"x": 1175,
				"y": 288
			},
			"use": {
				"x": 1090,
				"y": 316
			}
		},
		"high dive": {
			"buy": {
				"x": 1254,
				"y": 288
			},
			"use": {
				"x": 1177,
				"y": 316
			}
		},
		"banana peel": {
			"buy": {
				"x": 780,
				"y": 341
			},
			"use": {
				"x": 650,
				"y": 375
			}
		},
		"rake": {
			"buy": {
				"x": 859,
				"y": 341
			},
			"use": {
				"x": 739,
				"y": 375
			}
		},
		"marbles": {
			"buy": {
				"x": 938,
				"y": 341
			},
			"use": {
				"x": 828,
				"y": 375
			}
		},
		"quicksand": {
			"buy": {
				"x": 1017,
				"y": 341
			},
			"use": {
				"x": 913,
				"y": 375
			}
		},
		"trapdoor": {
			"buy": {
				"x": 1096,
				"y": 341
			},
			"use": {
				"x": 1000,
				"y": 375
			}
		},
		"tnt": {
			"buy": {
				"x": 1175,
				"y": 341
			},
			"use": {
				"x": 1090,
				"y": 375
			}
		},
		"railroad": {
			"buy": {
				"x": 1254,
				"y": 341
			},
			"use": {
				"x": 1177,
				"y": 375
			}
		},
		"1$ bill": {
			"buy": {
				"x": 780,
				"y": 394
			},
			"use": {
				"x": 650,
				"y": 433
			}
		},
		"small magnet": {
			"buy": {
				"x": 859,
				"y": 394
			},
			"use": {
				"x": 739,
				"y": 433
			}
		},
		"$5 bill": {
			"buy": {
				"x": 938,
				"y": 394
			},
			"use": {
				"x": 828,
				"y": 433
			}
		},
		"big magnet": {
			"buy": {
				"x": 1017,
				"y": 394
			},
			"use": {
				"x": 913,
				"y": 433
			}
		},
		"$10 bill": {
			"buy": {
				"x": 1096,
				"y": 394
			},
			"use": {
				"x": 1000,
				"y": 433
			}
		},
		"hypno goggles": {
			"buy": {
				"x": 1175,
				"y": 394
			},
			"use": {
				"x": 1090,
				"y": 433
			}
		},
		"presentation": {
			"buy": {
				"x": 1254,
				"y": 394
			},
			"use": {
				"x": 1177,
				"y": 433
			}
		},
		"bike horn": {
			"buy": {
				"x": 780,
				"y": 447
			},
			"use": {
				"x": 650,
				"y": 492
			}
		},
		"whistle": {
			"buy": {
				"x": 859,
				"y": 447
			},
			"use": {
				"x": 739,
				"y": 492
			}
		},
		"bugle": {
			"buy": {
				"x": 938,
				"y": 447
			},
			"use": {
				"x": 828,
				"y": 492
			}
		},
		"aoogah": {
			"buy": {
				"x": 1017,
				"y": 447
			},
			"use": {
				"x": 913,
				"y": 492
			}
		},
		"elephant trunk": {
			"buy": {
				"x": 1096,
				"y": 447
			},
			"use": {
				"x": 1000,
				"y": 492
			}
		},
		"foghorn": {
			"buy": {
				"x": 1175,
				"y": 447
			},
			"use": {
				"x": 1090,
				"y": 492
			}
		},
		"opera singer": {
			"buy": {
				"x": 1254,
				"y": 447
			},
			"use": {
				"x": 1177,
				"y": 492
			}
		},
		"cupcake": {
			"buy": {
				"x": 780,
				"y": 500
			},
			"use": {
				"x": 650,
				"y": 548
			}
		},
		"fruit pie slice": {
			"buy": {
				"x": 859,
				"y": 500
			},
			"use": {
				"x": 739,
				"y": 548
			}
		},
		"cream pie slice": {
			"buy": {
				"x": 938,
				"y": 500
			},
			"use": {
				"x": 828,
				"y": 548
			}
		},
		"whole fruit pie": {
			"buy": {
				"x": 1017,
				"y": 500
			},
			"use": {
				"x": 913,
				"y": 548
			}
		},
		"whole cream pie": {
			"buy": {
				"x": 1096,
				"y": 500
			},
			"use": {
				"x": 1000,
				"y": 548
			}
		},
		"birthday cake": {
			"buy": {
				"x": 1175,
				"y": 500
			},
			"use": {
				"x": 1090,
				"y": 548
			}
		},
		"wedding cake": {
			"buy": {
				"x": 1254,
				"y": 500
			},
			"use": {
				"x": 1177,
				"y": 548
			}
		},
		"squirting flower": {
			"buy": {
				"x": 780,
				"y": 553
			},
			"use": {
				"x": 650,
				"y": 608
			}
		},
		"glass of water": {
			"buy": {
				"x": 859,
				"y": 553
			},
			"use": {
				"x": 739,
				"y": 608
			}
		},
		"squirt gun": {
			"buy": {
				"x": 938,
				"y": 553
			},
			"use": {
				"x": 828,
				"y": 608
			}
		},
		"seltzer bottle": {
			"buy": {
				"x": 1017,
				"y": 553
			},
			"use": {
				"x": 913,
				"y": 608
			}
		},
		"fire hose": {
			"buy": {
				"x": 1096,
				"y": 553
			},
			"use": {
				"x": 1000,
				"y": 608
			}
		},
		"storm cloud": {
			"buy": {
				"x": 1175,
				"y": 553
			},
			"use": {
				"x": 1090,
				"y": 608
			}
		},
		"geyser": {
			"buy": {
				"x": 1254,
				"y": 553
			},
			"use": {
				"x": 1177,
				"y": 608
			}
		},
		"flower pot": {
			"buy": {
				"x": 780,
				"y": 606
			},
			"use": {
				"x": 650,
				"y": 664
			}
		},
		"sand bag": {
			"buy": {
				"x": 859,
				"y": 606
			},
			"use": {
				"x": 739,
				"y": 664
			}
		},
		"anvil": {
			"buy": {
				"x": 938,
				"y": 606
			},
			"use": {
				"x": 828,
				"y": 664
			}
		},
		"big weight": {
			"buy": {
				"x": 1017,
				"y": 606
			},
			"use": {
				"x": 913,
				"y": 664
			}
		},
		"safe": {
			"buy": {
				"x": 1096,
				"y": 606
			},
			"use": {
				"x": 1000,
				"y": 664
			}
		},
		"grand piano": {
			"buy": {
				"x": 1175,
				"y": 606
			},
			"use": {
				"x": 1090,
				"y": 675
			}
		},
		"toontanic": {
			"buy": {
				"x": 1254,
				"y": 606
			},
			"use": {
				"x": 1177,
				"y": 675
			}
		}
	}

	def controlMovement(args, size, message):
		direction = args[0]
		if(size > 0 and direction in movement["inputs"]):
			key = movement["inputs"][direction]["key"]
			if(size == 2):
				try:
					t = float(args[1])
				except:
					t = 0.0
				if(t > 0):
					newThread = threading.Thread(target = holdKey, args=(key, t))
					newThread.start()
					return
			elif(size == 1):
				pyautogui.keyDown(key)
				pyautogui.keyUp(key)
				return
		typeMessage(message)

	def holdKey(key, seconds):
		seconds = min(seconds, 30.0)
		pyautogui.keyDown(key)
		time.sleep(seconds)
		pyautogui.keyUp(key)

	def controlTurning(args, size, message):
		if size > 1:
			direction = args[1]
			if(direction == "left" or direction == "right"):
				controlMovement(args[1:], size - 1, message)
				return
		typeMessage(message)

	def useGag(args, size, message):
		if(size > 1):
			gag = " ".join(args[1:])
			if(gag in gags):
				coordX = gags[gag]["use"]["x"]
				coordY = gags[gag]["use"]["y"]
				pyautogui.moveTo(coordX, coordY)
				clickMouse()
				return
		typeMessage(message)

	def buyGag(args, size, message):
		if(size > 1):
			try:
				x = int(args[size-1])
			except:
				x = -1
			if(x >= 0):
				gag = " ".join(args[1:(size-1)])
			else:
				gag = " ".join(args[1:])
				x = 1
			if(gag in gags):
				coordX = gags[gag]["buy"]["x"]
				coordY = gags[gag]["buy"]["y"]
				for i in range(x):
					pyautogui.moveTo(coordX, coordY)
					clickMouse()
				return
		typeMessage(message)

	def showGags():
		if (inGags):
			pyautogui.keyUp('home')
			inGags = False
		else:
			if(inTasks):
				tasks()
			pyautogui.keyDown('home')
			inGags = True

	def showTasks():
		if (inTasks):
			pyautogui.keyUp('end')
			inTasks = False
		else:
			if(inGags):
				gags()
			pyautogui.keyDown('end')
			inTasks = True

	def inUnsafeClickBounds():
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
			args = message.split(" ")
			argsLength = len(args)
			command = args[0]

			print("reading " + message)

			if(command in movement["inputs"]):
				controlMovement(args, argsLength, message)
			elif(command == "turn"):
				controlTurning(args, argsLength, message)
			elif(command == "use"):
				useGag(args, argsLength, message)
			elif(command == "buy"):
				buyGag(args, argsLength, message)
			elif message == "gags":
				showGags()
			elif message == "tasks":
				showTasks()
			elif message == "map":
				map()
			elif message == "friends":
				friends()
			elif message == "book":
				book()
			elif message == "delete":
				delete()
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
