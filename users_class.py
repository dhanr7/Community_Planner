#The User_pwd_type class. Stores usernames, passwords, and type of user (teacher, admin, student body, etc.)

class User_pwd_type:
    #constructor
    def __init__(self, usrname, pwd, type_classifier): #type classifier denoting teacher, admin, etc.
        self.username = usrname
        self.password = pwd
        self.classifier = type_classifier

    #get methods
    @classmethod
    def getUsername(cls):
        return User_pwd_type.username
    
    @classmethod
    def getPassword(cls):
        return User_pwd_type.password

    @classmethod
    def getClassifier(cls):
        return User_pwd_type.classifier 
    
    #set methods
    @classmethod
    def setUsername(cls, newUsername):
        User_pwd_type.username = newUsername
    
    @classmethod
    def setPwd(cls, newPass):
        User_pwd_type.password = newPass
    
    @classmethod
    def updateClassifier(cls, newClassifier):
        User_pwd_type.classifier = newClassifier
    
    @classmethod
    #authentication
    def authenticateCredentials(cls, user, pW):
        if (User_pwd_type.username == user) and (User_pwd_type.password == pW):
            return True
        return False
        


    
   

