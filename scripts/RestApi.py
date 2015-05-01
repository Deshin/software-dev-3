from DatabaseWrapper import DatabaseWrapper 
import CgiResponse       
import json

class RestApi:
    def __init__(self, DatabaseWrapper):
        self._databaseWrapper = DatabaseWrapper

    @property
    def databaseWrapper(self):
        return self._databaseWrapper

    def getScan(self, fileID):
        # TODO: generate DB Query
        data = self._databaseWrapper.query("some query here")
        header = "Content-type: application/json"
        return CgiResponse(header, data)   

    def getAllDocuments(self):
        data = self._databaseWrapper.query("SELECT * FROM Publications")
        jsonData = json.dumps(data)
        header = "Content-type: application/json"
        return CgiResponse(header, jsonData)   




        
        
        

    



