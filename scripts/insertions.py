#!/usr/bin/env python
"""RESTful endpoint for inserting a document into the database."""

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi, os
import sys
import json
import base64


def main(details):
    """Runs and prints the output of :func:`restInsertion.insertDocument`, the result of attempting to insert a document into the database."""
    db = SqliteWrapper()
    rest = RestApi(db)
    result= rest.insertDocument(details)
    if result[0]=="400":
        print "Status:400"
        print "Content-Type: text/html"
        print ""
        print "The document could not be added to the database because "
        print result[1]
    else:
        print "Status:200"
        print "Content-Type: text/html"
        print ""
        print "Success"

if __name__ == "__main__":
    details = json.load(sys.stdin)
              
    
#     details={"Title": "blah",
#              "Abstract": "blah",
#              "Category": "Journal Aricle",
#              "JournalTitle": "blah",
#              "PeerReviewProcess":"blah",
#              "Year": "2013",
#              "Publisher": "blah", 
#              "ISSN":"1234567",
#              "Authors":[{"FirstName": "Sarah", "Surname": "Ward", "Initials": "S.R"}, {"FirstName": "Anthony", "Surname": "Farquharson", "Initials":"A.J."}]}
    main(details)
