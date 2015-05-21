#!/usr/bin/env python

#A wrapper class for sqlite. Implimentation is determined by the DatabaseWrapper class
import abc
from DatabaseWrapper import DatabaseWrapper
import sqlite3

class SqliteWrapper(DatabaseWrapper):
    """Wrapper class for sqlite3, enabling it's use in the back-end"""

    def __init__(self):
        self._database= "../db/elen4010.sqlite3"
        self._cur=[]
        self._con=[]

    def connect(self):
    """ Allows for a connection to a database to be established."""
        try:
            self._con=sqlite3.connect(self._database)
            sqlite3.isolation_level = None
            self._cur=self._con.cursor()
        except sqlite3.Error,e:
            raise
        
    def disconnect(self):
    """ Allows for disconnection from a database """
        self._con.close()

    def query(self, queryString, values=()):
    """ Performs and returns the results of an SQL query

    :param queryString: A SQL query string, with the variables replaced with '?'
    :param values: A tuple containing string values to be substituted into the place of the ?'s in the query string. """
        try:
            self._cur.execute(queryString, values)
            if queryString.startswith("SELECT"):
                items=self._cur.fetchall()
                return items 
                                 
        except sqlite3.Error,e:
            raise
        
    def commit(self):
        try:
            self._con.commit()
        except sqlite3.Error,e:
            raise
