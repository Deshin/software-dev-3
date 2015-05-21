#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi, os
import sys
import json
import base64


def main(details):
    db = SqliteWrapper()
    rest = RestApi(db)
    result="404"
    for item in details:
        if item["format"]=="DHET" or item["format"]==IBSS or item["format"]==ISI:
            result= rest.updateAccredited(self, details)
        elif item["format"]=="Predatory":
            result= rest.updatePredatory(self, predatoryCSV)
        elif item["format"]=="H-Index":
            result= rest.updateHIndex(self,HIndexCSV)
            
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
              
    main(details)