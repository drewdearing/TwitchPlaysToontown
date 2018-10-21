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
					return
			elif(size == 1):
				pyautogui.keyDown(key)
				pyautogui.keyUp(key)
				return
		typeMessage(message)

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

			if(command in movement["inputs"]):
				controlMovement(args, argsLength, message)
			elif(command == "turn"):
				controlTurning(args, argsLength, message)
			elif(command == "use"):
				useGag(args, argsLength, message)
			elif(command == "buy"):
				buyGag(args, argsLength, message)
			elif message == "show gags":
				showGags()
			elif message == "show tasks":
				showTasks()
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
				print(msg["user"] +": " +msg["message"])
				messageList.append(msg)

if __name__ == '__main__':
	thread1 = threading.Thread(target = twitch)
	thread2 = threading.Thread(target = gameControl)
	thread1.start()
	thread2.start()
