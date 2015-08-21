#!/usr/bin/env python

#this actually incorporates use case g1 and g2
import json


def getAuthors(self, pubId):
    """ Function to find all the authors associated with a publication ID

    :param pubId: Integer publication ID number which uniquely identifies a publication in the database.

    :return: An array of dictionaries containing all the information regarding a certain author.
    :rtype: An array of Dict objects"""
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
    """ Returns information on all the authors in the database.

    :return: An array of dictionaries containing author details for all authors
    :rtype: An array of Dict objects """
    auths = self._databaseWrapper.query("SELECT * FROM Authors")
    auth = []
    for j in range(0, len(auths)):
        auth.append({"ID":auths[j][0],
                     "PublicationID":auths[j][1],
                     "FirstName" : auths[j][2],
                     "Surname" : auths[j][3],
                     "Initials" : auths[j][4]})
    return auth

def getExtraDocuments(self, pubId):
    """ Find information on all the extra documents associated with a publication.

    :param pubId: An integer which uniquely identifies a publication in the database
    :return: An array of dictionaries containing document information for all the documents associated with a publication.
    :rtype: An array of Dict objects. """
    peerReview=self._databaseWrapper.query("SELECT * FROM PeerReviewDocumentation WHERE PublicationID=(?)",[str(pubId)])
    docs=[]
    for j in range(0,len(peerReview)):
        docs.append({"ID":peerReview[j][0],
                     "PublicationID":peerReview[j][1],
                     "PathToFile":peerReview[j][2],
                     "DocumentTitle":peerReview[j][3]})
    return docs

def getAllDocuments(self, skip, length, sortBy, sort):
    """ Finds information on all the documents listend in the database.

    :param skip: Integer, represents the first entry to return -1. Used for pagination.
    :param length: Integer, defines how many entries to return. Used for pagination.
    :param sortBy: A string representing a field name to sort the results by.
    :param sort: A string, "ASC" or "DESC" which signifies "ascending or descending". This determines in which order to sorth the returned document details.

    :return: A json array containing json objects that hold document details. The array contains `length` number of elements.
    :rtype: A stringified json array of objects"""

    pubs = self._databaseWrapper.query("SELECT * FROM Publications "+self.sortDocuments(sortBy, sort) + " LIMIT ? OFFSET ?", (length, skip))

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
    """ Finds the details for the specified document

    :param id: The Publication ID integer that uniquely identifies a publication in the database.

    :return: A stringified json object containing the details for the specified publication.
    :rtype: A String, representing a json object"""
    try:
        details = self._databaseWrapper.query("SELECT * FROM Publications WHERE Id=(?)", [id])
        columnNames = [i[0] for i in self._databaseWrapper._cur.description]
        data=dict(zip(columnNames, details[0]))
        authors = self.getAuthors(id)
        authors={"Authors":authors}
        data=dict(data, **authors)
        docs = self.getExtraDocuments(id)
        docs={"PeerReviewDocumentation":docs}
        data=dict(data, **docs)
        category=data["Category"].lower()


        if category.startswith("journal"):
            journalPubDetails=self._databaseWrapper.query("SELECT * FROM JournalPublicationDetail WHERE PublicationID=(?)",[str(data["ID"])])
            columnNames = [i[0] for i in self._databaseWrapper._cur.description]
            journalPubDetails=dict(zip(columnNames, journalPubDetails[0]))
            data=dict(data,**journalPubDetails)

            journalDetails=self._databaseWrapper.query("SELECT * FROM Journals WHERE ID=(?)",[str(data["JournalID"])])

            print journalDetails
            columnNames = [i[0] for i in self._databaseWrapper._cur.description]
            journalDetails=dict(zip(columnNames, journalDetails[0]))
            data=dict(data, **journalDetails)

            #peerReview=self._databaseWrapper.query("SELECT * FROM PeerReviewDocumentation WHERE PublicationID=(?)",[str(id)])
            #columnNames = [i[0] for i in self._databaseWrapper._cur.description]
            #peerReview=dict(zip(columnNames, peerReview[0]))
            #data=dict(data, **peerReview)

        elif category.startswith("conference"):
            conferencePubDetails=self._databaseWrapper.query("SELECT * FROM ConferencePublicationDetail WHERE PublicationID=(?)",[str(data["ID"])])
            columnNames = [i[0] for i in self._databaseWrapper._cur.description]
            conferencePubDetails=dict(zip(columnNames, conferencePubDetails[0]))
            data=dict(data,**conferencePubDetails)

            conferenceDetails=self._databaseWrapper.query("SELECT * FROM Conferences WHERE ID=(?)",[str(data["ConferenceID"])])
            columnNames = [i[0] for i in self._databaseWrapper._cur.description]
            conferenceDetails=dict(zip(columnNames, conferenceDetails[0]))
            data=dict(data, **conferenceDetails)

            #peerReview=self._databaseWrapper.query("SELECT * FROM PeerReviewDocumentation WHERE PublicationID=(?)",[str(id)])
            #columnNames = [i[0] for i in self._databaseWrapper._cur.description]
            #peerReview=dict(zip(columnNames, peerReview[0]))
            #data=dict(data, **peerReview)

        elif category.startswith("book"):
            bookPubDetails=self._databaseWrapper.query("SELECT * FROM BookPublications WHERE PublicationID=(?)",[str(data["ID"])])
            columnNames = [i[0] for i in self._databaseWrapper._cur.description]
            bookPubDetails=dict(zip(columnNames, bookPubDetails[0]))
            data=dict(data,**bookPubDetails)

            bookDetails=self._databaseWrapper.query("SELECT * FROM Books WHERE ID=(?)",[str(data["BooksID"])])
            columnNames = [i[0] for i in self._databaseWrapper._cur.description]
            bookDetails=dict(zip(columnNames, bookDetails[0]))
            data=dict(data, **bookDetails)

            #peerReview=self._databaseWrapper.query("SELECT * FROM PeerReviewDocumentation WHERE PublicationID=(?)",[str(id)])
            #columnNames = [i[0] for i in self._databaseWrapper._cur.description]
            #peerReview=dict(zip(columnNames, peerReview[0]))
            #data=dict(data, **peerReview)
            
        data=json.dumps(data)
        if data==[]:
            return "404"
        else:
            return data
    except:
        return "404"

def getLoginCredentials(self,username):
    """ Finds the login credentials for a certain user

    :param username: A string that uniquely identifies a certain user account in the database.
    :return: A dictionary containing the permission level and hashed password of the specified user account.
    :rtype: A Dict object."""
    try:
        loginDetails=self._databaseWrapper.query("SELECT * FROM Users WHERE Username=(?)",[username])
        data={"Password":loginDetails[0][3].encode("unicode-escape"),
            "Permission":loginDetails[0][2].encode("unicode-escape")}
        return data
    except:
        return "401"
