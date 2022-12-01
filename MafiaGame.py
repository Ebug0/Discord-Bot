from Classes import Player
import random
import statistics
from Client import client
from Token import TOKEN
from discord.commands import *
from discord.ui import *
import discord
import asyncio

ctx = None



async def send_message(message, interaction = None, private = False):
    global ctx
    if interaction != None:
        private = True

    if private == True:
        await interaction.user.send(message)
    else:
        await ctx.send(message)

async def mafiachooser(playerlist, playerdict, mafcount):
    mafnumbers = []

    for i in range (0,mafcount):
        chance = random.randint(0, len(playerlist)-1)                                                   #creates a random number within the index of the playerlist
        while chance in mafnumbers:                                                                     #if that index is already taken by then it randomly creates another one until its not in the list
            chance = random.randint(0,len(playerlist)-1)
        mafnumbers.append(chance)                                                                       #adds the index to list of mafia for call back later
        await send_message( f"You have been picked as a mafia!", playerdict[playerlist[i]].id, True)
        playerdict[playerlist[chance]].changerole("mafia")                                              #changes a players role to mafia 
    
    return mafnumbers 

async def sherifchooser(positionnumbers, playerdict, playerlist):
    
    chance = random.randint(0, len(playerlist)-1) 
    while chance in positionnumbers:
        chance = random.randint(0,len(playerdict)-1)
    playerdict[playerlist[chance]].changerole("sheriff")
    sherifnumber = chance                                                                               #puts the index of the sherifnumber in a variable for later callback
    await send_message("You have been chosen as the Sherif!", playerdict[playerlist[sherifnumber]].id, True)
    return sherifnumber
    
async def doctorchooser(positionnumbers, playerdict, playerlist):
    chance = random.randint(0,len(playerlist)-1)
    while chance in positionnumbers:
        chance = random.randint(0,len(playerlist)-1)
    playerdict[playerlist[chance]].changerole("doctor")                                                 #same as above but for the doctor role
    docnumber = chance
    await send_message("You have been chosend as the doctor!", playerdict[playerlist[docnumber]].id, True)
    return docnumber

async def mafiaturn(mafnumber,playerdict,playerlist):
    await send_message("Mafia turn start")
    for i in mafnumber:
        if len(mafnumber) == 2:
            await send_message(f"Each mafia member will vote seperatly, in case of a tie it will be random\nmake sure to talk to your fellow mafia members via dm \
            your fellow mafia members are {playerlist[0]} and {playerlist[1]}", playerdict[playerlist[i]])
        elif len(mafnumber) == 3:
            await send_message(f"Each mafia member will vote seperatly in case of a tie it will be random\nmake sure to talk to your fellow mafia members via dm \
            your fellow mafia members are {playerlist[0]}, {playerlist[1]} and {playerlist[2]}", playerdict[playerlist[i]])
        else:
            await send_message("Your a lone mafia good luck", playerdict[playerlist[i]])
    for i in mafnumber:
        if playerdict[playerlist[i]].status == "dead":
            await send_message("You are dead and can not act", playerdict[playerlist[i]].id)
        else:
            await send_message(f"Mafia {playerlist[i]} who do you wish to kill?\nHere is who you can kill", playerdict[playerlist[i]].id, True) #each mafia gets to vote on how they wish to kill
            for o in range (0,len(playerlist)):
                if playerlist[i] == playerlist[o]:                                                          #tells the player they can't kill themselves
                    await send_message("You can't kill yourself", playerdict[playerlist[i]].id, True)
                elif playerdict[playerlist[o]].role == "mafia":                                             #lets them know who are fellow mafia members
                    await send_message(f"Can't kill {playerlist[o]} because they are a fellow mafia", playerdict[playerlist[i]].id, True)
                elif playerdict[playerlist[o]].status == "alive":                                           #shows the rest of the players who are still alive
                    await send_message(f"Name: {playerlist[o]} enter {o} to kill", playerdict[playerlist[i]].id, True)

            killchoice = None
            await send_message("Please enter who you want to kill", playerdict[playerlist[i]].id)
            await asyncio.sleep(0.5)
            def check(m):
                return m.author == playerdict[playerlist[i]].id.user

            message = await client.wait_for("message", check=check)
            print("got past for message")
            try:
                killchoice = int(message.content)
            except:
                await send_message("A mafia sent a non number vote this round and their vote is forfit")
                break
            
            if killchoice in mafnumber or killchoice >= len(playerlist)-1 or killchoice < 0:                #makes sure they don't enter an invalid answer and if they do forfit it
                await send_message("A mafia sent an invalid choice for their vote. Dumbass")
            else:
                playerdict[playerlist[killchoice]].changevote(1,False)                                      #adds one to the vote for the player they which to kill
                print("added vote")
    await send_message("Mafia turn over")
            
