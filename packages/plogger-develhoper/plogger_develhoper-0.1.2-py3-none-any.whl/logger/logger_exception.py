class LoggerException(Exception):
    
    def __init__(self,message):
        super(LoggerException,self).__init__(message)
