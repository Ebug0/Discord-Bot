from discord.commands import *
from discord.ui import *
import discord



class Player:
    def __init__ (self, status, role, id):
        self.status = status
        self.role = role
        self.safe = ""
        self.id = id
        self.vote = 0
        self.invest = False

    def display(self):
        return (f"Status {self.status} Role {self.role} Temp {self.safe} Vote {self.vote} Investigated {self.invest}")

    def changerole (self, role):
        self.role = role
    
    def changestatus(self, status):
        self.status = status
    
    def changesafe(self,safe):
        self.safe = safe
    
    def changevote(self, vote, clear):
        if clear == True:
            self.vote = 0
        self.vote += vote
    def changeinvest(self, invest):
        self.invest = invest

class MyView(View):

    def __init__(self, ctx):
        super().__init__()
        self.mafchoosen = False
        self.ctx = ctx
        self.value = None
        self.players_name = []
        self.player_id = []
        self.mafnumber = 0

    @discord.ui.button(label = "Join", style = discord.ButtonStyle.green)
    async def button_callback (self, button, interaction):
        self.players_name.append(interaction.user.name)
        self.player_id.append(interaction.user.id)
        await interaction.response.send_message(f"{interaction.user} has joined the game!\nThese are the people currently in the game {self.players_name}")

    @discord.ui.button(label = "Click to Start", style = discord.ButtonStyle.red, custom_id = "start")
    async def danger_button_callback (self, button, interaction):

        if self.mafchoosen == True:
            await interaction.response.edit_message (content = f"the Game has started with {self.players_name}", view = None)
        else:
            await interaction.response.send_message (content = "Please pick the number of mafia")
        
        self.value = "started"
        self.stop()
            
    
    @discord.ui.button(label = "Click for 1 mafia", style = discord.ButtonStyle.grey, custom_id = "maf1")
    async def maf1_button_callback (self, button, interaction):

        button2 = [x for x in self.children if x.custom_id == "maf2"][0]
        button3 = [x for x in self.children if x.custom_id == "maf3"][0]
        
        button.label = "Mafia Selected"
        button2.label = "Mafia Selected"
        button3.label = "Mafia Selected"
        button.disabled = True
        button2.disabled = True
        button3.disabled = True
        self.mafchoosen = True
        self.mafnumber = 1

        await self.ctx.send("1 Mafia selected")
        await interaction.response.edit_message(view = self)
            
    
    @discord.ui.button(label = "Click for 2 mafia", style = discord.ButtonStyle.grey, custom_id = "maf2")
    async def maf2_button_callback (self, button, interaction):

        button2 = [x for x in self.children if x.custom_id == "maf1"][0]
        button3 = [x for x in self.children if x.custom_id == "maf3"][0]
        button.label = "Mafia Selected"
        button2.label = "Mafia Selected"
        button3.label = "Mafia Selected"
        button.disabled = True
        button2.disabled = True
        button3.disabled = True
        self.mafchoosen = True
        self.mafnumber = 2
        
        await self.ctx.send("2 Mafia selected")
        await interaction.response.edit_message(view = self)
    
    @discord.ui.button(label = "Click for 3 mafia", style = discord.ButtonStyle.grey, custom_id = "maf3")
    async def maf3_button_callback (self, button, interaction):

        button2 = [x for x in self.children if x.custom_id == "maf2"][0]
        button3 = [x for x in self.children if x.custom_id == "maf1"][0]
        button.label = "Mafia Selected"
        button2.label = "Mafia Selected"
        button3.label = "Mafia Selected"
        button.disabled = True
        button2.disabled = True
        button3.disabled = True
        self.mafchoosen = True
        self.mafnumber = 3

        await self.ctx.send("3 Mafia selected")
        await interaction.response.edit_message(view = self)
    

    
    
