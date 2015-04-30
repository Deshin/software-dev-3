import RestApi
import SqliteWrapper
import CgiResponse

def main():
    db = SqliteWrapper()
    rest = RestApi(db)
    rest.getDocuments().send()    

if __name__ == "__main__":
    main()
