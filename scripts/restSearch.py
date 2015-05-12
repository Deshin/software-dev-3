def simpleSearch(self, searchTerms):
    # searchTerms is a list of strings
    return Pubs = self._databaseWrapper.query(
        """
        SELECT  Publications.PublicationID, 
                Publications.Title
        FROM Publications JOIN Authors
                ON  Publications.PublicationID=Authors.PublicationID
        WHERE 
            Authors.FirstName LIKE ? OR
            Authors.Surname LIKE ? OR
            Publications.Title LIKE ?

        UNION

        SELECT  BookPublications.PublicationId, 
                BookPublications.Title 
        FROM BookPublications JOIN Authors 
                ON  BookPublications.PublicationID=Authors.PublicationID
        WHERE 
            Authors.FirstName LIKE ? OR
            Authors.Surname LIKE ?  
            BookPublications.Title Like ?

        UNION

        SELECT  ConferencePublicationDetail.PublicationId,
                ConferencePublicationDetail.Title
        FROM ConferencePublicationDetail JOIN Authors 
                ON  ConferencePublicationDetail.PublicationID =
                    Authors.PublicationID 
        WHERE 
            Authors.FirstName LIKE ? OR
            Authors.Surname LIKE ?  
            ConferencePublicationDetail.Title LIKE ?

        UNION
        
        SELECT  JounalPublicationDetail.PublicationId,
                JounalPublicationDetail.Title
        FROM JounalPublicationDetail JOIN Authors 
                ON  JounalPublicationDetail.PublicationID = 
                    Authors.PublicationID 
        WHERE 
            Authors.FirstName LIKE ? OR
            Authors.Surname LIKE ?  
            JournalPublicationDetail.Title LIKE ?
        """)

