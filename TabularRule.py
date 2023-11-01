import pandas as pd


class TabularRule:
    data = pd.DataFrame()

    def __init__(self, data):
        self.data = data

    def runner(self):
        content = ''
        row_list = []

        print(self.data)

        for index, (x1, text) in enumerate(zip(self.data['left'], self.data['text'])):
            previous_row = self.data.iloc[index - 1]
            x2 = previous_row['left']
            w2 = previous_row['width']
            distance = x1 - (x2 + w2)

            if TabularRule.rule1(self.data):
                print('rule 1')
                row_list = [text]
            elif TabularRule.rule2(index):
                print('rule 2')
                content = text
            elif TabularRule.rule3(distance):
                print('rule 3')
                content += ' ' + text
            elif TabularRule.rule4(distance, index, self.data):
                print('rule 4')
                row_list.append(content)
            elif TabularRule.rule5(distance, index, self.data):
                print('rule 5')
                row_list.append(content)
                content = text
                row_list.append(content)
            elif TabularRule.rule6(distance):
                print('rule 6')
                row_list.append(content)
                content = text

            print(f'content: {content}')
        return row_list

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
    Rule 3: If the distance is lower than 40.
    @param dist
    @return True if rule is applied, False otherwise.
    '''
    @staticmethod
    def rule3(dist):
        return dist < 40

    '''
    Rule 4: If the distance is lower than 40 and last element of the row.
    @param counter
    @param data
    @return True if rule is applied, False otherwise.
    '''
    @staticmethod
    def rule4(dist, counter, data):
        return dist < 40 and counter == len(data) - 1

    '''
    Rule 5: If the distance is higher or equal to 40 and last element of the row.
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
