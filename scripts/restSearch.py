def simpleSearch(self, searchTerm):
    # searchTerms is a list of strings
    query = "SELECT  Publications.Title, Publications.Category "\
        "FROM Publications JOIN Authors "\
                "ON Publications.ID=Authors.PublicationID "\
        "WHERE "\
            "Authors.FirstName LIKE ? OR "\
            "Authors.Surname LIKE ? OR "\
            "Publications.Title LIKE ?"
    return self._databaseWrapper.query(query, [searchTerm for i in range(0,3)])

