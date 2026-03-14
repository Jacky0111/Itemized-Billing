from Bill import Bill
from TabularRule import TabularRule


def test_tabular_rule_groups_two_far_apart_items():
    data = [
        Bill(x=0, y=0, width=10, height=10, text="A"),
        Bill(x=50, y=0, width=10, height=10, text="B"),
    ]

    tr = TabularRule(data, first=True)
    tr.runner()

    assert [b.text for b in tr.row_list] == ["A", "B"]


def test_tabular_rule_single_item_row():
    data = [Bill(x=5, y=0, width=8, height=10, text="ONLY")]

    tr = TabularRule(data, first=True)
    tr.runner()

    assert [b.text for b in tr.row_list] == ["ONLY"]


def test_tabular_rule_groups_close_items_then_new_cell():
    data = [
        Bill(x=0, y=0, width=10, height=10, text="A"),
        Bill(x=15, y=0, width=10, height=10, text="B"),
        Bill(x=60, y=0, width=10, height=10, text="C"),
    ]

    tr = TabularRule(data, first=True)
    tr.runner()

    assert [b.text for b in tr.row_list] == ["A B", "C"]


def test_tabular_rule_header_rules_with_two_columns():
    data = [
        Bill(x=10, y=0, width=10, height=10, text="ITEM"),
        Bill(x=60, y=0, width=10, height=10, text="PRICE"),
    ]

    tr = TabularRule(data, first=True)
    tr.runner()

    assert len(tr.col_range) == 2
    assert tr.col_range[0][0] <= tr.col_range[0][1]
    assert tr.col_range[1][0] <= tr.col_range[1][1]
