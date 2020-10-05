
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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