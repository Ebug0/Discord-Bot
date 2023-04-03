import random
import CheckPastMessage

def handle_response(message, channel, author) -> str:
    pmessage = message.lower()                                    #makes the message all lowercase characters for comparision

    if pmessage == "cum":
        return "Ben said that was a no no word"

    if author == "190245035567087626" and pmessage == "spinner":  #if james uses the spinner command it "breaks" on him and only display one value
        chance = random.randint(0,200)
        if chance == 100:
            return "James maybe you should take a break from the spinner command"

    if channel != "ebot-haven":                                   #checks to see if the same thing is said twice and if so send that message in the channel
        if CheckPastMessage.callpastmessage() == pmessage and CheckPastMessage.checkdupmessage(CheckPastMessage.callpastmessage()): 
            gifcheck = CheckPastMessage.callpastmessage()
            if gifcheck[:4] == "https":
                return "No Gifs"
            else:
                CheckPastMessage.storedupmessage(pmessage)
                return CheckPastMessage.callpastmessage()
        else:
            CheckPastMessage.storepastmessage(pmessage)
    
    if channel == "ebot-haven":                                   #makes the text commands only work in the desginated channel (ebot-haven)
        if pmessage == "hello":
            return "ebot says your a bitch"
    
        if pmessage == "roll":
            chance = random.randint(1,6)
            return chance
    
        if pmessage == 'help':
            return "`Help - Gives a list of commands and uses\nPut a ! before the command to have the answer DMed to you\nSpinner - gives 1 of 8 random reasons why mado didn't go to school \
                \nroll - Rolls a 6 sided die for you`"
    
        if pmessage == "spinner":
            chance = random.randint(1,12)
            if chance == 1:
                return "Mado was a little tired today :cry:"
            elif chance == 2:
                return "Mado had to get a 'Haircut'!"
            elif chance == 3:
                return "Mado slept through his alarm for the 10th time!"
            elif chance == 4:
                return "Mado ran out of hotdog buns :scream:"
            elif chance == 5:
                return "Mado's mom told him to stay home!"
            elif chance == 6:
                return "Mado got 'sick'!"
            elif chance == 7:
                return "Mado missed the bus!"
            elif chance == 8:
                return "Mado had to open a package for his mother!"
            elif chance == 9:
                return "Mado had to watch his baby sister for the day!"
            elif chance == 10:
                return "Mado just felt like it today"
            elif chance == 11:
                return "Mado had to go buy a bike today"
            elif chance == 12:
                return "Mado didn't have a choice"
