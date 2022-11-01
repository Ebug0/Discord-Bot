

pastmessage = ""
dupmessage = ""

def storepastmessage(message): 
    global pastmessage
    pastmessage = message

def storedupmessage(message): #makes sure it doesnt repeat itself forever
    global dupmessage
    dupmessage = message

def checkdupmessage(message):
    global dupmessage
    if dupmessage == message:
        return False
    else:
        return True

def callpastmessage():
    global pastmessage
    return pastmessage

