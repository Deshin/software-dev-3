#!/usr/bin/env python
""" RESTful endpoint for accrediting a document """

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi, os
import sys
import json
import base64


def main(details):
    """ Runs and prints the results of :func:`restAccounts.updateAccredited`, :func:`restAccounts.updatePredatory or :func:`restAccounts.updateHIndex` """
    db = SqliteWrapper()
    rest = RestApi(db)
    result="404"
    for item in details:
        if item["type"]=="Accredited":
            rest.updateAccredited(item)
        elif item["type"]=="Predatory":
            result= rest.updatePredatory(item)
        elif item["type"]=="H-Index":
            result= rest.updateHIndex(item)
        
    if result=="400":
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
    db = SqliteWrapper()
    rest = RestApi(db)
              
    main(details)