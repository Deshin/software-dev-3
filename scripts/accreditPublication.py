#!/usr/bin/env python
"""RESTful endpoint for setting the accreditation status of a Publication"""
import cgi
from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main(publicationID):
    """ Accredits the publication

    :param publicationID: An integer that uniquely identifies a publication in the database

    see :func:`restInsertion.insertPublicationAccreditation` for more info """

    db = SqliteWrapper()
    rest = RestApi(db)
    print "Status:200"
    print "Content-Type: text/html"
    print ""
    print "Success"
    rest.accreditPublication(publicationID)

if __name__ == "__main__":
    form = cgi.FieldStorage()
    publicationID = form.getvalue("publicationID", None)
    main(publicationID)    

         


 