async def doctorturn(docnumber, playerdict, playerlist):
    await send_message("Doc turn start")
    await send_message(f"Doctor {playerlist[docnumber]} who do you wish to save", playerdict[playerlist[docnumber]].id, True)
    for i in range (0,len(playerlist)):
        if i == docnumber:                                                                              #same as mafia except that they get to save a person and that gets changed in the object
            await send_message(f"To save yourself enter {i}", playerdict[playerlist[docnumber]].id)
        elif playerdict[playerlist[i]].status == "alive":
            await send_message(f"Name: {playerlist[i]} Enter {i} to save this person", playerdict[playerlist[docnumber]].id)
    savechoice = None
    
    await asyncio.sleep(0.5)
    def check(m):
        return m.author == playerdict[playerlist[docnumber]].id.user

    await send_message("Please enter the number of the person you wish to save", playerdict[playerlist[docnumber]].id)

    message = await client.wait_for("message", check=check)
    
    try:
        savechoice = int(message.content)
    except:
        await send_message("The Doctor sent a non number choice this round and their save is forfit")
        return
    print("got past messages")
    

    if savechoice >= len(playerlist)-1 or savechoice < 0:
        await send_message("the Doctor entered an invalid choice and their save is forfit")
    else:
        playerdict[playerlist[savechoice]].changesafe("safe")
    await send_message("Doc turn over")

async def sherifturn(sherifnumber, playerdict, playerlist):
    await send_message("Sherif Turn start")
    await send_message(f"Sherif {playerlist[sherifnumber]} Please choose who you wish to investigate", playerdict[playerlist[sherifnumber]].id)
    for i in range (0,len(playerlist)):                                                                 #same as above except they are investigating a person to find out their role
        if i == sherifnumber:
            await send_message("You can't invetegate yourself", playerdict[playerlist[sherifnumber]].id)
        elif playerdict[playerlist[i]].invest == True and playerdict[playerlist[i]].status == "alive":  #if the sherif already investagted them it lets them know what their role was
            await send_message(f"You already Investgated {playerlist[i]} and there role is {playerdict[playerlist[i]].role}", playerdict[playerlist[sherifnumber]].id)
        elif playerdict[playerlist[i]] == "alive":
            await send_message(f"Name: {playerlist[i]} Enter {i} to investigate this person", playerdict[playerlist[sherifnumber]].id)
    
    investchoice = None
    await send_message("Please enter who you want to kill", playerdict[playerlist[i]].id)
    await asyncio.sleep(0.5)
    def check(m):
        return m.author == playerdict[playerlist[i]].id.user

    message = await client.wait_for("message", check=check)
    print("got past for message")
    try:
        investchoice = int(message.content)
    except:
        await send_message("The Sherif sent a non number choice this round and their investigation is forfit")
        return
    
    if investchoice >= len(playerlist)-1 or investchoice < 0:
        await send_message(f"The sherif entered an invalid choice and wasted their investigation")
    else:
        await send_message(f"Name: {playerlist[investchoice]} There role is {playerdict[playerlist[investchoice]].role}", playerdict[playerlist[sherifnumber]].id)
        playerdict[playerlist[investchoice]].changeinvest(True)
    await send_message("Sherif Turn over")
        
