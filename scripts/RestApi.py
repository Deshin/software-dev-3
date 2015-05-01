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
        data = self._databaseWrapper.query("SELECT * FROM Publications")
        return json.dumps(data)




        
        
        

    



