# This is a sample Python script.

from PyQt5.QtWidgets import QApplication

import sys
import ing_csv_parsing
import donut_chart


if __name__ == '__main__':
    entries = ing_csv_parsing.parse_csv("NL42INGB0660362848_01-01-2020_31-01-2020.csv")
    result = ing_csv_parsing.process_entries(entries)
    app = QApplication(sys.argv)
    income = dict(filter(lambda elem: elem[1] > 0.0, result.items()))
    expenses = dict(filter(lambda elem: elem[1] < 0.0, result.items()))
    widget = donut_chart.Widget(income, expenses)
    widget.show()

    app.exec_()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
