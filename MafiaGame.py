from Classes import Player
import random

def mafiachooser(playerlist, playerdict, mafcount):
    mafnumbers = []
    for i in range (0,mafcount):
        chance = random.randint(0, len(playerlist)-1)
        if chance in mafnumbers:
            while chance in mafnumbers:
                chance = random.randint(0,len(playerlist)-1)
        mafnumbers.append(chance)
        playerdict[playerlist[chance]].changerole("mafia")

    return mafnumbers 

def sherifchooser(positionnumbers, playerdict, playerlist):
    chance = random.randint(0, len(playerlist)-1)
    while chance in positionnumbers:
        chance = random.randint(0,len(playerdict)-1)
    playerdict[playerlist[chance]].changerole("sherif")
    sherifnumber = chance

    return sherifnumber

def doctorchooser(positionnumbers, playerdict, playerlist):
    chance = random.randint(0,len(playerlist)-1)
    while chance in positionnumbers:
        chance = random.randint(0,len(playerlist)-1)
    playerdict[playerlist[chance]].changerole("doctor")
    docnumber = chance

    return docnumber


if __name__ == "__main__":
    players = input("Please enter mafia plus the name of the player with a space inbetween: ")
    mafcount = int(input("Enter in how many maffia members you wish to have: "))
    templist = players.split()
    playerlist = templist[1:]
    playerdict = {name: Player("alive", "none") for name in playerlist}

    mafnumber = mafiachooser(playerlist, playerdict, mafcount)
    positionsnumber = mafnumber
    sherifnumber = sherifchooser(positionsnumber, playerdict, playerlist)
    positionsnumber.append(sherifnumber)
    docnumber = doctorchooser(positionsnumber, playerdict, playerlist)
    positionsnumber.append(docnumber)
    
    for i in range (0, len(playerlist)):
        if i not in positionsnumber:
            playerdict[playerlist[i]].changerole("bystander")







    for i in playerlist:
        print(f"Name: {i} Role: {playerdict[i].role} Status: {playerdict[i].status}")

