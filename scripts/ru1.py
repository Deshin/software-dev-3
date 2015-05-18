#!/usr/bin/env python

import json
import sys
import os

def insertDocument(self, details):
    try:
        details["Accreditation"]="Not Yet Accredited"   
        details["Type"]="Unknown"   
    
        if details["Category"].lower().startswith("conference"):
            details["ScanPath"]="conferences/"+details["ConferenceTitle"]+"/publications/"+details["Title"]
            details["TableOfContentsPath"]="conferences/"+details["ConferenceTitle"]+"/TOC/TableOfContents"
            result=insertConferencePaper(self,details)
            
        elif details["Category"].lower().startswith("journal"):
            if "Volume" not in details:
                details["Volume"]=None
            if "Issue" not in details:
                details["Issue"]=None
            details["HIndex"]=None
            details["ScanPath"]="journals/"+details["JournalTitle"]+"/publications/"+details["Title"]
            details["TableOfContentsPath"]="journals/"+details["JournalTitle"]+"/TOC/TableOfContents"
            result=insertJournalPaper(self,details)
            
        elif details["Category"].lower().startswith("book"):
            result=insertBookSection(self,details)
            details["ScanPath"]="books/"+details["BookTitle"]+"/publications/"+details["Title"]
            details["TableOfContentsPath"]="books/"+details["BookTitle"]+"/TOC/TableOfContents"
    except:
        return "400"
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
        publicationID=self._databaseWrapper._cur.lastrowid
        self._databaseWrapper.query("INSERT INTO ConferencePublicationDetail(ConferenceID,PublicationID,Abstract,MotivationForAccreditation,PeerReviewProcess) VALUES(?,?,?,?,?)",(conferenceID,publicationID,details["Abstract"], details["MotivationForAccreditation"], details["PeerReview"]))
        details["PathToFile"]="peerReview/"+str(publicationID)+"/"+details["DocumentTitle"]
        self._databaseWrapper.query("INSERT INTO PeerReviewDocumentation(PublicationID,PathToFile,DocumentTitle) VALUES(?,?)",(PublicationID,details["PathToFile"]))
        insertAuthors(self,details,publicationID)
        #this commit must be at the end to make the process atomic
        self._databaseWrapper.commit()
        
        scanpath = r"..www/files/conferences/"+details["ConferenceTitle"]+"/publications"
        if not os.path.exists(scanpath): os.makedirs(scanpath)
        TOCpath = r"..www/files/conferences/"+details["ConferenceTitle"]+"/TOC"
        if not os.path.exists(TOCpath): os.makedirs(TOCpath)  
        return 200
    except:
        return "400",sys.exc_info()[1]

def insertNewConference(self,details):
    try:
       self._databaseWrapper.query("INSERT INTO Conferences(ConferenceTitle, Year, Country) VALUES(?,?,?)",(details["ConferenceTitle"],details["Year"], details["Country"]))
       conferenceID=self._databaseWrapper._cur.lastrowid
       insertExistingConference(self,details,conferenceID)
       return "200"
    except:
        return "400",sys.exc_info()[1]
 
    
def insertJournalPaper(self,details):
    existingJournal=self._databaseWrapper.query("SELECT * FROM Journals WHERE JournalTitle=?",[details["JournalTitle"]])
    if existingJournal!=[]:
        journalID=existingJournal[0][0]
        result=insertExistingJournal(self,details,journalID)
    else:
        result=insertNewJournal(self,details)
    return result

