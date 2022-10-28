import random
import CheckPastMessage

def handle_response(message, channel) -> str:
    pmessage = message.lower()

    if CheckPastMessage.callpastmessage() == pmessage and CheckPastMessage.checkdupmessage(CheckPastMessage.callpastmessage()):
        CheckPastMessage.storedupmessage(pmessage)
        return CheckPastMessage.callpastmessage()
    else:
        CheckPastMessage.storepastmessage(pmessage)
    
    if channel == "ebot-haven":
        if pmessage == "hello":
            return "bitch"
    
        if pmessage == "roll":
            chance = random.randint(1,6)
            return chance
    
        if pmessage == 'help':
            return "`Help - Gives a list of commands and uses\nPut a ! before the command to have the answer DMed to you\nSpinner - gives 1 of 8 random reasons why mado didn't go to school \
                \nroll - Rolls a 6 sided die for you`"
    
        if pmessage == "spinner":
            chance = random.randint(1,8)
            if chance == 1:
                return "Mado was a little tired today :cry:"
            elif chance == 2:
                return "Mado had to get a 'Haircut'"
            elif chance == 3:
                return "Mado slept through his alarm for the 5th time"
            elif chance == 4:
                return "Mado ran out of hotdog buns :scream:"
            elif chance == 5:
                return "Mado's mom told him to stay home"
            elif chance == 6:
                return "Mado got 'sick'"
            elif chance == 7:
                return "Mado missed the bus"
            elif chance == 8:
                return "Mado had to open a package for his mother"
