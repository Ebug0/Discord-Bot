import random
import CheckPastMessage
import time
from collections import defaultdict
import Scoreboard

# Rate limiting for 67 command
command_67_cooldowns = defaultdict(float)

def handle_response(message, channel, author, username=None) -> str:
    pmessage = message.lower()                                    #makes the message all lowercase characters for comparision
    chance = random.randint(0,200)
    if pmessage == "cum":
        return "Ben said that was a no no word"

    if author == "190245035567087626" and chance == 100:  #give james a random chance to get a nice message :)
        return "Hi James hope your having a great day!"
    
    if author == "498995283481460786" and chance == 100: #for chucky
        return "Get back to drawing, Chucky."
    
    if author == "227929692353593345" and chance == 100: #for Floppa
        return "Straight up flopping my comrade."
    
    if author == "321800487982858241" and chance == 100: #for Jace
        return "What a cool dog, probably a good Sol Badguy main too."
    
    if author == "325342729494200340" and chance == 100: #for Burger
        return "I'm going to sue your ass Burger"
    
    if author == "293860346790412288" and chance == 100: #for Ben
        return "Hawk 2a respect button Ben ----->"
    
    if author == "293942718801903617" and chance == 100: #for Ty
        return "Don't forget to eat your protein today Ty"
    
    if author == "289200162121842695" and chance == 100: #for Mado
        return "I'll get back to you soon Amado (AST)"
    
    if author == "660284556385058817" and chance == 100: #for Gavin
        return "Bruh bro wut damn Gavin"
    
    if author == "461137261073793034" and chance == 100: #for Tanon
        return "Even a black ball room dancer got a Tanon"

    if "ebot" not in channel:                                   #checks to see if the same thing is said twice and if so send that message in the channel
        if CheckPastMessage.callpastmessage() == pmessage and CheckPastMessage.checkdupmessage(CheckPastMessage.callpastmessage()): 
            gifcheck = CheckPastMessage.callpastmessage()
            if gifcheck[:5] == "https":
                return
            if gifcheck[0] == "<":
                return
            else:
                CheckPastMessage.storedupmessage(pmessage)
                return CheckPastMessage.callpastmessage()
        else:
            CheckPastMessage.storepastmessage(pmessage)

    if "ebot" in channel:                                   #makes the text commands only work in the desginated channel (ebot-haven)
        if pmessage == "hello":
            return "ebot says you're a bitch"
    
        if pmessage == "roll":
            chance = random.randint(1,6)
            return chance

        if pmessage == "67":
            current_time = time.time()
            last_used = command_67_cooldowns[author]
            if current_time - last_used < 1:  # 1 second cooldown
                return  # Silently ignore if rate limited
            command_67_cooldowns[author] = current_time
            # Track scoreboard count
            if username:
                Scoreboard.increment_count(author, username)
            return "67"    
    
        if pmessage == 'help':
            return "`Help - Gives a list of commands and uses\nPut a ! before the command to have the answer DMed to you\nSpinner - gives 1 of 8 random reasons why mado didn't go to school \
                \nroll - Rolls a 6 sided die for you`"
    
        if pmessage == "spinner":
            chance = random.randint(1,16)
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
            elif chance == 13:
                return "Mado had to cut his hamburger!"
            elif chance == 14:
                return "James rubbed peanut butter on Mado!"
            elif chance == 15:
                return "Mado stayed on TikTok!"
            elif chance == 16:
                return "Mado hit a deer!"
                
