#!/usr/bin/env python
from DatabaseWrapper import DatabaseWrapper 
import CgiResponse       
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

    def getAllDocuments(self):
        auths = self._databaseWrapper.query("SELECT * FROM Authors")
        pubs = self._databaseWrapper.query("SELECT * FROM Publications")
        
        data = []
        for i in range(0,len(pubs)):
            
            auth = []
            for j in range(0, len(auths)):
                if auths[j][1] == pubs[i][0]:
                    auth.append({"First Name" : auths[j][2],
                                 "Surname" : auths[j][3], 
                                 "Initials" : auths[j][4]})

            data.append({"PublicationId" : pubs[i][0], 
                         "Title" : pubs[i][1], 
                         "Category" : pubs[i][2], 
                         "Year" : pubs[i][3], 
                         "Publisher" :pubs[i][4],
                         "Authors" : auth})

        return json.dumps(data)




        
        
        

    



