from hypatia import class_override, class_get, class_list
from hypatia.camera import Camera

def test_interaction():
    return {
        "say": ["My camera class is %r!" % class_get("Camera")]
    }

@class_override("Camera")
class MyCamera(class_get("Camera")):
    pass
