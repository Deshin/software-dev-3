#!/usr/bin/env python

#A wrapper class for sqlite. Implimentation is determined by the DatabaseWrapper class
import abc
from DatabaseWrapper import DatabaseWrapper
import sqlite3

class SqliteWrapper(DatabaseWrapper):
#Initialisation
    def __init__(self):
        self._database= "../db/elen4010.sqlite3"
        self._cur=[]
        self._con=[]

#Function allowing a connection to a database to be established        
    def connect(self):
        try:
            self._con=sqlite3.connect(self._database)
            sqlite3.isolation_level = None
            self._cur=self._con.cursor()
        except sqlite3.Error,e:
            #print "Error %s:" %e.args[0]
            raise
        
#Function allowing one to disconnect from a database       
    def disconnect(self):
        self._con.close()

#Function to perform an SQL query and return any results if applicable        
    def query(self, queryString, values=()):
        try:
            self._cur.execute(queryString, values)
            if queryString.startswith("SELECT"):
                items=self._cur.fetchall()
                return items 
                                 
        except sqlite3.Error,e:
            #print "Error %s:" %e.args[0]
            raise
        
    def commit(self):
        try:
            self._con.commit()
        except sqlite3.Error,e:
            raise
