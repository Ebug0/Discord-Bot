from Classes import Player
import random

if __name__ == "__main__":
    players = input("Please enter mafia plus the name of the player with a space inbetween: ")
    mafcount = int(input("Enter in how many maffia members you wish to have: "))
    mafnumbers = []
    templist = players.split()
    playerlist = templist[1:]

    print(playerlist)
    playerdict = {name: Player("alive", "none") for name in playerlist}
    print(playerdict)
    for i in (1,mafcount):
        chance = random.randint(0, len(playerlist)-1)
        while chance in mafnumbers:
            chance = random.randint(0,len(playerlist)-1)
        mafnumbers.append(i)
        playerdict[playerlist[chance]].changerole("mafia")

    print(playerdict[playerlist[0]].display())
    print(playerdict[playerlist[1]].display())
    print(playerdict[playerlist[2]].display())
    print(mafnumbers)
    print(len(playerlist)-1)