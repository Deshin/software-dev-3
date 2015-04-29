#Abstract base class used to specify the interface for database wrappers
import abc

class WrapperBase(object):
    __metaclass__=abc.ABCMeta
    
    @abc.abstractmethod
    def connect(self):
        """Connect to the specified database"""
    
    @abc.abstractmethod
    def disconnect(self):
        """Disconnect from the specified database"""
        
    
    @abc.abstractmethod
    def query(self, queryString):
        """Search using a query string"""
        return