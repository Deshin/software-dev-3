#!/usr/bin/env python

import json

def createAccount(self,username, password, permission, firstName, surname, initials):
    """ Creates an account with the given parameters.
    Creates a database entry representing the user-account. User accounts can only be created by administrators.
    
    :param username: String to be used as a user-name.
    :param password: String hash of the user password to be saved in the Database.
    :param permission: String representing the permission level of the account to be created.
    :param firstName: String representing the first name of the person the account is associated with.
    :param surname: String representing the surname of the person the account is associated with.
    :param initials: A string with the Initials - the first letters of each name of the person the acocunt is associated with. 
    """
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
    """ Deletes a user-account, identified by the username
    
    Removes a user-account from the database, identified by the username, which can uniquely identify a user.
    
    :param username: A string holding the user-name of the account to be deleted. """
    try:
        existingAccount=self._databaseWrapper.query("SELECT * FROM Users WHERE Username=?",[username])
        if existingAccount==[]:
            return "404"
        else:
            if existingAccount[0][2]=="admin":
                return "403"
            else:
                self._databaseWrapper.query("DELETE FROM Users WHERE Username=?",[username])
                self._databaseWrapper.commit()
                return "Account Deleted"
    except:
        return "400"
    
def getAllAccountDocs(self,username):
    """ Returns all the information associated with a user-account.
    
    :param username: A string used to uniquely identify the user-account of which information is returned.
    :returns: A json object holding the user-name, first-name, surname, initials and permissions associated with the account.
    :rtype: A json string """
    try:
        existingAccount=self._databaseWrapper.query("SELECT * FROM Users WHERE Username=?",[username])
        if existingAccount==[]:
            return "400"
        else:
            result={"username":existingAccount[0][1], "firstname":existingAccount[0][4], "surname":existingAccount[0][5], "initials":existingAccount[0][6], "permission":existingAccount[0][2]}
            result=json.dumps(result)
            return result
    except:
        return"404"
    
def updateAccredited(self, accreditedCSV):
    print "Accredited"
    
def updateDHET(self,accreditedCSV):
    print "DHET"
    
def updateISI(self,accreditedCSV):
    print "ISI"
    
def updateIBBS(self,accreditedCSV):
    print "IBBS"
    
def updatePredatory(self, predatoryCSV):
    print "Predatory"
    
def updateHIndex(self,HIndexCSV):
    print "HIndex"

        
