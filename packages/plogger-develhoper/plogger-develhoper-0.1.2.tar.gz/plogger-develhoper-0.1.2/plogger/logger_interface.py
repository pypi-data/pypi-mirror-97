from abc import ABC, abstractmethod

class LoggerInterface(ABC):

    @abstractmethod
    def write(self,message):
        pass


class DefaultOutput(LoggerInterface):

    def write(self,message):
        print(message)
