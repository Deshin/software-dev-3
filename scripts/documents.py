import RestApi
import SqliteWrapper
import CgiResponse

def main():
    db = SqliteWrapper()
    rest = RestApi(db)
    cgiResponse = rest.getAllDocuments()
    cgiResponse.send()

if __name__ == "__main__":
    main()
