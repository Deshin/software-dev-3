#A wrapper class for sqlite. Implimentation is determined by the WrapperBase class
import abc
from DatabaseWrapper
import sqlite3

class SqliteWrapper(DatabaseWrapper):

    def __init__(self):
        self._database= "../db/elen4010.sqlite3"
        self._cur=[]
        self._con=[]

#Function allowing a connection to a database to be established        
    def connect(self):
        try:
            self._con=sqlite3.connect(self._database)
            self._cur=self._con.cursor()
            print "Connecting to Database "+self._database
        except sqlite3.Error,e:
            print "Error %s:" %e.args[0]
            raise
        
#Function allowing one to disconnect from a database       
    def disconnect(self):
        self._con.close()
        print "Disconnecting from the Database"

#Function to perform an SQL query and return any results if applicable        
    def query(self, queryString):
        try:
            self._cur.execute(queryString)
            if queryString.startswith("SELECT"):
                items=self._cur.fetchall()  
                return items                      
        except sqlite3.Error,e:
            print "Error %s:" %e.args[0]
            raise
        print "The query string is "+queryString
        
    
# if __name__=='__main__':
#     wrapper=SqliteWrapper("arb database")
#     wrapper.connect()
#     wrapper.query('SELECT SQLITE_VERSION()')
#     wrapper.disconnect()
