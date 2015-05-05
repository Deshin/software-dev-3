#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi

def main(details):
    db = SqliteWrapper()
    rest = RestApi(db)
    result = rest.insertDocument(details)
    if result=="404":
        print "Status:404"
        print "Content-Type: text/html"
        print ""
        print "The document could not be added to the database"
    print "Content-Type: application/json"
    print "Success"
    print result    

if __name__ == "__main__":
    form=cgi.FieldStorage()
    id=form.getlist('details')
    main(details)