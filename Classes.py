class Player:
    def __init__ (self, status, role):
        self.status = status
        self.role = role
        self.safe = ""
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