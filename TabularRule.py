class TabularRule:
    first = None  # Header condition
    data = []
    row_list = []

    def __init__(self, data, first):
        self.data = data
        self.first = first
        self.row_list = []

    def runner(self):
        self.tableRules()
        self.headerRules() if self.first is True else self.contentRules()

    def tableRules(self):
        content = ''

        # for index, (x1, text) in enumerate(zip(self.data['left'], self.data['text'])):
        for index, row in enumerate(self.data):
            x1 = row.x
            text = row.text
            previous_row = self.data[index - 1]
            x2 = previous_row.x
            w2 = previous_row.width
            distance = x1 - (x2 + w2)

            if TabularRule.rule1(self.data):
                print('Comply Rule 1')
                self.row_list = [text]
            elif TabularRule.rule2(index):
                print('Comply Rule 2')
                content = text
            elif TabularRule.rule3(distance, index, self.data):
                print('Comply Rule 3')
                self.row_list.append(content)
            elif TabularRule.rule4(distance):
                print('Comply Rule 4')
                content += ' ' + text
            elif TabularRule.rule5(distance, index, self.data):
                print('Comply Rule 5')
                self.row_list.append(content)
                content = text
                self.row_list.append(content)
            elif TabularRule.rule6(distance):
                print('Comply Rule 6')
                self.row_list.append(content)
                content = text

    def headerRules(self):
        midpoint = 0

        if self.data is None:
            return

        for index, ele in enumerate(self.data):
            x1 = ele.x
            w1 = ele.width
            x2 = self.data[index + 1].x if not index == len(self.data) - 1 else 0

            print(f'Before      x1:{x1}, w1: {w1}, x2: {x2}')

            if index == 0:  # First element of the list
                continue
            elif index == 1:
                midpoint = (x2 - (x1 + w1)) / 2
                ele.x = x1 - midpoint
                ele.width = (x1 + w1) + midpoint
                self.data[index - 1].width = ele.x
            elif index == len(self.data) - 1:  # Last element of the list
                ele.x = x1 - midpoint
            else:
                ele.x = x1 - midpoint
                midpoint = (x2 - (x1 + w1)) / 2
                ele.width = (x1 + w1) + midpoint

            print(f'After       x1:{ele.x}, w1: {ele.width}, x2: {x2}')
            print()

    def contentRules(self):
        pass

    '''
    Rule 1: If the row only has 1 element.
    @param data
    @return True if rule is applied, False otherwise.
    '''

    @staticmethod
    def rule1(data):
        return len(data) == 1

    '''
    Rule 2: If the first element of the row.
    @param counter
    @return True if rule is applied, False otherwise.
    '''

    @staticmethod
    def rule2(counter):
        return counter == 0

    '''
    Rule 3: If the distance is lower than 40 and last element of the row.
    @param dist
    @param counter
    @param data
    @return True if rule is applied, False otherwise.
    '''

    @staticmethod
    def rule3(dist, counter, data):
        return dist < 40 and counter == len(data) - 1

    '''
    Rule 4: If the distance is lower than 40.
    @param dist
    @return True if rule is applied, False otherwise.
    '''

    @staticmethod
    def rule4(dist):
        return dist < 40

    '''
    Rule 5: If the distance is higher or equal to 40 and last element of the row.
    @param dist
    @param counter
    @param data
    @return True if rule is applied, False otherwise.
    '''

    @staticmethod
    def rule5(dist, counter, data):
        return dist >= 40 and counter == len(data) - 1

    '''
    Rule 6: If the distance is higher or equal to 40.
    @param dist
    @return True if rule is applied, False otherwise.
    '''

    @staticmethod
    def rule6(dist):
        return dist >= 40

    '''
    Rule 7: For KPJ hospital bill, add "Item" as the first column name.
    @param dist
    @return True if rule is applied, False otherwise.
    '''

    @staticmethod
    def rule7(dist):
        return dist >= 40
