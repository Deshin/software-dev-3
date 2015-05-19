import json

def simpleSearch(self, searchTerm):
    # searchTerms is a list of strings
    query = "SELECT  * "\
        "FROM Publications "\
        "WHERE "\
        "Publications.Title LIKE ?"
    pubs = self._databaseWrapper.query(query, ('%'+searchTerm+'%',))
    if pubs == []:
        return "200"
    data = []
    for i in range(0,len(pubs)):
        auths = self._databaseWrapper.query("SELECT * FROM Authors WHERE (FirstName LIKE ? OR Surname LIKE ?) AND PublicationID="+str(pubs[i][0]), [('%'+searchTerm+'%') for k in range(0,2)])
        auth = []
        for j in range(0, len(auths)):
            auth.append({"ID":auths[j][0], "PublicationID":auths[j][1], "First Name" : auths[j][2], "Surname" : auths[j][3],  "Initials" : auths[j][4]})
        data.append({"PublicationId" : pubs[i][0], "Title" : pubs[i][1], "Category" : pubs[i][2], "Year" : pubs[i][3], "Publisher" :pubs[i][4], "Authors" : auth})
    return json.dumps(data)
