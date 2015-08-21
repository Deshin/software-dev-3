#!/usr/bin/env python

import RestApi as ra
import SqliteWrapper as sw
import cgi
import string

def makeSearchTerms(search):
    for p in string.punctuation:
        search = search.replace(p, "")
    return search.split()

def searchBy(pubs, field, term):
    result = []
    for pub in pubs:
        if term in pub[field]:
            result.append(pub) 

def main(search):
    db = sw.SqliteWrapper()
    rest = ra.RestApi(db)
    allDocs = rest.getAllDocuments()
    if result == "404":
        print "Status:404"
        print "Content-Type: text/html"
        print ""
        print "No document details were found"   
        return
    
    terms = makeSearchTerms(search)
    fields = ["Title", "Year"]

    for term in terms:
        for field in fields:
            results = results + searchBy(allDocs, field, term)
        




if __name__ == "__main__":
    form = cgi.FieldStorage()
    searchString = form.getlist("searchString")[0]
    main(str(searchString))
