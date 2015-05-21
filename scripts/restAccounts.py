#!/usr/bin/env python

import json
import base64
import string
import os
import csv

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
    if accreditedCSV["format"]=="DHET":
        self.updateDHET(accreditedCSV)
    elif accreditedCSV["format"]=="IBSS":
        self.updateIBBS(accreditedCSV)
    elif accreditedCSV["format"]=="ISI":
        self.updateISI(accreditedCSV)
    
def updateDHET(self,accreditedCSV):
    accredited=base64.urlsafe_b64decode(accreditedCSV["data"])
    data=[]
    if not os.path.exists("../www/files/AccreditedJournals/DHET"): os.makedirs("../www/files/AccreditedJournals/DHET")
    scanfile = open("../www/files/AccreditedJournals/DHET/DHET.csv", "wb")
    scanfile.write(accredited)
    
    journals=[]
    with open('../www/files/AccreditedJournals/DHET/DHET.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            issn=None
            count=0
            for item in row:
                if count==0:
                    title=item
                elif count==1:
                    issn=item
                else:
                    journals.append({"JournalTitle":title,"ISSN":issn.replace("-","").replace(",","")})
                count=count+1

    count=0;   
    for journal in journals:
        if count!=0:
            existingJournal=[]
            existingJournal=self._databaseWrapper.query("SELECT * FROM Journals WHERE ISSN=?",[journal["ISSN"]])
            if existingJournal!=[]:
                self._databaseWrapper.query("UPDATE Journals SET Type=? WHERE ISSN=?",("Accredited",journal["ISSN"]))
                for item in existingJournal:
                    journal2=self._databaseWrapper.query("UPDATE Publications SET Accreditation = ? WHERE Id = (?)",["Accredited",item["ID"]])
            self._databaseWrapper.commit()
        count=count+1
        
    
    
def updateISI(self,accreditedCSV):
    accredited=base64.urlsafe_b64decode(accreditedCSV["data"])
    data=[]
    if not os.path.exists("../www/files/AccreditedJournals/ISI"): os.makedirs("../www/files/AccreditedJournals/ISI")
    scanfile = open("../www/files/AccreditedJournals/ISI/ISI.csv", "wb")
    scanfile.write(accredited)
    
    journals=[]
    with open('../www/files/AccreditedJournals/ISI/ISI.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            issn=None
            count=0
            for item in row:
                if count==0:
                    title=item
                elif count==1:
                    issn=item
                else:
                    journals.append({"JournalTitle":title,"ISSN":issn.replace("-","").replace(",","")})
                count=count+1

    count=0;   
    for journal in journals:
        if count!=0:
            existingJournal=[]
            existingJournal=self._databaseWrapper.query("SELECT * FROM Journals WHERE ISSN=?",[journal["ISSN"]])
            if existingJournal!=[]:
                self._databaseWrapper.query("UPDATE Journals SET Type=? WHERE ISSN=?",("Accredited",journal["ISSN"]))
                for item in existingJournal:
                    journal2=self._databaseWrapper.query("UPDATE Publications SET Accreditation = ? WHERE Id = (?)",["Accredited",item["ID"]])
            self._databaseWrapper.commit()
        count=count+1

    
def updateIBBS(self,accreditedCSV):
    accredited=base64.urlsafe_b64decode(accreditedCSV["data"])
    data=[]
    if not os.path.exists("../www/files/AccreditedJournals/IBSS"): os.makedirs("../www/files/AccreditedJournals/IBSS")
    scanfile = open("../www/files/AccreditedJournals/IBSS/IBSS.csv", "wb")
    scanfile.write(accredited)
    
    journals=[]
    with open('../www/files/AccreditedJournals/IBSS/IBSS.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            issn=None
            count=0
            for item in row:
                if count==0:
                    title=item
                elif count==1:
                    issn=item
                else:
                    journals.append({"JournalTitle":title,"ISSN":issn.replace("-","").replace(",","")})
                count=count+1

    count=0;   
    for journal in journals:
        if count!=0:
            existingJournal=[]
            existingJournal=self._databaseWrapper.query("SELECT * FROM Journals WHERE ISSN=?",[journal["ISSN"]])
            if existingJournal!=[]:
                self._databaseWrapper.query("UPDATE Journals SET Type=? WHERE ISSN=?",("Accredited",journal["ISSN"]))
                for item in existingJournal:
                    journal2=self._databaseWrapper.query("UPDATE Publications SET Accreditation = ? WHERE Id = (?)",["Accredited",item["ID"]])
            self._databaseWrapper.commit()
        count=count+1

    
def updatePredatory(self, predatoryCSV):
    predatory=base64.urlsafe_b64decode(predatoryCSV["data"])
    data=[]
    if not os.path.exists("../www/files/PredatoryJournals"): os.makedirs("../www/files/PredatoryJournals")
    scanfile = open("../www/files/PredatoryJournals/predatory.csv", "wb")
    scanfile.write(predatory)
    
    journals=[]
    with open('../www/files/PredatoryJournals/predatory.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            issn=None
            count=0
            for item in row:
                if count==0:
                    title=item
                elif count==1:
                    journals.append({"JournalTitle":title})
                count=count+1
                
    count=0;   
    for journal in journals:
        if count!=0:
            existingJournal=[]
            existingJournal=self._databaseWrapper.query("SELECT * FROM Journals WHERE Title=?",[journal["JournalTitle"]])
            if existingJournal!=[]:
                self._databaseWrapper.query("UPDATE Journals SET Type=? WHERE Title=?",("Predatory",journal["JournalTitle"]))
                for item in existingJournal:
                    journal2=self._databaseWrapper.query("UPDATE Publications SET Accreditation = ? WHERE Id = (?)",["Accredited",item["ID"]])
            self._databaseWrapper.commit()

    
def updateHIndex(self,HIndexCSV):
    HI=base64.urlsafe_b64decode(HIndexCSV["data"])
    data=[]
    if not os.path.exists("../www/files/HIndex"): os.makedirs("../www/files/HIndex")
    scanfile = open("../www/files/HIndex/HI.csv", "wb")
    scanfile.write(HI)
    
    journals=[]
    with open('../www/files/HIndex/HI.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            count=0
            issn=None
            hindex=None
            for item in row:
                if count==3:
                    issn=item[5:]
                if count==5:
                    hindex=item
                if issn!=None and hindex!=None:
                    journals.append({"ISSN":issn, "HIndex":hindex})
                count=count+1
                
    count=0;   
    for journal in journals:
        if count!=0:
            existingJournal=[]
            existingJournal=self._databaseWrapper.query("SELECT * FROM Journals WHERE ISSN=?",[journal["ISSN"]])
            if existingJournal!=[]:
                self._databaseWrapper.query("UPDATE Journals SET HIndex=? WHERE ISSN?",(journal["HIndex"],journal["ISSN"]))
            
            self._databaseWrapper.commit()

        
