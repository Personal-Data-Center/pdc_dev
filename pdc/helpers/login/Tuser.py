class Tuser:

    def __init__(self, name, email, isAdmin):
        self.name = name
        self.email = email
        self.isAdmin = isAdmin

    def getName(self):
        return self.name

    def getEmail(self):
        return self.email

    def isAdmin(self):
        return self.isAdmin
