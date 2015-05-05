#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi

def main(id):
    db = SqliteWrapper()
    rest = RestApi(db)
    result = rest.getDocumentDetails(id)
    if result=="404":
        print "Status:404"
        print "Content-Type: text/html"
        print ""
        print "404 - No document details were found"
    print "Content-Type: application/json"
    print ""
    print result    

if __name__ == "__main__":
    form=cgi.FieldStorage()
    id=form.getlist('id')[0]
    main(str(id))
