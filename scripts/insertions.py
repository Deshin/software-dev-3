#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi

def main(details):
    db = SqliteWrapper()
    rest = RestApi(db)
    result= rest.insertDocument(details)
    if result[0]=="404":
        print "Status:404"
        print "Content-Type: text/html"
        print ""
        print "The document could not be added to the database"
        print result[1]
    else:
        print "Status:200"
        print "Content-Type: text/html"
        print "Success"

if __name__ == "__main__":
    form=cgi.FieldStorage()
    details=form.getlist('publication')
#     details={"Title": "This document is testing book section insertion",
#              "Category": "Book section",
#              "Year": 2015,
#              "Chapter":3,
#              "Publisher": "Testing publishers", 
#              "TableOfContentsPath": "books\arbBook\TOC\TestingInsertion",
#              "ScanPath": "books\arbBook\Publications\TestingInsertion3",
#              "Accreditation": "Not Accredited",
#              "Abstract": "It is important to have a document to test adding to the database",
#              "BookTitle": "PRASA",
#              "ISBN":1234567,
#              "Type":"Accredited",
#              "Authors":[{"FirstName": "Sarah", "Surname": "Ward", "Initials": "S.R"}, {"FirstName": "Anthony", "Surname": "Farquharson", "Initials":"A.J."}]}
    main(details)