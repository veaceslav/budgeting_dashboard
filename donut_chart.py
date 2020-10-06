import functools
import random

from PyQt5.QtChart import *
from table_utils import *


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




class Widget(QWidget):

    def __init__(self, income, expenses):
        super().__init__()

        self.update_data(income,expenses)

    def update_data(self, income, expenses):
        self.income_chartView = DisplayPie(income, "Income")
        self.expenses_chartView = DisplayPie(expenses, "Expenses")

        data = [
            list(income.keys()),
            list(income.values())
        ]

        self.income_table = DisplayTable(income)
        self.expenses_table = DisplayTable(expenses)

        self.layout = QGridLayout()
        self.layout.addWidget(self.income_chartView, 0, 0)
        self.layout.addWidget(self.expenses_chartView, 0, 1)
        self.layout.addWidget(self.income_table, 1,0)
        self.layout.addWidget(self.expenses_table, 1,1)
        self.setLayout(self.layout)
        #self.income_chartView.show()
        #self.expenses_chartView.show()

