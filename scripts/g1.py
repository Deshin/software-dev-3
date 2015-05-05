#!/usr/bin/env python

#this actually incorporates use case g1 and g2
import json

def getDocumentDetails(self, id):
    try:
        details = self._databaseWrapper.query("SELECT * FROM Publications WHERE Id=?", (id))
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
        if data==[]:
            return "404"
        else:
            return data
    except:
        return "404"