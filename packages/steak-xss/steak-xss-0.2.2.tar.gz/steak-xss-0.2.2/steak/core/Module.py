from .Payload import Payload
from steak.utils import steak_format
from .Logger import Logger
import os
class Module:
    '''
    The Module class is the base class for attack modules
    Users can derive this class and build their own attack modules.
    '''
    def __init__(self,**kwargs) -> None:
        self.logger = Logger()
        try:
            self.logger.debug(f'Reading Moudle javascript from steak/modules/{self.__class__.__name__}/command.js')
            jspath=os.path.join(os.path.dirname(__file__),f'../modules/{self.__class__.__name__}/command.js')
            self.jstemplate=open(jspath).read()
        except FileNotFoundError:
            raise Exception(f'Javascript source file not found in {jspath}, we expect you to place one there')
        self.kwargs=kwargs
        self.jspayload=steak_format(self.jstemplate,**self.kwargs)
        self.payload=self.get_jspayload()

    
    def get_jspayload(self)->Payload:
        '''
        Constructs a Payload object that is to be sent to user
        '''
        return Payload(self.jspayload,self)
    
    def parse_result(self,result):
        '''
        Parses the result submited by the client
        Users can implement their own parse_result function to extract information they need
        '''
        return result