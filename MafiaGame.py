from Classes import Player
import random
from collections import OrderedDict
import statistics
def mafiachooser(playerlist, playerdict, mafcount):
    mafnumbers = [] 
    
    for i in range (0,mafcount):
        chance = random.randint(0, len(playerlist)-1)                                                   #creates a random number within the index of the playerlist
        while chance in mafnumbers:                                                                     #if that index is already taken by then it randomly creates another one until its not in the list
            chance = random.randint(0,len(playerlist)-1)
        mafnumbers.append(chance)                                                                       #adds the index to list of mafia for call back later
        playerdict[playerlist[chance]].changerole("mafia")                                              #changes a players role to mafia 
    return mafnumbers 
def sherifchooser(positionnumbers, playerdict, playerlist):
    
    chance = random.randint(0, len(playerlist)-1) 
    while chance in positionnumbers:
        chance = random.randint(0,len(playerdict)-1)
    playerdict[playerlist[chance]].changerole("sheriff")
    sherifnumber = chance                                                                               #puts the index of the sherifnumber in a variable for later callback
    return sherifnumber
def doctorchooser(positionnumbers, playerdict, playerlist):
    chance = random.randint(0,len(playerlist)-1)
    while chance in positionnumbers:
        chance = random.randint(0,len(playerlist)-1)
    playerdict[playerlist[chance]].changerole("doctor")                                                 #same as above but for the doctor role
    docnumber = chance
    return docnumber
def mafiaturn(mafnumber,playerdict,playerlist):
    for i in mafnumber:
        print(f"Mafia {playerlist[i]} who do you wish to kill?")                                        #each mafia gets to vote on how they wish to kill
        print("Here is who you can kill")
        for o in range (0,len(playerlist)):
            if playerlist[i] == playerlist[o]:                                                          #tells the player they can't kill themselves
                print("You can't kill yourself")
            elif playerdict[playerlist[o]].role == "mafia":                                             #lets them know who are fellow mafia members
                print(f"Can't kill {playerlist[o]} because they are a fellow mafia")
            elif playerdict[playerlist[o]].status == "alive":                                           #shows the rest of the players who are still alive
                print(f"Name: {playerlist[o]} enter {o} to kill")
        killchoice = int(input("Enter in the number of the person you wish to kill: "))
        if killchoice in mafnumber or killchoice >= len(playerlist)-1 or killchoice < 0:                #makes sure they don't enter an invalid answer and if they do forfit it
            print("You entered an invalid choice your vote is forfit")
            
        else:
            playerdict[playerlist[killchoice]].changevote(1,False)                                      #adds one to the vote for the player they which to kill
def doctorturn(docnumber, playerdict, playerlist):
    print(f"Doctor {playerlist[docnumber]} who do you wish to save")
    for i in range (0,len(playerlist)):
        if i == docnumber:                                                                              #same as mafia except that they get to save a person and that gets changed in the object
            print(f"To save yourself enter {i}")
        elif playerdict[playerlist[i]].status == "alive":
            print(f"Name: {playerlist[i]} Enter {i} to save this person")
    savechoice = int(input("Enter in who you wish to save: "))
    if savechoice >= len(playerlist)-1 or savechoice < 0:
        print("You entered an invalid choice your save is forfit")
    else:
        playerdict[playerlist[savechoice]].changesafe("safe")
def sherifturn(sherifnumber, playerdict, playerlist):
    print(f"Sherif {playerlist[sherifnumber]} Please choose who you wish to investigate")
    for i in range (0,len(playerlist)):                                                                 #same as above except they are investigating a person to find out their role
        if i == sherifnumber:
            print("You can't invetegate yourself")
        elif playerdict[playerlist[i]].invest == True and playerdict[playerlist[i]].status == "alive":  #if the sherif already investagted them it lets them know what their role was
            print(f"You already Investgated {playerlist[i]} and there role is {playerdict[playerlist[i]].role}")
        elif playerdict[playerlist[i]] == "alive":
            print(f"Name: {playerlist[i]} Enter {i} to investigate this person")
    
    investchoice = int(input("Please enter the number of the person you wish to investigate: "))
    #sherifturn function not done yet
    
    if investchoice >= len(playerlist)-1 or investchoice < 0:
        print(f"You entered an invalid choice and you can't investigate them")
    else:
        playerdict[playerlist[investchoice]].changeinvest(True)

def rankDictionary(data):
    temp = {}
    for i in data:
        temp[i] = sorted(data[i])
    
    return temp

