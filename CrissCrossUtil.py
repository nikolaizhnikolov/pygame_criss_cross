def load_image(path: str) -> pygame.surface:
    image = pygame.image.load(path).convert()
    if path.__contains__('png'):
        image.set_colorkey((0, 0, 255))
    return image


def scale_image(image: pygame.surface, width: int, height: int) -> pygame.surface:
    return pygame.transform.scale(image, (width, height))
