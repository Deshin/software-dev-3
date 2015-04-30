import DatabaseWrapper
import CgiResponse       
import json

class RestApi:
    def __init__(self, databaseWrapper):
        self._databaseWrapper = databaseWrapper

    @property
    def databaseWrapper(self):
        return databaseWrapper

    def getScan(self, fileID):
        # TODO: generate DB Query
        data = databaseWrapper.query("some query here")
        header = "Content-type: application/json"
        return CgiResponse(header, data)   

    def getAllDocuments(self):
        data = databaseWrapper.query("SELECT * FROM Publications")
        jsonData = json.dumps(data)
        header = "Content-type: application/json"
        return CgiResponse(header, jsonData)   




        
        
        

    



