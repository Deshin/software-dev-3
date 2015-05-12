#!/usr/bin/env python

from DatabaseWrapper import DatabaseWrapper      
import json
import retrieval
import restSearch

class RestApi:
    def __init__(self, DatabaseWrapper):
        self._databaseWrapper = DatabaseWrapper
        self.databaseWrapper.connect()

    @property
    def databaseWrapper(self):
        return self._databaseWrapper

    def getAuthors(self, pubId):
        return retrieval.getAuthors(self, pubId)

    def getAllAuthors(self):
        return retrieval.getAllAuthors(self)
        
    def getAllDocuments(self):
        return retrieval.getAllDocuments(self)

    def getDocumentDetails(self, id):
        return retrieval.getDocumentDetails(self, id)
        
    def insertDocument(self, details):
        return ru1.insertDocument(self, details)

    def simpleSearch(self, searchTerms):
        return restSearch.simpleSearch(self, searchTerms)


        
        
        

    



