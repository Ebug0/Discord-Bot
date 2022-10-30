class Player:
    def __init__ (self, status, role):
        self.status = status
        self.role = role
        self.temp = ""

    def display(self):
        return (f"Status {self.status} Role {self.role} Temp ")

    def changerole (self, role):
        self.role = role
    
    def changestatus(self, status):
        self.status = self