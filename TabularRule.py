from Bill import Bill


class TabularRule:
    id = None
    head = None  # Header condition
    data = []
    row_list = []
    col_range = []
    final_list = []

    def __init__(self, data, first):
        self.data = data
        self.head = first
        self.row_list = []
        self.final_list = [None] * 4

    def runner(self):
        self.id = 'Head' if self.head else 'Body'
        self.tableRules()
        self.headerRules() if self.head else self.contentRules()

    def tableRules(self):
        xx1 = None
        xx2 = None
        rule4 = False
        content = ''

        # for index, (x1, text) in enumerate(zip(self.data['left'], self.data['text'])):
        for index, row in enumerate(self.data):
            rule6 = False
            x1 = row.x
            w1 = row.width
            text = row.text
            previous_row = self.data[index - 1]
            x2 = previous_row.x
            w2 = previous_row.width
            distance = x1 - (x2 + w2)

            if TabularRule.rule1(self.data):
                # print('Comply Rule 1')
                # self.row_list = [text]
                xx1 = x1
                xx2 = x1 + w1

                grouped_bill = Bill(x=xx1, width=xx2-xx1, text=text, identity=self.id)
                # print(f'x={xx1}, width={xx2 - xx1}, text={text}, identity={self.id}')
                self.row_list = [grouped_bill]

            elif TabularRule.rule2(index):
                # print('Comply Rule 2')
                content = text
                xx1 = x1
            elif TabularRule.rule3(distance, index, self.data):
                # print('Comply Rule 3')
                # self.row_list.append(content)
                xx1 = xx1 if xx1 else x2
                xx2 = x1 + w1

                grouped_bill = Bill(x=xx1, width=xx2-xx1, text=content, identity=self.id)
                # print(f'x={xx1}, width={xx2 - xx1}, text={content}, identity={self.id}')

                self.row_list.append(grouped_bill)

            elif TabularRule.rule4(distance):
                # print('Comply Rule 4')
                content += ' ' + text
                xx1 = x2 if not rule4 else xx1
                rule4 = True

            elif TabularRule.rule5(distance, index, self.data):
                # print('Comply Rule 5')
                xx1 = x2
                xx2 = x2 + w2
                # self.row_list.append(content)

                grouped_bill = Bill(x=xx1, width=xx2-xx1, text=content, identity=self.id)
                # print(f'x={xx1}, width={xx2 - xx1}, text={content}, identity={self.id}')

                self.row_list.append(grouped_bill)

                content = text
                # self.row_list.append(content)
                xx1 = x1
                xx2 = x1 + w1

                grouped_bill = Bill(x=xx1, width=xx2-xx1, text=content, identity=self.id)
                # print(f'x={xx1}, width={xx2 - xx1}, text={content}, identity={self.id}')

                self.row_list.append(grouped_bill)

            elif TabularRule.rule6(distance):
                # print('Comply Rule 6')
                rule4 = False
                rule6 = True
                # self.row_list.append(content)
                xx1 = x2 if not xx1 else xx1
                xx2 = x2 + w2

                grouped_bill = Bill(x=xx1, width=xx2-xx1, text=content, identity=self.id)
                # print(f'x={xx1}, width={xx2 - xx1}, text={content}, identity={self.id}')

                self.row_list.append(grouped_bill)

                content = text

            # print(xx1, xx2, content)
            # print('=========================================================')

            xx1 = 0 if rule6 else xx1
            xx2 = 0 if rule6 else xx2

    def headerRules(self):
        midpoint = 0
        self.col_range.clear()

        if self.row_list is None:
            return

        for index, ele in enumerate(self.row_list):
            x1 = ele.x
            w1 = ele.width
            x2 = self.row_list[index + 1].x if not index == len(self.row_list) - 1 else 0

            # print(f'Before      x1:{x1}, w1: {w1}, x2: {x2}, text: {ele.text}')

            if index == 0:  # First element of the list
                continue
            elif index == 1:
                midpoint = (x2 - (x1 + w1)) / 2
                ele.x = x1 - midpoint
                xw1 = ((x1 + w1) + midpoint)
                ele.width = xw1 - ele.x
                self.row_list[index - 1].width = ele.x
            elif index == len(self.row_list) - 1:  # Last element of the list
                ele.x = x1 - midpoint
            else:
                ele.x = x1 - midpoint
                midpoint = (x2 - (x1 + w1)) / 2
                xw1 = (x1 + w1) + midpoint
                ele.width = xw1 - ele.x

            # print(f'After       x1:{ele.x}, w1: {ele.width}, x2: {x2}, text: {ele.text}')
            # print()

        self.col_range.extend((ele.x, ele.x + ele.width) for ele in self.row_list)

    def contentRules(self):
        for val in self.row_list:
            for i, coordinate in enumerate(self.col_range):
                x1, x2 = coordinate
                if x1 < val.x < x2 and x1 < val.x + val.width < x2:
                    self.final_list[i] = val.text

        # self.final_list = [val.text if x1 < val.x < x2 and x1 < val.x + val.width < x2 else old_val for
        #                    old_val, (x1, x2) in zip(self.final_list, self.col_range) for val in self.row_list]

        print(self.final_list)



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