def insertExistingJournal(self,details,journalID):
    try:        
        #note: although this is repeated code from conference insertion, it is important
        #that it is repeated here to ensure atomicity of insertions
        self._databaseWrapper.query("INSERT INTO Publications(Title,Category,Year,Publisher,TableOfContentsPath,ScanPath,Accreditation) VALUES(?,?,?,?,?,?,?)",(details["Title"],details["Category"],details["Year"],details["Publisher"], details["TableOfContentsPath"], details["ScanPath"], details["Accreditation"]))
        publicationID=self._databaseWrapper._cur.lastrowid
        print details
        self._databaseWrapper.query("INSERT INTO JournalPublicationDetail(JournalID,PublicationID,Volume,Issue,Abstract) VALUES(?,?,?,?,?)",(journalID, publicationID, details["Volume"], details["Issue"], details["Abstract"]))
        details["PathToFile"]="peerReview/"+str(publicationID)+"/"+details["DocumentTitle"]
        #self._databaseWrapper.query("INSERT INTO PeerReviewDocumentation(PublicationID,PathToFile,DocumentTitle) VALUES(?,?)",(PublicationID,details["PathToFile"]))
        insertAuthors(self,details,publicationID)
        #this commit must be at the end to make the process atomic
        self._databaseWrapper.commit()
        
        scanpath = r"..www/files/journals/"+details["JournalTitle"]+"/publications"
        if not os.path.exists(scanpath): os.makedirs(scanpath)
        TOCpath = r"..www/files/journalss/"+details["JournalTitle"]+"/TOC"
        if not os.path.exists(TOCpath): os.makedirs(TOCpath)
        return "200"
    except:
        return "400", sys.exc_info()[1]

def insertNewJournal(self,details):
    try:
       self._databaseWrapper.query("INSERT INTO Journals(JournalTitle, ISSN, HIndex,Type) VALUES(?,?,?,?)",(details["JournalTitle"],details["ISSN"], details["HIndex"], details["Type"]))
       journalID=self._databaseWrapper._cur.lastrowid
       insertExistingJournal(self,details,journalID)
       return "200"
    except:
        return "400",sys.exc_info()[1]
    
def insertBookSection(self,details):
    existingBook=self._databaseWrapper.query("SELECT * FROM Books WHERE BookTitle=?",[details["BookTitle"]])
    if existingBook!=[]:
        bookID=existingBook[0][0]
        result=insertExistingBook(self,details,bookID)
    else:
        result=insertNewBook(self,details)
    return result
    
    
def insertExistingBook(self,details,bookID):
    try:        
        #note: although this is repeated code from conference insertion, it is important
        #that it is repeated here to ensure atomicity of insertions
        self._databaseWrapper.query("INSERT INTO Publications(Title,Category,Year,Publisher,TableOfContentsPath,ScanPath,Accreditation) VALUES(?,?,?,?,?,?,?)",(details["Title"],details["Category"],details["Year"],details["Publisher"], details["TableOfContentsPath"], details["ScanPath"], details["Accreditation"]))
        publicationID=self._databaseWrapper._cur.lastrowid
        self._databaseWrapper.query("INSERT INTO BookPublications(PublicationID,Chapter,Abstract, BooksID) VALUES(?,?,?,?)",(publicationID, details["Chapter"], details["Abstract"], bookID))
        insertAuthors(self,details,publicationID)
        details["PathToFile"]="peerReview/"+str(publicationID)+"/"+details["DocumentTitle"]
        self._databaseWrapper.query("INSERT INTO PeerReviewDocumentation(PublicationID,PathToFile,DocumentTitle) VALUES(?,?)",(PublicationID,details["PathToFile"]))
        #this commit must be at the end to make the process atomic
        self._databaseWrapper.commit()
        
        scanpath = r"../www/files/books/"+details["BookTitle"]+"/publications"
        if not os.path.exists(scanpath): os.makedirs(scanpath)
        TOCpath = r"..www/files/books/"+details["BookTitle"]+"/TOC"
        if not os.path.exists(TOCpath): os.makedirs(TOCpath)
        return "200"
    except:
        return "400", sys.exc_info()[1]

def insertNewBook(self,details):
    try:
       self._databaseWrapper.query("INSERT INTO Books(BookTitle, ISBN,Type) VALUES(?,?,?)",(details["BookTitle"],details["ISBN"], details["Type"]))
       bookID=self._databaseWrapper._cur.lastrowid
       insertExistingBook(self,details,bookID)
       return "200"
    except:
        return "400",sys.exc_info()[1]    
    
def insertAuthors(self, details, publicationID):
    try:
        for item in details["Authors"]:
            self._databaseWrapper.query("INSERT INTO Authors(PublicationID, FirstName, Surname,Initials) VALUES(?,?,?,?)",(publicationID,item["FirstName"], item["Surname"], item["Initials"]))
        return"200"
    except:
        return "400", sys.exc_info()[1]