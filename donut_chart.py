import functools
import random

from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class DisplayPie(QChartView):

    def setup_chart(self, label, slices, chartView, donuts):
        chartView.setRenderHint(QPainter.Antialiasing)
        chart = chartView.chart()
        chart.legend().setVisible(False)
        chart.setTitle(label)
        chart.setAnimationOptions(QChart.AllAnimations)

        donut = QPieSeries()
        for label, value in slices.items():
            slice_ = QPieSlice(label, value)
            slice_.setLabelVisible(True)
            slice_.setLabelPosition(QPieSlice.LabelOutside)
            slice_.hovered[bool].connect(functools.partial(self.explodeSlice, slice_=slice_))
            donut.append(slice_)

        donuts.append(donut)
        chartView.chart().addSeries(donut)

    def __init__(self, data, label):
        super().__init__()
        self.m_donuts = []

        self.setup_chart(label, data, self, self.m_donuts)

    def explodeSlice(self, exploded, slice_):
        if exploded:
            sliceStartAngle = slice_.startAngle()
            sliceEndAngle = slice_.startAngle() + slice_.angleSpan()

            donut = slice_.series()
            seriesIndex = self.m_donuts.index(donut)
            for i in range(seriesIndex + 1, len(self.m_donuts)):
                self.m_donuts[i].setPieStartAngle(sliceEndAngle)
                self.m_donuts[i].setPieEndAngle(360 + sliceStartAngle)
        else:
            for donut in self.m_donuts:
                donut.setPieStartAngle(0)
                donut.setPieEndAngle(360)
        slice_.setExploded(exploded)


class DisplayTable(QTableView):
    def __init__(self, data):
        super().__init__()
        self._data = [
            list(data.keys()),
            list(data.values())
        ]
        self.tableModel = TableModel(self._data)
        self.setModel(self.tableModel)


class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Note: self._data[index.row()][index.column()] will also work
            value = self._data[index.column()][index.row()]
            return str(value)

    def rowCount(self, index):
        return len(self._data[0])

    def columnCount(self, index):
        return len(self._data)

class Widget(QWidget):

    def __init__(self, income, expenses):
        super().__init__()
        self.setMinimumSize(800, 600)


        self.income_chartView = DisplayPie(income, "Income")
        self.expenses_chartView = DisplayPie(expenses, "Expenses")

        data = [
            list(income.keys()),
            list(income.values())
        ]

        self.income_table = DisplayTable(income)
        self.expenses_table = DisplayTable(expenses)

        # create main layout
        self.mainLayout = QGridLayout(self)
        self.mainLayout.addWidget(self.income_chartView, 0, 0)
        self.mainLayout.addWidget(self.expenses_chartView, 0, 1)
        self.mainLayout.addWidget(self.income_table, 1,0)
        self.mainLayout.addWidget(self.expenses_table, 1,1)
        self.income_chartView.show()
        self.expenses_chartView.show()
        self.setLayout(self.mainLayout)

