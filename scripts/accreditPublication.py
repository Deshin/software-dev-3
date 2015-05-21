#!/usr/bin/env python
import cgi
from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main(publicationID):
    db = SqliteWrapper()
    rest = RestApi(db)
    print "Status:200"
    print "Content-Type: text/html"
    print ""
    print "Success"
    rest.accreditPublication(publicationID)

if __name__ == "__main__":
    form = cgi.FieldStorage()
    publicationID = form.getvalue("publicationID", None)
    main(publicationID)    

         


 
