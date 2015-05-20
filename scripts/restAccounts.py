#!/usr/bin/env python

def createAccount(self,username, password, permission, firstName, surname, initials):
    try:
        existingAccount=self._databaseWrapper.query("SELECT * FROM Users WHERE FirstName=? AND Surname=? AND Initials=?",[firstName, surname, initials])
        if existingAccount!=[]:
            return "409"
        else:
            self._databaseWrapper("INSERT INTO Users(Username, Permission, Password, FirstName, Surname, Initials) VALUES(?,?,?,?,?,?)",[username,permission,password,firstNAme,surname,initials])
            return "Added!"
    except:
        return"400"