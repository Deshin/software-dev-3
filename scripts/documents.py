from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
from DatabaseWrapper import DatabaseWrapper 
import CgiResponse

def main():
    db = SqliteWrapper()
    rest = RestApi(db)
    cgiResponse = rest.getAllDocuments()
    cgiResponse.send()

if __name__ == "__main__":
    main()
