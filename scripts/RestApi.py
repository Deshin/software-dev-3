#!/usr/bin/env python

from DatabaseWrapper import DatabaseWrapper      
import json
import restRetrieval
import restSearch
import ru1

class RestApi:
    def __init__(self, DatabaseWrapper):
        self._databaseWrapper = DatabaseWrapper
        self.databaseWrapper.connect()

    @property
    def databaseWrapper(self):
        return self._databaseWrapper

    def getAuthors(self, pubId):
        return restRetrieval.getAuthors(self, pubId)

    def getAllAuthors(self):
        return restRetrieval.getAllAuthors(self)
        
    def getAllDocuments(self):
        return restRetrieval.getAllDocuments(self)

    def getDocumentDetails(self, id):
        return restRetrieval.getDocumentDetails(self, id)
        
    def insertDocument(self, details):
        return ru1.insertDocument(self, details)

    def simpleSearch(self, searchTerms):
        return restSearch.simpleSearch(self, searchTerms)


        
        
        

    



