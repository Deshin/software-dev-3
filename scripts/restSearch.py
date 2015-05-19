import json

def simpleSearch(self, searchTerm, skip, length, sortBy, sort):
    # searchTerms is a list of strings
    query = "SELECT  Publications.* "\
        "FROM Publications JOIN Authors ON Authors.PublicationID=Publications.ID "\
        "WHERE "\
        "Authors.FirstName LIKE ? OR "\
        "Authors.Surname Like ? OR "\
        "Publications.Title LIKE ? "\
        "GROUP BY Publications.Title "+sortDocuments(self,sortBy, sort)+\
        "LIMIT ? OFFSET ? "
    pubs = self._databaseWrapper.query(query, ('%'+searchTerm+'%','%'+searchTerm+'%','%'+searchTerm+'%', length, skip))
    if pubs == []:
        return "200"
    data = []
    for i in range(0,len(pubs)):
        auths = self._databaseWrapper.query("SELECT * FROM Authors WHERE PublicationID=? ", (str(pubs[i][0]),))
        auth = []
        for j in range(0, len(auths)):
            auth.append({"ID":auths[j][0], "PublicationID":auths[j][1], "First Name" : auths[j][2], "Surname" : auths[j][3],  "Initials" : auths[j][4]})
        data.append({"PublicationId" : pubs[i][0], "Title" : pubs[i][1], "Category" : pubs[i][2], "Year" : pubs[i][3], "Publisher" :pubs[i][4], "Authors" : auth})
    return json.dumps(data)

def sortDocuments(self, sortBy, sort):
    validSortBy=["Title", "Category", "Year", "Publisher"]
    validSort=["ASC", "DESC"]
    
    sortString=""
    
    if sortBy in validSortBy and sort in validSort:
        if sortBy!="Title":
            sortString=" ORDER By "+sortBy+" COLLATE NOCASE "+sort+ " ,Title COLLATE NOCASE ASC "
        sortString=" ORDER BY "+sortBy+" COLLATE NOCASE "+sort+" "
        
    return sortString