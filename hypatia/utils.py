import pygame

from PIL import Image, ImageFilter


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

def keyname_to_keysym(keyname):
    if keyname.startswith("K_"):
        return getattr(pygame, keyname, None)

    return None

def keysym_to_keyname(keysym):
    for i in [a for a in dir(pygame) if a.startswith("K_")]:
        if getattr(pygame, i, None) == keysym:
            return i
    
    return None

def wrap_line(font, target_width, line):
    lines = []
    currentline = []
    words = line.split()

    if font.size(line)[0] <= target_width:
        return [line]

    i = 0

    while True:
        length = 0

        while length <= target_width:
            if len(words) is 0:
                break

            word = words.pop(0)
            currentline.append(word)
            length = font.size(" ".join(currentline))[0]

        if len(currentline) is 0:
            break

        lines.append(" ".join(currentline))
        currentline = []

    return lines

def blur_surface(surface, radius=6):
    size = surface.get_size()
    data = pygame.image.tostring(surface, "RGBA")

    pil_image = Image.frombytes("RGBA", size, data)
    pil_blurred = pil_image.filter(ImageFilter.GaussianBlur(radius=radius))
    pil_data = pil_blurred.tobytes("raw", "RGBA")

    pygame_blurred = pygame.image.fromstring(pil_data, size, "RGBA")

    return pygame_blurred
