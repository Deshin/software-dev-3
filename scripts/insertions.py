#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi, os
import sys
import json
import cgitb; cgitb.enable()

def main(details):
    db = SqliteWrapper()
    rest = RestApi(db)
    result= rest.insertDocument(details)
    if result[0]=="400":
        print "Status:400"
        print "Content-Type: text/html"
        print ""
        print "The document could not be added to the database"
        print result[1]
    else:
        print "Status:200"
        print "Content-Type: text/html"
        print "Success"

if __name__ == "__main__":
    details = json.load(sys.stdin)

# try: # Windows needs stdio set for binary mode.
#     import msvcrt
#     msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
#     msvcrt.setmode (1, os.O_BINARY) # stdout = 1
# except ImportError:
#     pass
# 
# form = cgi.FieldStorage()
# 
# # A nested FieldStorage instance holds the file
# fileitem = form['file']
# 
# # Test if the file was uploaded
# if fileitem.filename:
#    
#    # strip leading path from file name to avoid directory traversal attacks
#    fn = os.path.basename(fileitem.filename)
#    open('files/' + fn, 'wb').write(fileitem.file.read())
#    message = 'The file "' + fn + '" was uploaded successfully'
#    
# else:
#    message = 'No file was uploaded'
    
    
    
    
    
#     details={"Title": "blah",
#              "Category": "Journal Aricle",
#              "JournalTitle": "blah",
#              "PeerReviewProcess":"blah",
#              "Year": "2013",
#              "Publisher": "blah", 
#              "ISSN":"1234567",
#              "Authors":[{"FirstName": "Sarah", "Surname": "Ward", "Initials": "S.R"}, {"FirstName": "Anthony", "Surname": "Farquharson", "Initials":"A.J."}]}
    main(details)