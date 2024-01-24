class User:
    
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        
    
    def toPrintString(self):
        return "Hello, " + self.firstname + " " + self.lastname + " welcome my micro-blog"