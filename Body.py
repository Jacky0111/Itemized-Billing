from Bill import Bill


class Body(Bill):
    TYPE_BODY = 'body'  # Type of content

    def __init__(self, x=0, y=0, width=0, height=0, conf=0, text=None, identity=None):
        super().__init__(x, y, width, height, conf, text, identity)
        self.identity = self.TYPE_BODY

    '''
    Execute function
    '''
    def runner(self):
        print('---------------------------------------This row is Body---------------------------------------')
        print('-------------------------------------Assigning Coordinate-------------------------------------')
        whole = super().assignCoordinate(df)

    def __str__(self):
        return super.__str__(self)
