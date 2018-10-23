import socket
import pyautogui
import threading
import time
import json
from auth import login

SERVER = "irc.twitch.tv"
PORT = 6667
PASS = login()
BOT = "PeachBot"
CHANNEL = "itspeachtea"
OWNER = "itspeachtea"

messageList = []
inTasks = False
inGags = False

irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send((
	"PASS "+ PASS + "\n" + 
	"NICK " + BOT + "\n" +
	"JOIN #" + CHANNEL + "\n"
	).encode())

def gameControl():
	monitorSize = pyautogui.size()
	sinceLastInput = time.time()

	with open('gags.json') as f:
		gags = json.load(f)

	with open('unsafeBounds.json') as f:
		unsafeBounds = json.load(f)

	with open('movement.json') as f:
		movement = json.load(f)

	with open('keys.json') as f:
		keys = json.load(f)

	with open('mouseLocations.json') as f:
		mouseLocations = json.load(f)

	with open('mouse.json') as f:
		mouseDirections = json.load(f)

	def holdKey(key, seconds):
		seconds = min(seconds, 30.0)
		pyautogui.keyDown(key)
		time.sleep(seconds)
		pyautogui.keyUp(key)

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
					return True
			elif(size == 1):
				pyautogui.keyDown(key)
				pyautogui.keyUp(key)
				return True
		return False

	def controlMovement(args, size, message):
		direction = message
		t = 0
		if(size > 1):
			try:
				t = float(args[size-1])
			except:
				t = 0
			if(t > 0):
				direction = " ".join(args[:(size-1)])
		if(direction in movement["inputs"]):
			key = movement["inputs"][direction]["key"]
			if(t > 0):
				newThread = threading.Thread(target = holdKey, args=(key, t))
				newThread.start()
				return True
			else:
				pyautogui.keyDown(key)
				pyautogui.keyUp(key)
				return True
		return False

	def useGag(args, size, message):
		if(size > 1):
			gag = " ".join(args[1:])
			if(gag in gags):
				coordX = gags[gag]["use"]["x"]
				coordY = gags[gag]["use"]["y"]
				pyautogui.moveTo(coordX, coordY)
				clickMouse()
				return True
		return False

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
				return True
		return False

	def controlShow(args, size, message):
		if(size == 2):
			name = args[1]
			if(name == "gags"):
				showGags()
				return True
			elif(name == "tasks"):
				showTasks()
				return True
		return False

	def controlHide(args, size, message):
		if(size == 2):
			name = args[1]
			if(name == "gags"):
				hideGags()
				return True
			elif(name == "tasks"):
				hideTasks()
				return True
		return False

	def showGags():
		global inGags
		global inTasks
		if (inGags):
			hideGags()
		if (inTasks):
			hideTasks()
		pyautogui.keyDown('home')
		inGags = True

	def showTasks():
		global inGags
		global inTasks
		if (inTasks):
			hideTasks()
		if (inGags):
			hideGags()
		pyautogui.keyDown('end')
		inTasks = True

	def hideGags():
		global inGags
		if(inGags):
			pyautogui.keyUp('home')
			inGags = False

	def hideTasks():
		global inTasks
		if(inTasks):
			pyautogui.keyUp('end')
			inTasks = False

	def inUnsafeClickBounds():
		posx, posy = pyautogui.position()
		for bound in unsafeBounds:
			if (posx >= bound["xMin"] and
				posx <= bound["xMax"] and
				posy >= bound["yMin"] and
				posy <= bound["yMax"]):
				return True
		return False

	def controlMouse(args, size, message):
		direction = " ".join(args[1:])
		x = -1
		y = -1
		t = 1
		if(size > 2):
			try:
				x = min(int(args[size - 2]), 1919)
			except:
				x = -1
			try:
				y = min(int(args[size - 1]), 1079)
			except:
				y = -1
			if(x > 0 and y > 0):
				direction = " ".join(args[1:(size - 2)])
			elif(y > 0):
				direction = " ".join(args[1:(size - 1)])
				t = y
			else:
				return False
		if(direction == "click"):
			for i in range(min(t, 15)):
				clickMouse()
			return True
		elif(direction == "to"):
			if(x > 0 and y > 0):
				pyautogui.moveTo(x, y)
				return True
		elif(direction == "hold"):
			mouseDown()
			return True
		elif(direction == "release"):
			mouseUp()
			return True
		elif(direction in mouseDirections["inputs"]):
			speed = t * mouseDirections["speed"]
			mouseDirX = speed * mouseDirections["inputs"][direction]["x"]
			mouseDirY = speed * mouseDirections["inputs"][direction]["y"]
			if(mouseDirX == 0):
				mouseDirX = None
			if(mouseDirY == 0):
				mouseDirY = None
			pyautogui.moveRel(mouseDirX, mouseDirY)
			posx, posy = pyautogui.position()
			print(str(posx)+", "+str(posy))
			return True
		return False

	def mouseDown():
		if(inUnsafeClickBounds()):
			print("WARNING: unsafe click detected")
			return False
		else:
			pyautogui.mouseDown()
			return True

	def mouseUp():
		pyautogui.mouseUp();

	def clickMouse():
		if(mouseDown()):
			mouseUp()

	def keyPress(message):
		key = keys["inputs"][message]["key"]
		pyautogui.keyDown(key)
		pyautogui.keyUp(key)

	def mouseLocation(message):
		location = mouseLocations["inputs"][message]
		pyautogui.moveTo(location['x'], location['y'])
		clickMouse()

	def typeMessage(message):

		pyautogui.typewrite(message, interval=0.01)
		pyautogui.keyDown("enter")
		pyautogui.keyUp("enter")

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

			if(controlMovement(args, argsLength, message)):
				pass
			elif(command == "use" and useGag(args, argsLength, message)):
				pass
			elif(command == "buy" and buyGag(args, argsLength, message)):
				pass
			elif(command == "mouse" and controlMouse(args, argsLength, message)):
				pass
			elif (command == "show" and controlShow(args, argsLength, message)):
				pass
			elif (command == "hide" and controlHide(args, argsLength, message)):
				pass
			elif(message in keys["inputs"]):
				keyPress(message)
			elif(message in mouseLocations["inputs"]):
				mouseLocation(message)
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
				if(msg["user"] != "nightbot"):
					print(msg["user"] +": " +msg["message"])
					messageList.append(msg)

if __name__ == '__main__':
	thread1 = threading.Thread(target = twitch)
	thread2 = threading.Thread(target = gameControl)
	thread1.start()
	thread2.start()
