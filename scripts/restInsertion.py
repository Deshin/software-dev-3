#!/usr/bin/env python

import json
import sys
import os
import base64

def insertDocument(self, details):
    details["Accreditation"]="Not Yet Accredited"   
    details["Type"]="Unknown"   

    if details["Category"].lower().startswith("conference"):
        details["ScanPath"]="conferences/"+details["ConferenceTitle"].replace(' ', '_')+"/publications/"
        details["ScanFileName"]=details["Title"].replace(' ', '_')+".pdf"
        details["TableOfContentsPath"]="conferences/"+details["ConferenceTitle"].replace(' ', '_')+"/TOCs/"
        details["PeerReviewPath"]="conferences/"+details["ConferenceTitle"].replace(' ', '_')+"/peerReviews/"+details["Title"].replace(' ', '_')+'/'
        result=insertConferencePaper(self,details)
        
    elif details["Category"].lower().startswith("journal"):
        if "Volume" not in details:
            details["Volume"]=None
        if "Issue" not in details:
            details["Issue"]=None
        details["HIndex"]=None
        details["ScanPath"]="journals/"+details["JournalTitle"].replace(' ', '_')+"/publications/"
        details["ScanFileName"]=details["Title"].replace(' ', '_')+".pdf"
        details["TableOfContentsPath"]="journals/"+details["JournalTitle"].replace(' ', '_')+"/TOCs/"
        details["PeerReviewPath"]="journals/"+details["JournalTitle"].replace(' ', '_')+"/peerReviews/"+details["Title"].replace(' ', '_')+'/'
        result=insertJournalPaper(self,details)
        
    elif details["Category"].lower().startswith("book"):
        result=insertBookSection(self,details)
        details["ScanPath"]="books/"+details["BookTitle"].replace(' ', '_')+"/publications/"
        details["ScanFileName"]=details["Title"].replace(' ', '_')+".pdf"
        details["TableOfContentsPath"]="books/"+details["BookTitle"].replace(' ', '_')+"/TOCs/"
        details["PeerReviewPath"]="books/"+details["BookTitle"].replace(' ', '_')+"/peerReviews/"+details["Title"].replace(' ', '_')+'/'

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
        
        self._databaseWrapper.query("INSERT INTO Publications(Title,Category,Year,Publisher,TableOfContentsPath,ScanPath,Accreditation) VALUES(?,?,?,?,?,?,?)",(details["Title"],details["Category"],details["Year"],details["Publisher"], details["TableOfContentsPath"]+'TOC.pdf', details["ScanPath"]+details["ScanFileName"], details["Accreditation"]))
        publicationID=self._databaseWrapper._cur.lastrowid
        self._databaseWrapper.query("INSERT INTO ConferencePublicationDetail(ConferenceID,PublicationID,Abstract,MotivationForAccreditation,PeerReviewProcess) VALUES(?,?,?,?,?)",(conferenceID,publicationID,details["Abstract"], details["MotivationForAccreditation"], details["PeerReview"]))
        if not os.path.exists("../www/files/"+details['PeerReviewPath']): os.makedirs("../www/files/"+details['PeerReviewPath'])
        print details;
        for suppDoc in details["SupportingDocumentation"]:
            PathToFile=details["PeerReviewPath"]+suppDoc['file']['name'].replace(' ', '_')
            self._databaseWrapper.query("INSERT INTO PeerReviewDocumentation(PublicationID,PathToFile, DocumentTitle) VALUES(?,?,?)",(publicationID,PathToFile,suppDoc['file']['name'].replace(' ', '_')))
            peerreviewdocfile=open("../www/files/"+PathToFile, "wb+")
            peerreviewdocfile.write(base64.b64decode(suppDoc["data"]))
        insertAuthors(self,details,publicationID)
        if not os.path.exists("../www/files/"+details['ScanPath']): os.makedirs("../www/files/"+details['ScanPath'])
        scanfile = open("../www/files/"+details['ScanPath']+details["ScanFileName"], "wb+")
        scanfile.write(base64.b64decode(details["PublicationFile"]["data"]))
        if not os.path.exists("../www/files/"+details["TableOfContentsPath"]): os.makedirs("../www/files/"+details["TableOfContentsPath"])
        tocfile =  open("../www/files/"+details['TableOfContentsPath']+"TOC.pdf", "wb+")
        tocfile.write(base64.b64decode(details["PublicationToc"]["data"]))
        #this commit must be at the end to make the process atomic
        self._databaseWrapper.commit()
        return "200"
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
        journal=self._databaseWrapper.query("SELECT * FROM Journals WHERE ID=?",[journalID])
        status=journal[0][4]
        #note: although this is repeated code from conference insertion, it is important
        #that it is repeated here to ensure atomicity of insertions
        self._databaseWrapper.query("INSERT INTO Publications(Title,Category,Year,Publisher,TableOfContentsPath,ScanPath,Accreditation) VALUES(?,?,?,?,?,?,?)",(details["Title"],details["Category"],details["Year"],details["Publisher"], details["TableOfContentsPath"]+'TOC.pdf', details["ScanPath"]+details["ScanFileName"], str(status)))
        publicationID=self._databaseWrapper._cur.lastrowid
        self._databaseWrapper.query("INSERT INTO JournalPublicationDetail(JournalID,PublicationID,Volume,Issue,Abstract) VALUES(?,?,?,?,?)",(journalID, publicationID, details["Volume"], details["Issue"], details["Abstract"]))
        if not os.path.exists("../www/files/"+details['PeerReviewPath']): os.makedirs("../www/files/"+details['PeerReviewPath'])
        for suppDoc in details["SupportingDocumentation"]:
            PathToFile=details["PeerReviewPath"]+suppDoc['file']['name'].replace(' ', '_')
            self._databaseWrapper.query("INSERT INTO PeerReviewDocumentation(PublicationID,PathToFile, DocumentTitle) VALUES(?,?,?)",(publicationID,PathToFile,suppDoc['file']['name'].replace(' ', '_')))
            peerreviewdocfile=open("../www/files/"+PathToFile, "wb+")
            peerreviewdocfile.write(base64.b64decode(suppDoc["data"]))
        insertAuthors(self,details,publicationID)
        
        if not os.path.exists("../www/files/"+details['ScanPath']): os.makedirs("../www/files/"+details['ScanPath'])
        scanfile = open("../www/files/"+details['ScanPath']+details["ScanFileName"], "wb+")
        scanfile.write(base64.b64decode(details["PublicationFile"]["data"]))
        if not os.path.exists("../www/files/"+details["TableOfContentsPath"]): os.makedirs("../www/files/"+details["TableOfContentsPath"])
        tocfile =  open("../www/files/"+details['TableOfContentsPath']+"TOC.pdf", "wb+")
        tocfile.write(base64.b64decode(details["PublicationToc"]["data"]))
        #this commit must be at the end to make the process atomic
        self._databaseWrapper.commit()
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
        
        self._databaseWrapper.query("INSERT INTO Publications(Title,Category,Year,Publisher,TableOfContentsPath,ScanPath,Accreditation) VALUES(?,?,?,?,?,?,?)",(details["Title"],details["Category"],details["Year"],details["Publisher"], details["TableOfContentsPath"]+'TOC.pdf', details["ScanPath"]+details["ScanFileName"], details["Accreditation"]))
        publicationID=self._databaseWrapper._cur.lastrowid
        self._databaseWrapper.query("INSERT INTO BookPublications(PublicationID,Chapter,Abstract, BooksID) VALUES(?,?,?,?)",(publicationID, details["Chapter"], details["Abstract"], bookID))
        insertAuthors(self,details,publicationID)
        if not os.path.exists("../www/files/"+details['PeerReviewPath']): os.makedirs("../www/files/"+details['PeerReviewPath'])
        for suppDoc in details["SupportingDocumentation"]:
            PathToFile=details["PeerReviewPath"]+suppDoc['file']['name'].replace(' ', '_')
            self._databaseWrapper.query("INSERT INTO PeerReviewDocumentation(PublicationID,PathToFile, DocumentTitle) VALUES(?,?,?)",(publicationID,PathToFile,suppDoc['file']['name'].replace(' ', '_')))
            peerreviewdocfile=open("../www/files/"+PathToFile, "wb+")
            peerreviewdocfile.write(base64.b64decode(suppDoc["data"]))
        if not os.path.exists("../www/files/"+details['ScanPath']): os.makedirs("../www/files/"+details['ScanPath'])
        scanfile = open("../www/files/"+details['ScanPath']+details["ScanFileName"], "wb+")
        scanfile.write(base64.b64decode(details["PublicationFile"]["data"]))
        if not os.path.exists("../www/files/"+details["TableOfContentsPath"]): os.makedirs("../www/files/"+details["TableOfContentsPath"])
        tocfile =  open("../www/files/"+details['TableOfContentsPath']+"TOC.pdf", "wb+")
        tocfile.write(base64.b64decode(details["PublicationToc"]["data"]))
        #this commit must be at the end to make the process atomic
        self._databaseWrapper.commit()
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

def insertPublicationAccreditation(self, publicationID, isAcreddited):
    query = "UPDATE Publications "\
        "SET Accreditation = ? "\
        "WHERE ID = ?"
    if isAccredited:
        accreditation = "Accredited"
    else:
        accreditation = "Not Accredited"
    self._databaseWrapper.query(query, [accreditation, publicationID])
