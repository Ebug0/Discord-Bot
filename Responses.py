import random

def handle_response(message: str) -> str:
    pmessage = message.lower()
    
    if pmessage == "hello":
        return "bitch"
    
    if pmessage == "roll":
        return "4"
    
    if pmessage == '!help':
        return "`Placeholder help text`"
    
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
            return "`placeholder text`"
        elif chance == 8:
            return "`placeholder text`"



