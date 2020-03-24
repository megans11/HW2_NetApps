import sys
import pymongo
import time
from datetime import datetime

client = pymongo.MongoClient()
db = client.test

command = input("Enter command: ")

dateTimeObj = datetime.now()
timeObj = dateTimeObj.time()
print('[Checkpoint 01:', timeObj, '] Message captured: ', command)

commandDict = {}
if command[0:2] == 'p:':
	commandDict['type'] = 'produce'
elif command[0:2] == 'c:':
	commandDict['type'] = 'consume'
else:
	print("Wrong format")
	
if command.index('+') != -1: # Get place
	place = command[command.index(':')+1:command.index('+')]
	commandDict['place'] = place

if commandDict['type'] == 'produce':
	subject = command[command.index('+')+1:command.index('"')-1] # Get subject
	message = command[command.index('"'):] # Get message
	commandDict['subject'] = subject
	commandDict['message'] = message
elif commandDict['type'] == 'consume':
	subject = command[command.index('+')+1:]
	commandDict['subject'] = subject
	commandDict['message'] = "n/a"

msgID = "17$" + str(time.time())
if commandDict['type'] == 'produce':
	mongoDocument = {
		"Action": "p",
		"Place": commandDict['place'],
		"MsgID": msgID, 
		"Subject": commandDict['subject'], 
		"Message": commandDict['message'] }	
elif commandDict['type'] == 'consume':
	mongoDocument = {
		"Action": "c",
		"Place": commandDict['place'],
		"MsgID": msgID, 
		"Subject": commandDict['subject'], 
		"Message": commandDict['message'] }	
		
dateTimeObj = datetime.now()
timeObj = dateTimeObj.time()
print('[Checkpoint 02:', timeObj, '] Store command in MongoDB instance: ', mongoDocument)

db.utilization.insert(mongoDocument)

