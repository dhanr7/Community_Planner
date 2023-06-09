#The User_pwd_type class. Stores usernames, passwords, and type of user (teacher, admin, student body, etc.)
import json
import pandas
import os

class User:
    def __init__(cls):
        pass

    @classmethod
    def addUser(cls, username, pwd, classifier):
        to_dump = {}
        if os.path.getsize("Community_Planner/users.json") != 0:
            with open("Community_Planner/users.json", "r+") as f:
                data = json.load(f)
                to_dump.clear()
                to_dump.update({
                    "Username": username,
                    "Password": pwd,
                    "Classifier": classifier,
                })
                if (to_dump not in data):
                    data.append(to_dump)
                    f.seek(0)
                    json.dump(data, f)
                else:
                    pass
            f.close() 
        elif os.path.getsize("Community_Planner/users.json") == 0:
            with open("Community_Planner/users.json", "w") as a:
                to_dump.clear()
                to_dump.update({
                    "Username": username,
                    "Password": pwd,
                    "Classifier": classifier,
                })
                a.seek(0)
                json.dump(to_dump, a)
            a.close()

    
    @classmethod
    def deleteUser(cls, username):
        with open("Community_Planner/users.json", "r+") as f:
            data = json.load(f)
            for i, x in enumerate(data):
                if x.get("Username") == username:
                    f.pop(data[i])
            json.dump(data, f)

    @classmethod
    def checkIfUserExists(cls, username, password):
        with open("Community_Planner/users.json", "r+") as f:
            data = json.load(f)
            for x in data:
                if (x.get("Username") == username) and (x.get("Password") == password):
                    return True
            return False
    
    @classmethod
    def checkIfAdmin(cls, username):
        with open("Community_Planner/users.json", "r+") as f:
            data = json.load(f)
            for x in data:
                if (x.get("Username") == username):
                    if (((x.get("Classifier")).lower() == "administrator")):
                        return True
            return False
    
    @classmethod
    def updateUsername(cls, username, password, newUsername):
        with open("Community_Planner/users.json", "r+") as f:
            data = json.load(f)
            for x in data:
                if (x.get("Username") == username):
                    x["Username"] == newUsername
        f.close()

    @classmethod
    def getTypeAccount(cls, username):
        with open("Community_Planner/users.json", "r+") as f:
            data = json.load(f)
            for x in data:
                if (x.get("Username") == username):
                    return str(x.get("Classifier"))
        return None
    











































    # def __init__(self, usrname, pwd, type_classifier): #type classifier denoting teacher, admin, etc.
    #     User.username = usrname
    #     User.password = pwd
    #     User.classifier = type_classifier

    # #get methods
    # @classmethod
    # def getUsername(cls):
    #     return User.username
    
    # @classmethod
    # def getPassword(cls):
    #     return User.password

    # @classmethod
    # def getClassifier(cls):
    #     return User.classifier 
    
    # #set methods
    # @classmethod
    # def setUsername(cls, newUsername):
    #     User.username = newUsername
    
    # @classmethod
    # def setPwd(cls, newPass):
    #     User.password = newPass
    
    # @classmethod
    # def updateClassifier(cls, newClassifier):
    #     User.classifier = newClassifier
    
    # @classmethod
    # #authentication
    # def authenticateCredentials(cls, user, pW):
    #     if (User.username == user) and (User.password == pW):
    #         return True
    #     return False
        


    
   

