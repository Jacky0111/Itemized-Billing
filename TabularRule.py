import pandas as pd

from Header import Header
from Body import Body


class TabularRule:
    first = None  # Header condition
    body = None
    header = None
    row_list = []
    data = pd.DataFrame()

    def __init__(self, data, first):
        self.header = Header()
        self.body = Body()
        self.data = data
        self.first = first
        self.row_list = []

    def runner(self):
        # self.headerRules() if self.first is True else self.contentRules()
        self.tableRules()

    def tableRules(self):
        content = ''

        for index, (x1, text) in enumerate(zip(self.data['left'], self.data['text'])):
            previous_row = self.data.iloc[index - 1]
            x2 = previous_row['left']
            w2 = previous_row['width']
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
        self.header.runner(self.data)

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
