#!/usr/bin/env python

from DatabaseWrapper import DatabaseWrapper      
import json

class RestApi:
    def __init__(self, DatabaseWrapper):
        self._databaseWrapper = DatabaseWrapper
        self.databaseWrapper.connect()

    @property
    def databaseWrapper(self):
        return self._databaseWrapper

    def getScan(self, fileID):
        # TODO: generate DB Query
        data = self._databaseWrapper.query("some query here")
        return json.dumps(data)

    def getAuthors(self, pubId):
        auths = self._databaseWrapper.query("SELECT * FROM Authors WHERE PublicationID="+str(pubId))
        auth = []
        for j in range(0, len(auths)):
            auth.append({"ID":auths[j][0],
                         "PublicationID":auths[j][1],
                         "First Name" : auths[j][2],
                         "Surname" : auths[j][3], 
                         "Initials" : auths[j][4]})
        return auth

    def getAllAuthors(self):
        auths = self._databaseWrapper.query("SELECT * FROM Authors")
        auth = []
        for j in range(0, len(auths)):
            auth.append({"ID":auths[j][0],
                         "PublicationID":auths[j][1],
                         "FirstName" : auths[j][2],
                         "Surname" : auths[j][3], 
                         "Initials" : auths[j][4]})
        return auth  
        
    def getAllDocuments(self):
        pubs = self._databaseWrapper.query("SELECT * FROM Publications")


        if pubs == []:
            return "404"
        
        data = []
        for i in range(0,len(pubs)):
            auth = self.getAuthors(pubs[i][0])
            
            data.append({"PublicationId" : pubs[i][0], 
                         "Title" : pubs[i][1], 
                         "Category" : pubs[i][2], 
                         "Year" : pubs[i][3], 
                         "Publisher" :pubs[i][4],
                         "Authors" : auth})

        return json.dumps(data)

    def getDocumentDetails(self, id):
        
        try:
            details = self._databaseWrapper.query("SELECT * FROM Publications WHERE Id="+str(id))
            columnNames = [i[0] for i in self._databaseWrapper._cur.description]
            data=dict(zip(columnNames, details[0]))
            authors = self.getAuthors(id)
            authors={"Authors":authors}
            data=dict(data, **authors)
            category=data["Category"].lower()
        
        
            if category.startswith("journal"):
                journalPubDetails=self._databaseWrapper.query("SELECT * FROM JournalPublicationDetail WHERE PublicationID="+str(data["ID"]))
                columnNames = [i[0] for i in self._databaseWrapper._cur.description]
                journalPubDetails=dict(zip(columnNames, journalPubDetails[0]))
                data=dict(data,**journalPubDetails)
                
                journalDetails=self._databaseWrapper.query("SELECT * FROM Journals WHERE ID="+str(data["PublicationID"]))
                columnNames = [i[0] for i in self._databaseWrapper._cur.description]
                journalDetails=dict(zip(columnNames, journalDetails[0]))
                data=dict(data, **journalDetails)
                
            elif category.startswith("conference"):
                conferencePubDetails=self._databaseWrapper.query("SELECT * FROM ConferencePublicationDetail WHERE PublicationID="+str(data["ID"]))
                columnNames = [i[0] for i in self._databaseWrapper._cur.description]
                conferencePubDetails=dict(zip(columnNames, conferencePubDetails[0]))
                data=dict(data,**conferencePubDetails)
                
                conferenceDetails=self._databaseWrapper.query("SELECT * FROM Conferences WHERE ID="+str(data["ConferenceID"]))
                columnNames = [i[0] for i in self._databaseWrapper._cur.description]
                conferenceDetails=dict(zip(columnNames, conferenceDetails[0]))
                data=dict(data, **conferenceDetails)
                
                peerReview=self._databaseWrapper.query("SELECT * FROM ConferencePublicationPeerReviewDocumentation WHERE ConferencePublicationDetailID="+str(data["ConferenceID"]))
                columnNames = [i[0] for i in self._databaseWrapper._cur.description]
                peerReview=dict(zip(columnNames, peerReview[0]))
                data=dict(data, **peerReview)
                
            elif category.startswith("book"):
                bookPubDetails=self._databaseWrapper.query("SELECT * FROM BookPublications WHERE PublicationID="+str(data["ID"]))
                columnNames = [i[0] for i in self._databaseWrapper._cur.description]
                bookPubDetails=dict(zip(columnNames, bookPubDetails[0]))
                data=dict(data,**bookPubDetails)
                
                bookDetails=self._databaseWrapper.query("SELECT * FROM Books WHERE ID="+str(data["BooksID"]))
                columnNames = [i[0] for i in self._databaseWrapper._cur.description]
                journalDetails=dict(zip(columnNames, journalDetails[0]))
                data=dict(data, **journalDetails)
                
            data=json.dumps(data)
            return data
        except:
            return "404"

        


        
        
        

    



