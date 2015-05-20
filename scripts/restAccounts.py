#!/usr/bin/env python

def createAccount(self,username, password, permission, firstName, surname, initials):
    existingAccount=self._databaseWrapper.query("SELECT * FROM Users WHERE FirstName=? AND Surname=? AND Initials=?",[firstName, surname, initials])
    if existingAccount!=[]:
        return "Account already exists!"
    else:
        print "Hi"
        