from os import kill
from pickle import FALSE
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

def mafiaturn(mafnumber,playerdict,playerlist):
    for i in mafnumber:
        print(f"Mafia {playerlist[i]} who do you wish to kill?")
        print("Here is who you can kill")
        for o in range (0,len(playerlist)):
            if playerdict[playerlist[o]].status == "alive" and playerlist[i] != playerlist[o]:
                print(f"Name: {playerlist[o]} enter {o} to kill")
            elif playerdict[playerlist[o]].role == "mafia":
                print(f"Can't kill {playerlist[o]} because they are a fellow mafia")
        killchoice = int(input("Enter in the number of the person you wish to kill: "))
        if killchoice in mafnumber or killchoice > len(playerlist)-1 or killchoice < 0:
            print("You entered an invalid choice your vote is forfit")
        playerdict[playerlist[killchoice]].changevote(1,FALSE)
    

if __name__ == "__main__":
    #players = input("Please enter mafia plus the name of the player with a space inbetween: ")
    players = "m Ethan Mado Vejay Mason Ben Jace Ty"
    #mafcount = int(input("Enter in how many maffia members you wish to have: "))
    mafcount = 2
    templist = players.split()
    mafnumber = []
    positionsnumber = []
    playerlist = templist[1:]
    playerdict = {name: Player("alive", "none") for name in playerlist}

    mafnumber = mafiachooser(playerlist, playerdict, mafcount)  #sets the roles for each player
    positionsnumber = mafnumber.copy()   #A list of which index of playerlist has a roll
    sherifnumber = sherifchooser(positionsnumber, playerdict, playerlist)
    positionsnumber.append(sherifnumber)
    docnumber = doctorchooser(positionsnumber, playerdict, playerlist)
    positionsnumber.append(docnumber)
    for i in range (0, len(playerlist)):
        if i not in positionsnumber:
            playerdict[playerlist[i]].changerole("bystander")

    mafiaturn(mafnumber, playerdict, playerlist)




    for i in playerlist:
        print(f"Name: {i} Role: {playerdict[i].role} Status: {playerdict[i].status}")

