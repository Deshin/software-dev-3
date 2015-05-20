#!/usr/bin/env python

import json

def createAccount(self,username, password, permission, firstName, surname, initials):
    try:
        existingAccount=self._databaseWrapper.query("SELECT * FROM Users WHERE Username=?",[username])
        if existingAccount!=[]:
            return "409"
        else:
            self._databaseWrapper.query("INSERT INTO Users(Username, Permission, Password, FirstName, Surname, Initials) VALUES(?,?,?,?,?,?)",[username,permission,password,firstName,surname,initials])
            self._databaseWrapper.commit()
            return "Added!"
    except:
        return"400"
    
def deleteAccount(self,username):
    try:
        existingAccount=self._databaseWrapper.query("SELECT * FROM Users WHERE Username=?",[username])
        if existingAccount==[]:
            return "404"
        else:
            self._databaseWrapper.query("DELETE FROM Users WHERE Username=?",[username])
            self._databaseWrapper.commit()
            return "Account Deleted"
    except:
        return "400"
    
def getAllAccountDocs(self,username):
    try:
        existingAccount=self._databaseWrapper.query("SELECT * FROM Users WHERE Username=?",[username])
        if existingAccount==[]:
            return "400"
        else:
            result={"username":existingAccount[0][1], "firstname":existingAccount[0][4], "surname":existingAccount[0][5], "initials":existingAccount[0][6]}
            result=json.dumps(result)
            return result
    except:
        return"404"

        