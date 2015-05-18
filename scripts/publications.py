#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main(arg):
    db = SqliteWrapper()
    rest = RestApi(db)
    if arg == None:
        result = rest.getAllDocuments()
    else 
        result = rest.simpleSearch(arg)
    if result == "404":
        print "Status:404"
        print "Content-Type: text/html"
        print ""
        print "404 - No documents were found."
    else:
        print "Content-Type: application/json"
        print ""
        print result

if __name__ == "__main__":
    form = cgi.Fieldstorage()
    search = form.getValue("simpleSearch", None)
    main(search)    