async def playervote(playerdict,playerlist):                #This function allows all of the players to vote to kick someone out
    votelist = []
    deadlist = []
    modelist = []

    for i in playerdict:                                       #If a player is dead, add them to the dead player list
        if playerdict[i].status == ("dead"):
            deadlist.append(i)

    await send_message("It's time to vote")

    for i in range(0,len(playerlist)):

        await send_message(f"<@{playerdict[playerlist[i]].id.user.id}> Who do you wish to vote?")

        for o in range (0,len(playerlist)):

            if playerlist[i] == playerlist[o]:                                                               #This allows players to vote
                await send_message("You can't vote yourself")
            elif playerdict[playerlist[o]].status == "alive":
                await send_message(f"Name: {playerlist[o]} enter {o} to vote")

        killchoice = None
        await send_message("Please enter who you want to kill", playerdict[playerlist[i]].id)
        await asyncio.sleep(0.5)

        def check(m):
            return m.author == playerdict[playerlist[i]].id.user

        message = await client.wait_for("message", check=check)
        print("got past for message")
        try:
            killchoice = int(message.content)
        except:
            await send_message(f"{playerlist[i]} entered in a non number result so their vote is forfit")
            break

        if killchoice in deadlist or (killchoice == i):
            await send_message("You entered an invalid choice and your vote is forfit")
        else:
            votelist.append(killchoice)

    if len(votelist) == 0:              
        await send_message("Everyone voted for themselves for some reason and wasted their vote")
        return
        
    modelist = statistics.multimode(votelist)                   #This creates a list and finds the most frequent number in the list
      
    if len(modelist) >= 2:                                      #If there is more than one most frequent number it calls for a tie
        await send_message("Nobody dies because there was a tie")  
        await send_message(f"These people tied in votes" )
        for i in modelist:
            await send_message(playerlist[i])
    else:
        playerdict[playerlist[modelist[0]]].changestatus("dead")

    await send_message("The votes were", votelist)
        
async def endOfTurn(playerdict,playerlist):                     #This function ends the turn for the mafia players 
    votecount = []
    await send_message("The Night has ended") 
    
    for i in playerlist:
        if playerdict[i].vote > 0:                              #If someone has a vote add them to a list 
            votecount.append(i)
    print(votecount)
    if len(votecount) == 1 and playerdict[votecount[0]].safe != "safe": #If only one person gets a vote and the doctor doesn't save them then kill them
        playerdict[votecount[0]].changestatus("dead")
    elif len(votecount) == 0:
        await send_message("The Mafia is an idiot and tried to kill someone he couldn't")
        return
    else:
        for i in votecount:
            if playerdict[i].vote >= 2:        #If the majority of mafia vote for this player then they die 
                if playerdict[i].safe != "safe":
                    playerdict[i].changestatus("dead")
                    await send_message(f"{playerdict[i]} has died. :cry:")
                else:
                    await send_message("The doctor magned to save this one...")
            else:
                tiebreaker =  random.randint(0,len(votecount)-1)         #This initiates the tiebreaker 
                await send_message("The Mafia killed", tiebreaker, ":cry:")                   #The tie breaker is finished and tells the players who died
                playerdict[votecount[tiebreaker]].changestatus("dead")  #This kills the loser of the tiebreaker
                break
    for i in playerlist:                                                #This clears the votes
        playerdict[i].changesafe("")
        playerdict[i].changevote(0, True)
        

