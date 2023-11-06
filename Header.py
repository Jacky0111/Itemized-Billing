from Bill import Bill


class Header(Bill):
    header_data = []
    TYPE_HEAD = 'head'  # Type of content

    def __init__(self, x=0, y=0, width=0, height=0, conf=0, text=None, identity=None):
        super().__init__(x, y, width, height, conf, text, identity)
        self.identity = self.TYPE_HEAD

    '''
    Execute function
    '''
    def runner(self, df):
        print('------------------------------------ -This row is Header--------------------------------------')
        print('-------------------------------------Assigning Coordinate-------------------------------------')
        data = super().assignCoordinate(df)
        print('----------------------------------Adjusting Column Threshold----------------------------------')
        self.columnThreshold(data)

    def columnThreshold(self, text_list):
        midpoint = 0

        if text_list is None:
            return

        for index, ele in enumerate(text_list):
            x1 = ele.x
            w1 = ele.width
            x2 = text_list[index+1].x if not index == len(text_list) - 1 else 0

            print(f'Before      x1:{x1}, w1: {w1}, x2: {x2}')

            if index == 0:  # First element of the list
                continue
            elif index == 1:
                midpoint = (x2 - (x1 + w1)) / 2
                ele.x = x1 - midpoint
                ele.width = (x1 + w1) + midpoint
                text_list[index-1].width = ele.x
            elif index == len(text_list) - 1:  # Last element of the list
                ele.x = x1 - midpoint
            else:
                ele.x = x1 - midpoint
                midpoint = (x2 - (x1 + w1)) / 2
                ele.width = (x1 + w1) + midpoint

            print(f'After       x1:{x1}, w1: {w1}, x2: {x2}')
            print()

    def __str__(self):
        return super.__str__(self)
