import random
from PySide6.QtGui import QColor


def rand_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return QColor(r, g, b)
