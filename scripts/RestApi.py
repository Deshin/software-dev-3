#!/usr/bin/env python

from DatabaseWrapper import DatabaseWrapper      
import json
import restRetrieval
import restSearch
import restInsertion
import restAccounts

class RestApi:
    """ RestApi is the central class used for the REST API, all REST enpoints pass through this class. The functions used in those endpoints are documented in their respective files. """
    
    def __init__(self, DatabaseWrapper):
        self._databaseWrapper = DatabaseWrapper
        self.databaseWrapper.connect()

    @property
    def databaseWrapper(self):
        return self._databaseWrapper
    
    def createAccount(self,username, password, permission, firstName, surname, initials):
        """see :func:`restAccounts.createAccount` for more info"""
        return restAccounts.createAccount(self,username, password, permission, firstName, surname, initials)
    
    def deleteAccount(self,username):
        """see :func:`restAccounts.deleteAccount` for more info"""
        return restAccounts.deleteAccount(self,username)
    
    def getAllAccountDocs(self,username):
        """see :func:`restAccounts.getAllAccountDocs` for more info"""
        return restAccounts.getAllAccountDocs(self,username)

    def getAuthors(self, pubId):
        """see :func:`restRetrieval.getAuthors` for more info"""
        return restRetrieval.getAuthors(self, pubId)

    def getAllAuthors(self):
        """see :func:`restRetrieval.getAllAuthors` for more info"""
        return restRetrieval.getAllAuthors(self)
        
    def getAllDocuments(self, skip, length, sortBy, sort):
        """see :func:`restRetrieval.getAllDocuments` for more info"""
        return restRetrieval.getAllDocuments(self, skip, length, sortBy, sort)

    def getDocumentDetails(self, id):
        """see :func:`restRetrieval.getDocumentDetails` for more info"""
        return restRetrieval.getDocumentDetails(self, id)
    
    def getExtraDocuments(self, pubId):  
        """see :func:`restRetrieval.getExtraDocuments` for more info"""
        return restRetrieval.getExtraDocuments(self, pubId) 
    
    def getLoginCredentials(self,username):
        """see :func:`restRetrieval.getLoginCredentials` for more info"""
        return restRetrieval.getLoginCredentials(self,username)
        
    def insertDocument(self, details):
        return restInsertion.insertDocument(self, details)

    def simpleSearch(self, searchTerms, skip, length, sortBy, sort):
        return restSearch.simpleSearch(self, searchTerms, skip, length, sortBy, sort)
   
    def sortDocuments(self,sortBy, sort):
        return restSearch.sortDocuments(self, sortBy, sort)

    def getAdvancedSearchFields(self):
        return restSearch.getAdvancedSearchFields()
    
    def getCSVFormats(self):
        return restInsertion.getCSVFormats(self)

    def advancedSearch(self, searchTerms, skip, length, sortBy, sort):
        return restSearch.advancedSearch(self, searchTerms, skip, length, sortBy, sort) 

    def accreditPublication(self, publicationID) :
        return restInsertion.insertPublicationAcceditation(self, publicationID)
    
    def updateAccredited(self, accreditedCSV):
        return restAccounts.updateAccredited(self, accreditedCSV)
    
    def updatePredatory(self, predatoryCSV):
        return restAccounts.updatePredatory(self,predatoryCSV)
    
    def updateHIndex(self,HIndexCSV):
        return restAccounts.updateHIndex(self,HIndexCSV)


        
        
        

    



