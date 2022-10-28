

pastmessage = ""
dupmessage = ""

def storepastmessage(message):
    global pastmessage
    pastmessage = message

def storedupmessage(message):
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

