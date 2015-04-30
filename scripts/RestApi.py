import DatabaseWrapper
import CgiResponse

class RestApi:
    def __init__(self, databaseWrapper):
        self._databaseWrapper = databaseWrapper

    @property
    def databaseWrapper(self):
        return databaseWrapper

    def request(self, route, params, method):
        if method == "GET":
            return get(route, params)
        elif method == "POST":
            return post(route, params)
        elif method == "PUT":
            return put(route, params)
        elif method == "DELETE":
            return delete(route, params)
        else
            print("??")
            # Request is screwed
        
    def get(route, params):
        if route == "scan":
            fileID = params[scanID]    
            return getScan(fileID)

    def post(self, route):

    def put(self, route):

    def delete(self, route):
        
    def getScan(self, fileID):
        # TODO: do DB query
        data = databaseWrapper.query("some query here")
        header = "Content-type: application/json"
        return CgiResponse(header, data)   A

    def getDocuments(self):
        # TODO: do DB query
        data = databaseWrapper.query("some query here")
        header = "Content-type: application/json"
        return CgiResponse(header, data)   A




        
        
        

    



