#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi, os
import sys
import json


def main(details):
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
    fileitem=details["PublicationFile"]["data"]
    newFile = open ("somefile" + ".pdf", "wb")
    newFile.write(fileitem)
        
        
        
        
    
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