async def newmain(mafcount, playerlist, playerid, ctxx):
    global ctx
    ctx = ctxx
    positionsnumber = []                                                               
    playerdict = {name: Player("alive", "none", id) for name, id in zip (playerlist, playerid)}    

    

    mafnumber = await mafiachooser(playerlist, playerdict, mafcount)                                  
    positionsnumber = mafnumber.copy()

    sherifnumber = await sherifchooser(positionsnumber, playerdict, playerlist)   
    positionsnumber.append(sherifnumber)

    docnumber = await doctorchooser(positionsnumber, playerdict, playerlist)                          
    positionsnumber.append(docnumber)

    for i in range (0, len(playerlist)):
        if i not in positionsnumber:                                                            
            playerdict[playerlist[i]].changerole("bystander")

    await mafiaturn(mafnumber, playerdict, playerlist)
    await doctorturn(docnumber, playerdict, playerlist)
    await sherifturn(sherifnumber, playerdict, playerlist)
    await playervote(playerdict,playerlist)
    await endOfTurn(playerdict,playerlist)

    win = True #keep True untill full testing
    while win == False:
        alive = []                                                       #Make a list for everyone who is alive
        deadmafia = []

        if playerdict[playerlist[docnumber]].status == "alive":        #This makes it so if the doctor is alive then he can use his turn
            doctorturn(docnumber, playerdict, playerlist)

        if playerdict[playerlist[sherifnumber]].status == "alive":     #Same thing above, if sherriff is alive, he can use his turn
            sherifturn(sherifnumber, playerdict, playerlist)

        mafiaturn(mafnumber, playerdict, playerlist)                    #These three run the rest of the game 
        endOfTurn(playerdict,playerlist)
        playervote(playerdict,playerlist)
        
            
        for i in playerlist:
            if playerdict[i].status == ("alive"):
                alive.append(i)
        
        for i in mafnumber:
            if playerdict[playerlist[i]].status == "alive":
                alive.remove(playerlist[i])
            else:
                deadmafia.append(i)
             
        if  len(alive) == 0:   
            print("The Mafia Won!")
            win = True
        
        if len(deadmafia) == len(mafnumber):
            print("The Players Won!")
            win = True

    
    for i in playerlist:                                                                        #just to help debug which objects have which values at the end of game (dev only)
        print(playerdict[i].display())
    count = input("done with loop")
    client.run(TOKEN)

def main():
    #players = input("Please enter mafia plus the name of the player with a space inbetween: ") #gets a list of players
    players = "Ethan Mado Vejay Mason Ben Jace Ty" #temp mesaure to make testing quicker
    #mafcount = int(input("Enter in how many maffia members you wish to have: ")) 
    mafcount = 2 #same thing as above
    templist = players.split()                                                                  #breaks up the full string of players and makes it into a list
    mafnumber = []
    positionsnumber = []
    playerlist = templist[1:]                                                                   #gets rid of the mafia invoke text
    playerdict = {name: Player("alive", "none",3) for name in (playerlist)}                         #makes each player in the list a object in a dictionary to be called later
    mafnumber = mafiachooser(playerlist, playerdict, mafcount)                                  #sets the special roles for the players that get them which the function
    print(mafnumber)
    #positionsnumber = mafnumber.copy()                                                          #A list of which index of playerlist has a roll
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
    #playervote(playerdict,playerlist)
    #endOfTurn(playerdict,playerlist)
    win = False
    while win == False:
        alive = []                                                       #Make a list for everyone who is alive
        deadmafia = []
        if playerdict[playerlist[docnumber]].status == "alive":
            doctorturn(docnumber, playerdict, playerlist)
        if playerdict[playerlist[sherifnumber]].status == "alive":
            sherifturn(sherifnumber, playerdict, playerlist)
        mafiaturn(mafnumber, playerdict, playerlist)
        endOfTurn(playerdict,playerlist)
        playervote(playerdict,playerlist)
        
            
        for i in playerlist:                                 #This makes a list for everyone who is alive 
            if playerdict[i].status == ("alive"):
                alive.append(i)
        
        for i in mafnumber:
            if playerdict[playerlist[i]].status == "alive":                          #For every mafia there is, it removes them from the alive list so that the list is only of non mafia players
                alive.remove(playerlist[i])
            else:
                deadmafia.append(i)               #If they are not alive, move them to the dead mafia list 
             
        if  len(alive) == 0:                       #If the length of alive civilian players is 0 then  the mafia win and stops the loop
            print("The Mafia Won!")
            win = True
        
        if len(deadmafia) == len(mafnumber):       #If the length of dead mafia is equal to the length of total mafia then the civilians win and stops the loop
            print("The Players Won!")
            win = True        
        
            
        
    for i in playerlist:                                                                        #just to help debug which objects have which values at the end of game (dev only)
        print(playerdict[i].display())

if __name__ == "__main__":
    main()
