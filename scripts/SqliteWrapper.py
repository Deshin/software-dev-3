#A wrapper class for sqlite. Implimentation is determined by the WrapperBase class
import abc
from WrapperBase import WrapperBase
import sqlite3

class SqliteWrapper(WrapperBase):
    def __init__(self, database):
        self._database=database
        self._cur=[]
        self._con=[]
        
    def connect(self):
        try:
            self._con=sqlite3.connect(self._database)
            self._cur=self._con.cursor()
            print "Connecting to Database "+self._database
        except sqlite3.Error,e:
            print "Error %s:" %e.args[0]
            sys.exit(1)
        
    def disconnect(self):
        self._con.close()
        print "Disconnecting from the Database"
        
    def query(self, queryString):
        print "The query string is "+queryString
        return queryString
    
if __name__=='__main__':
    wrapper=SqliteWrapper("arb database")
    wrapper.connect()
    wrapper.query("this is a query")
    wrapper.disconnect()
