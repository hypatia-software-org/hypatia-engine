from hypatia import class_default, class_get

@class_default
class ResourceException(Exception):
    pass

@class_default
class NotADirectory(class_get("ResourceException")):
    pass

@class_default
class NotAFile(class_get("ResourceException")):
    pass

@class_default
class FileNotFound(class_get("ResourceException")):
    pass

@class_default
class FileExists(class_get("ResourceException")):
    pass


