#!/usr/bin/env python

import json
import sys
import os
import base64

def insertDocument(self, details):
    """ Inserts a new publication into the database based on the details entered on the submission form.
        Creates a database entry representing the new publication. New publications can only be added by Registered users (lecturers) and Administrators
        
        :param details: json object containing fields based on the category of publication being added (i.e. conference, journal, or book section)
    """
    details["Accreditation"]="Not Evaluated"   
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
        
        details["ScanPath"]="books/"+details["BookTitle"].replace(' ', '_')+"/publications/"
        details["ScanFileName"]=details["Title"].replace(' ', '_')+".pdf"
        details["TableOfContentsPath"]="books/"+details["BookTitle"].replace(' ', '_')+"/TOCs/"
        details["PeerReviewPath"]="books/"+details["BookTitle"].replace(' ', '_')+"/peerReviews/"+details["Title"].replace(' ', '_')+'/'
        result=insertBookSection(self,details)

    return result
    
        
def insertConferencePaper(self,details):
    """ Inserts a new publication with the category "Conference"
    Inserts a new conference paper into the database using the details entered on the submission form.
    Checks if the conference that the paper belongs to already exists and calls the appropriate function (insertExistingConference or insertNewConference)
    
    :param details: json object containing all details relating to a new conference paper
    """
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
    """ Inserts a new publication with the category "Conference" that belongs to an existing conference.
    Inserts a new conference paper into the database using the details entered on the submission form.
    
    :param details: json object containing all details relating to a new conference paper
    :param conferenceID: the id (primary key) of the conference to which the paper will be added
    """
    try:          
        
        self._databaseWrapper.query("INSERT INTO Publications(Title,Category,Year,Publisher,TableOfContentsPath,ScanPath,Accreditation) VALUES(?,?,?,?,?,?,?)",(details["Title"],details["Category"],details["Year"],details["Publisher"], details["TableOfContentsPath"]+'TOC.pdf', details["ScanPath"]+details["ScanFileName"], details["Accreditation"]))
        publicationID=self._databaseWrapper._cur.lastrowid
        self._databaseWrapper.query("INSERT INTO ConferencePublicationDetail(ConferenceID,PublicationID,Abstract,MotivationForAccreditation,PeerReviewProcess) VALUES(?,?,?,?,?)",(conferenceID,publicationID,details["Abstract"], details["MotivationForAccreditation"], details["PeerReviewProcess"]))
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
        return "400",sys.exc_info()[1]

def insertNewConference(self,details):
    """ Inserts a new publication with the category "Conference" where the conference the paper belongs to does not exist.
    Inserts a new conference into the database using the details entered on the submission form. Then calls insertExistingConference to add the actual conference paper since the conference now exists.
    
    :param details: json object containing all details relating to a new conference paper
    """
    try:
       self._databaseWrapper.query("INSERT INTO Conferences(ConferenceTitle, Year, Country) VALUES(?,?,?)",(details["ConferenceTitle"],details["Year"], details["Country"]))
       conferenceID=self._databaseWrapper._cur.lastrowid
       insertExistingConference(self,details,conferenceID)
       return "200"
    except:
        return "400",sys.exc_info()[1]
 
    
def insertJournalPaper(self,details):
    """ Inserts a new publication with the category "Journal"
    Inserts a new journal article into the database using the details entered on the submission form.
    Checks if the journal that the article belongs to already exists and calls the appropriate function (insertExistingJournal or insertNewJournal)
    
    :param details: json object containing all details relating to a new conference paper
    """
    existingJournal=self._databaseWrapper.query("SELECT * FROM Journals WHERE JournalTitle=?",[details["JournalTitle"]])
    if existingJournal!=[]:
        journalID=existingJournal[0][0]
        result=insertExistingJournal(self,details,journalID)
    else:
        result=insertNewJournal(self,details)
    return result

def insertExistingJournal(self,details,journalID):
    """ Inserts a new publication with the category "Journal" that belongs to an existing journal.
    Inserts a new journal article into the database using the details entered on the submission form.
    
    :param details: json object containing all details relating to a new journal article
    :param journalID: the id (primary key) of the journal to which the paper will be added
    """
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
    """ Inserts a new publication with the category "Journal" where the journal the paper belongs to does not exist.
    Inserts a new journal into the database using the details entered on the submission form. Then calls insertExistingJournal to add the actual journal article since the journal now exists.
    
    :param details: json object containing all details relating to a new journal article
    """
    try:
       self._databaseWrapper.query("INSERT INTO Journals(JournalTitle, ISSN, HIndex,Type) VALUES(?,?,?,?)",(details["JournalTitle"],details["ISSN"], details["HIndex"], details["Type"]))
       journalID=self._databaseWrapper._cur.lastrowid
       insertExistingJournal(self,details,journalID)
       return "200"
    except:
        return "400",sys.exc_info()[1]
    
