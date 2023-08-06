from .logger_interface import LoggerInterface,DefaultOutput
from .logger_exception import LoggerException

class Logger:

    __instance=None
    __output__=None
    __format__ = "[{title}] {message}"

    @staticmethod
    def getInstance():
        if Logger.__instance is not None:
            return Singleton.__instance
        else:
            Logger()
            return Logger.__instance

    def __init__(self):
        if Logger.__instance is not None:
            raise Exception("This class is a Singleton")
        else:
            self.__output__=DefaultOutput()
            Logger.__instance=self
        
    def setOuput(self,output):
        if not isinstance(output,LoggerInterface):
            raise LoggerException("Output must be instance of LoggerInterface")
        
        self.__output__=output


    def log(self,title,message,format=None,output=None):

        if output is None:
            output=self.__output__
        else:
            self.__output__=output

        if not isinstance(output, LoggerInterface):
            raise LoggerException("output must be instance of LoggerInterface")

        if format is None:
            format = self.__format__

        output.write(format.format(title=title,message=message))

    
    def info(self,message,format=None,output=None):
        self.log("INFO",message,format,output)

    def warning(self,message,format=None,output=None):
        self.log("WARNING",message,format=format,output=output)

    def error(self,message,format=None,output=None):
        self.log("ERROR",message,format=format,output=output)
