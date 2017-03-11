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

def pillow_image_to_pygame_surface(image):
    image_as_bytes = image.convert("RGBA").tobytes()
    return pygame.image.fromstring(image_as_bytes, image.size, "RGBA")
