class ResourceException(Exception):
    pass

class NotADirectory(ResourceException):
    pass

class NotAFile(ResourceException):
    pass

class FileNotFound(ResourceException):
    pass

class FileExists(ResourceException):
    pass


