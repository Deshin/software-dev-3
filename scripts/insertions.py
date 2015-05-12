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
    else:
        print "Status:200"
        print "Content-Type: text/html"
        print "Success"
        print result    

if __name__ == "__main__":
    form=cgi.FieldStorage()
    details=form.getlist('publication')
    details={"Title": "This document is testing conference paper insertion",
             "Category": "Conference paper",
             "Year": 2015,
             "Publisher": "Testing publishers", 
             "TableOfContentsPath": "conferences\PRASA2014\TOC\PRASA2014-3",
             "ScanPath": "conferences\PRASA2014\Publications\TestingInsertion3",
             "Accreditation": "Not Accredited",
             "Abstract": "It is important to have a document to test adding to the database",
             "MotivationForAccreditation": "Please accredit me!",
             "PeerReview": "People read it :)",
             "ConferenceTitle": "PRASA",
             "Country": "South Africa"}
    main(details)