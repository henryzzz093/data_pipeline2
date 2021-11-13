from PIL import Image


def get_image(path, size=200):
    image = Image.open(path)
    image = image.resize((size, size))
    return image
