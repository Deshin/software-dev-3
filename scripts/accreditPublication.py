#!/usr/bin/env python
import cgi

def main(publicationID):
    db = SqliteWrapper()
    rest = RestApi(db)
    rest.insertPublicationAccreditation(publicationID, True)

if __name__ == "__main__":
    form = cgi.FieldStorage()
    publicationID = form.getvalue("publicationID", None)
    main(publicationID)    

         


 
