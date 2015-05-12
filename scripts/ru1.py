#!/usr/bin/env python

import json
import sys

def insertDocument(self, details):
    if details["Category"].lower().startswith("conference"):
        try:
            print details["PathToFile"]
        except:
            details["PathToFile"]=None
        try:
            print details["DocumentTitle"]
        except:
            details["DocumentTitle"]=None
        result=insertConferencePaper(self,details)
        
    elif details["Category"].lower().startswith("journal"):
        result=insertJournalPaper(self,details)
        
    elif details["Category"].lower().startswith("book"):
        result=insertBookSection(self,details)
    return result
    
        
def insertConferencePaper(self,details):
    existingConference=self._databaseWrapper.query("SELECT * FROM Conferences WHERE ConferenceTitle=?",[details["ConferenceTitle"]])
    if existingConference!=[]:
        for item in existingConference:
            if item[2]==details["Year"]:
                conferenceID=item[0]
                result=insertExistingConference(self,details,conferenceID)
            else:
                result=insertNewConference(self,details)
    else:
        result=insertNewConference(self,details)
    return result
        
def insertExistingConference(self,details, conferenceID):
    try:     
        self._databaseWrapper.query("INSERT INTO Publications(Title,Category,Year,Publisher,TableOfContentsPath,ScanPath,Accreditation) VALUES(?,?,?,?,?,?,?)",(details["Title"],details["Category"],details["Year"],details["Publisher"], details["TableOfContentsPath"], details["ScanPath"], details["Accreditation"]))
        publicationID=self.databaseWrapper._cur.lastrowid
        self._databaseWrapper.query("INSERT INTO ConferencePublicationDetail(ConferenceID,PublicationID,Abstract,MotivationForAccreditation,PeerReviewProcess) VALUES(?,?,?,?,?)",(conferenceID,publicationID,details["Abstract"], details["MotivationForAccreditation"], details["PeerReview"]))
        conferencePublicationDetailID=self.databaseWrapper._cur.lastrowid
        if(details["PathToFile"]!=None and details["DocumentTitle"]!=None):
            self._databaseWrapper.query("INSERT INTO ConferencePublicationPeerReviewDocumentation(ConferencePublicationDetailID,PathToFile,DocumentTitle) VALUES(?,?,?)",(conferencePublicationDetailID,details["PathToFile"],details["DocumentTitle"]))
        #this commit must be at the end to make the process atomic
        self._databaseWrapper.commit()
    except:
        print sys.exc_info()[1]
        return "404"

def insertNewConference(self,details):
    try:
       self._databaseWrapper.query("INSERT INTO Conferences(ConferenceTitle, Year, Country) VALUES(?,?,?)",(details["ConferenceTitle"],details["Year"], details["Country"]))
       conferenceID=self.databaseWrapper._cur.lastrowid
       insertExistingConference(self,details,conferenceID)
    except:
        print sys.exc_info()[1]
        return "404"
 
    
def insertJournalPaper(self,details):
    print details
    
def insertBookSection(self,details):
    print details
    
    