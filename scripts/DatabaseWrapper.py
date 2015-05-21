#!/usr/bin/env python

#Abstract base class used to specify the interface for database wrappers
import abc

class DatabaseWrapper(object):
    """Abstract base class for a database-wrapper.

    Has methods that must be overloaded so that any SQL-database may be wrapped and used in the back-end"""
    __metaclass__=abc.ABCMeta
    
    @abc.abstractmethod
    def connect(self):
        """Connect to the specified database"""
    
    @abc.abstractmethod
    def disconnect(self):
        """Disconnect from the specified database"""
        
    @abc.abstractmethod
    def query(self, queryString, value):
        """Search using a query string"""
        return
    
    @abc.abstractmethod
    def commit(self):
        """Search using a query string"""
        return
