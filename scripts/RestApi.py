import WrapperBase

class RESTAPI:
    def __init__(self, databaseWrapper):
        self._databaseWrapper = databaseWrapper

    @property
    def databaseWrapper(self):
        return databaseWrapper

    def getScan(scanId):
        queryString = "balls"
        scanPath = dataBasewrapper.query(queryString)
        return scanPath

# TODO What functions do we need? just getX where X is a thing in the DB?
# I have to pick up Dani from MM, will work more on this later...
