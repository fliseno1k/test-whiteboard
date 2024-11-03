class Shape:
    def __init__(self):
        self.left: int = 0
        self.top: int = 0
        self.width: int = 0
        self.height: int = 0
        self.background_color: str | None


class Rectangle(Shape):
    def __init__(self):
        super().__init__()


class Connector(Shape):
    def __init__(self):
        super().__init__()
