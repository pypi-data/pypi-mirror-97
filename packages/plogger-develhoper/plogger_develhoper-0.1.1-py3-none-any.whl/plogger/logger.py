from .logger_interface import LoggerInterface,DefaultOutput
from .logger_exception import LoggerException

class Logger:

    __instance=None
    __output=None

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
            self.__output=DefaultOutput()
            Logger.__instance=self
        

    def log(self,title,message,format="[{title}] {message}",output=None):

        if output is None:
            output=self.__output

        if not isinstance(output, LoggerInterface):
            raise LoggerException("output must be instance of LoggerInterface")

        output.write(format.format(title=title,message=message))
