class PDCUser:

    def __init__(self, username, email, admin, firstName, lastName, lastLogin,
    dateJoined, profilePicSize4, profilePicSize3, profilePicSize2, profilePicSize1):
        self.username = username
        self.email = email
        self.admin = (admin == "true")
        self.firstName = firstName
        self.lastName = lastName
        self.dateJoined = dateJoined
        self.lastLogin = lastLogin
        self.profilePicSize4 = profilePicSize4
        self.profilePicSize3 = profilePicSize3
        self.profilePicSize2 = profilePicSize2
        self.profilePicSize1 = profilePicSize1
