from Bill import Bill


class Header(Bill):
    TYPE_HEAD = 'head'  # Type of content

    def __init__(self, x=0, y=0, width=0, height=0, conf=0, text=None, identity=None):
        super().__init__(x, y, width, height, conf, text, identity)
        self.identity = self.TYPE_HEAD

    def __str__(self):
        return super.__str__(self)
