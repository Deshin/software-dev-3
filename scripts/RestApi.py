#!/usr/bin/env python

from DatabaseWrapper import DatabaseWrapper      
import json
import restRetrieval
import restSearch
import restInsertion
import restAccounts

class RestApi:
    def __init__(self, DatabaseWrapper):
        self._databaseWrapper = DatabaseWrapper
        self.databaseWrapper.connect()

    @property
    def databaseWrapper(self):
        return self._databaseWrapper
    
    def createAccount(self,username, password, permission, firstName, surname, initials):
        return restAccounts.createAccount(self,username, password, permission, firstName, surname, initials)
    
    def deleteAccount(self,username):
        return restAccounts.deleteAccount(self,username)
    
    def lockAccount(self,username):
        return restAccounts.lockAccount(self,username)

    def getAuthors(self, pubId):
        return restRetrieval.getAuthors(self, pubId)

    def getAllAuthors(self):
        return restRetrieval.getAllAuthors(self)
        
    def getAllDocuments(self, skip, length, sortBy, sort):
        return restRetrieval.getAllDocuments(self, skip, length, sortBy, sort)

    def getDocumentDetails(self, id):
        return restRetrieval.getDocumentDetails(self, id)
    
    def getExtraDocuments(self, pubId):  
        return restRetrieval.getExtraDocuments(self, pubId) 
    
    def getLoginCredentials(self,username):
        return restRetrieval.getLoginCredentials(self,username)
        
    def insertDocument(self, details):
        return restInsertion.insertDocument(self, details)

    def simpleSearch(self, searchTerms, skip, length, sortBy, sort):
        return restSearch.simpleSearch(self, searchTerms, skip, length, sortBy, sort)
   
    def sortDocuments(self,sortBy, sort):
        return restSearch.sortDocuments(self, sortBy, sort)

    def getAdvancedSearchFields(self):
        return restSearch.getAdvancedSearchFields()

    def advancedSearch(self, searchTerms, skip, length, sortBy, sort):
        return restSearch.advancedSearch(self, searchTerms, skip, length, sortBy, sort) 
    


        
        
        

    



