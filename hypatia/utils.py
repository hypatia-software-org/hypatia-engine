import pygame

def compare_surfaces(a, b):
    """\
    Compare the two given surfaces, returning True if they are identical.
    """

    if a.get_size() != b.get_size():
        return False

    for y in range(a.get_height()):
        for x in range(a.get_width()):
            if a.get_at((x, y)) != b.get_at((x, y)):
                return False

    return True
