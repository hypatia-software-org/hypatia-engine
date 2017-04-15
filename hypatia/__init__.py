__version__ = '0.4.0-alpha'

class_list = {}

def _import_all():
    """\
    Import all the Hypatia Engine game classes.
    """

    import hypatia.animatedsprite
    import hypatia.camera
    import hypatia.character
    import hypatia.default_config
    import hypatia.game
    import hypatia.test_mocks
    import hypatia.tile
    import hypatia.tilemap
    import hypatia.tilesheet
    import hypatia.utils

    import hypatia.scenes
    import hypatia.scenes.textbox
    import hypatia.scenes.tilemap
    import hypatia.scenes.traceback

    import hypatia.resources
    import hypatia.resources.bytesio
    import hypatia.resources.exceptions
    import hypatia.resources.filesystem

def class_default(cls):
    """\
    Specify that the decorated class is the default class for it's name.
    """

    global class_list
    class_list[cls.__name__] = cls

    return cls

def class_override(class_name):
    """\
    Override a game class by the name of class_name.
    """

    def wrapper(cls):
        global class_list
        class_list[class_name] = cls

        return cls

    return wrapper

def class_get(class_name):
    """\
    Get the game class by the given class_name from the override list.
    """

    global class_list
    return class_list.get(class_name, None)
