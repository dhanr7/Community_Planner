#The User_pwd_type class. Stores usernames, passwords, and type of user (teacher, admin, student body, etc.)

class User:
    username = ""
    password = ""
    classfier = ""
    #constructor
    def __init__(self, usrname, pwd, type_classifier): #type classifier denoting teacher, admin, etc.
        User.username = usrname
        User.password = pwd
        User.classifier = type_classifier

    #get methods
    @classmethod
    def getUsername(cls):
        return User.username
    
    @classmethod
    def getPassword(cls):
        return User.password

    @classmethod
    def getClassifier(cls):
        return User.classifier 
    
    #set methods
    @classmethod
    def setUsername(cls, newUsername):
        User.username = newUsername
    
    @classmethod
    def setPwd(cls, newPass):
        User.password = newPass
    
    @classmethod
    def updateClassifier(cls, newClassifier):
        User.classifier = newClassifier
    
    @classmethod
    #authentication
    def authenticateCredentials(cls, user, pW):
        if (User.username == user) and (User.password == pW):
            return True
        return False
        


    
   

