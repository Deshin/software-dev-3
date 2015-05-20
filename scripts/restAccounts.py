#!/usr/bin/env python

def createAccount(self,username, password, permission, firstName, surname, initials):
    try:
        existingAccount=self._databaseWrapper.query("SELECT * FROM Users WHERE Username",[username])
        if existingAccount!=[]:
            return "409"
        else:
            self._databaseWrapper("INSERT INTO Users(Username, Permission, Password, FirstName, Surname, Initials) VALUES(?,?,?,?,?,?)",[username,permission,password,firstNAme,surname,initials])
            self._databaseWrapper.commit()
            return "Added!"
    except:
        return"400"
    
def deleteAccount(self,username):
    try:
        existingAccount=self._databaseWrapper.query("SELECT * FROM Users WHERE Username=?",[username])
        if existingAccount==[]:
            return "400"
        else:
            self._databaseWrapper.query("DELETE FROM Users WHERE Username=?",[username])
            self._database.commit()
            return "200"