def playervote(playerdict,playerlist):
    votelist = []
    print("It's time to vote")
    for i in range(0,len(playerlist)):
        print(f"Who do you wish to vote?", (playerlist[i]))
        for o in range (0,len(playerlist)):
            if playerlist[i] == playerlist[o]:                                                          
                print("You can't vote yourself")
            elif playerdict[playerlist[o]].status == "alive":
                print(f"Name: {playerlist[o]} enter {o} to kill")
        killchoice = int(input("Enter the number of the person you want to kill "))
        
        votelist.append(killchoice)
        deadlist = []
        for i in playerdict:
            if playerdict[i].status == ("dead"):
                deadlist.append(i)
        if killchoice in deadlist:
            print("You entered an invalid choice and your vote is forfit")
        else:
            playerdict[playerlist[killchoice]].changevote(1,False)
            
    for i in playerlist:
        if playerdict[i].vote > 0:
                votelist.append(i)
                if len(votelist) == 0:
                    print("Everyone voted for themselves for some reason and wasted their vote")
                    return
        
        else:
            modelist = []
            modelist = statistics.multimode(votelist)
            result = statistics.multimode(votelist)
            playerdict[playerlist[result[0]]].changestatus("dead")
            
    if len(modelist) >= 2:
        print("Nobody dies because there was a tie")
        playerdict[playerlist[modelist[0]]].changestatus("alive") 
        playerdict[playerlist[modelist[1]]].changestatus("alive")
        playerdict[playerlist[modelist[2]]].changestatus("alive")  
    print("These people tied in votes", modelist)
    print("The votes were", votelist)
    for i in playerlist:
            playerdict[i].changesafe("")
            playerdict[i].changevote(0, True)
        
           


def endOfTurn(playerdict,playerlist):
    votecount = []
    print("The turn has ended") #If the player has the most votes, change status in object to dead 
    
    for i in playerlist:
        if playerdict[i].vote > 0:
            votecount.append(i)
    print(votecount)
    if len(votecount) == 1 and playerdict[votecount[0]].safe != "safe":
        playerdict[votecount[0]].changestatus("dead")
    elif len(votecount) == 0:
        print("The Mafia is an idiot and tried to kill someone he couldn't")
        return
    else:
        for i in votecount:
            if playerdict[i].vote >= 2:
                playerdict[i].changestatus("dead")
            else:
               tiebreaker =  random.randint(0,len(votecount)-1)
            if playerdict[i].safe == "safe":
                playerdict[i].changestatus("alive")  
            else:
                print("The Mafia killed", tiebreaker)
                playerdict[votecount[tiebreaker]].changestatus("dead")
                break
    for i in playerlist:
        playerdict[i].changesafe("")
        playerdict[i].changevote(0, True)








if __name__ == "__main__":
    #players = input("Please enter mafia plus the name of the player with a space inbetween: ") #gets a list of players
    players = "m Ethan Mado Vejay Mason Ben Jace Ty" #temp mesaure to make testing quicker
    #mafcount = int(input("Enter in how many maffia members you wish to have: ")) 
    mafcount = 2 #same thing as above
    templist = players.split()                                                                  #breaks up the full string of players and makes it into a list
    mafnumber = []
    positionsnumber = []
    playerlist = templist[1:]                                                                   #gets rid of the mafia invoke text
    playerdict = {name: Player("alive", "none") for name in playerlist}                         #makes each player in the list a object in a dictionary to be called later
    mafnumber = mafiachooser(playerlist, playerdict, mafcount)                                  #sets the special roles for the players that get them which the function
    positionsnumber = mafnumber.copy()                                                          #A list of which index of playerlist has a roll
    sherifnumber = sherifchooser(positionsnumber, playerdict, playerlist)   
    positionsnumber.append(sherifnumber)
    docnumber = doctorchooser(positionsnumber, playerdict, playerlist)                          #docnumber and sherifnumber is to be able to call those players in the future for their turns
    positionsnumber.append(docnumber)
    for i in range (0, len(playerlist)):
        if i not in positionsnumber:                                                            #anyplayer that did not get a special role gets the default role
            playerdict[playerlist[i]].changerole("bystander")
    #mafiaturn(mafnumber, playerdict, playerlist)
    #doctorturn(docnumber, playerdict, playerlist)
    #sherifturn(sherifnumber, playerdict, playerlist)
    playervote(playerdict,playerlist)
    #endOfTurn(playerdict,playerlist)
    
    
    for i in playerlist:                                                                        #just to help debug which objects have which values at the end of game (dev only)
        print(playerdict[i].display())