def insertBookSection(self,details):
    """ Inserts a new publication with the category "Book"
    Inserts a new book section into the database using the details entered on the submission form.
    Checks if the book that the book section belongs to already exists and calls the appropriate function (insertExistingBook or insertNewBook)
    
    :param details: json object containing all details relating to a new conference paper
    """
    existingBook=self._databaseWrapper.query("SELECT * FROM Books WHERE BookTitle=?",[details["BookTitle"]])
    if existingBook!=[]:
        bookID=existingBook[0][0]
        result=insertExistingBook(self,details,bookID)
    else:
        result=insertNewBook(self,details)
    return result
    
    
def insertExistingBook(self,details,bookID):
    """ Inserts a new publication with the category "Book" that belongs to an existing book.
    Inserts a new jbook section into the database using the details entered on the submission form.
    
    :param details: json object containing all details relating to a new book section
    :param bookID: the id (primary key) of the book to which the section will be added
    """
    try:  
        #note: although this is repeated code from conference insertion, it is important
        #that it is repeated here to ensure atomicity of insertions
        self._databaseWrapper.query("INSERT INTO Publications(Title,Category,Year,Publisher,TableOfContentsPath,ScanPath,Accreditation) VALUES(?,?,?,?,?,?,?)",(details["Title"],details["Category"],details["Year"],details["Publisher"], details["TableOfContentsPath"]+'TOC.pdf', details["ScanPath"]+details["ScanFileName"], details["Accreditation"]))
        publicationID=self._databaseWrapper._cur.lastrowid
        self._databaseWrapper.query("INSERT INTO BookPublications(PublicationID,Chapter,Abstract, BooksID) VALUES(?,?,?,?)",(publicationID, details["Title"], details["Abstract"], bookID))
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
    """ Inserts a new publication with the category "Book" where the book the book section belongs to does not exist.
    Inserts a new book into the database using the details entered on the submission form. Then calls insertExistingBook to add the actual book section since the book now exists.
    
    :param details: json object containing all details relating to a new book section
    """
    try:
       self._databaseWrapper.query("INSERT INTO Books(BookTitle, ISBN,Type) VALUES(?,?,?)",(details["BookTitle"],details["ISBN"], details["Type"]))
       bookID=self._databaseWrapper._cur.lastrowid
       insertExistingBook(self,details,bookID)
       return "200"
    except:
        return "400",sys.exc_info()[1]    
    
def insertAuthors(self, details, publicationID):
    """ Inserts all the authors tied to a particular publication.
    Inserts new authors based on the details entered on the submission form.
    
    :param details: json object containing all details relating to the inserted publication.
    :param publicationID: the id of the publication to which the authors need to be linked.
    """
    try:
        for item in details["Authors"]:
            self._databaseWrapper.query("INSERT INTO Authors(PublicationID, FirstName, Surname,Initials) VALUES(?,?,?,?)",(publicationID,item["FirstName"], item["Surname"], item["Initials"]))
        return"200"
    except:
        return "400", sys.exc_info()[1]

def insertPublicationAccreditation(self, publicationID, isAccredited):
    """Changes the accreditation status of a document in the database.
    Changes the accreditation of a document that is already in the database to either "Accredited" or "Not Accredited"
    
    :param publicationID: the ID (primary key) of the publication that needs to be updated
    :param isAccredited: boolean determining if a publication should be accredited or not
    """
    query = "UPDATE Publications "\
        "SET Accreditation = ? "\
        "WHERE Id = (?)"
    if isAccredited:
        accreditation = "Accredited"
    else:
        accreditation = "Not Yet Accredited"
    try:
        self._databaseWrapper.query(query, [accreditation, publicationID])
        self._databaseWrapper.commit()
        return"200"
    except:
        return "400", sys.exc_info()[1]
    
def getCSVFormats(self):
    """ Returns all the valid formats that accreditation CSV files can be uploaded in.
    Sends the formats that csv files can be uploaded in. This can easily be added to at a later point if new formats are introduced.
    These formats are retrieved by the front end to populate a dropdown table for file upload
    """
    validFormats=["DHET","ISI", "IBSS", "Predatory", "HIndex"]
    validFormats=json.dumps(validFormats)
    return validFormats
