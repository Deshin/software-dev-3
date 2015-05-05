#!/usr/bin/env python

from DatabaseWrapper import DatabaseWrapper      
import json
import g1

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
        return g1.getDocumentDetails(self, id)
        

    def insertDocument(self, details):
        print "Hello"


        
        
        

    



