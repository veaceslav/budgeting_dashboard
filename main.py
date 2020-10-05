# This is a sample Python script.

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QAction, QFileDialog

from PyQt5.QtGui import QIcon
import sys
import ing_csv_parsing
import donut_chart
from pathlib import Path


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.textLabel = QLabel("Please use File->Open to select the downloaded csv file from ING")
        self.setCentralWidget(self.textLabel)
        self.statusBar()

        openFile = QAction(QIcon(), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 550, 450)
        self.setWindowTitle('Budget Overview')
        self.show()

    def showDialog(self):

        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir, filter="*.csv")

        if fname[0]:
            self.process_csv(fname[0])

    def process_csv(self,file_path):
        entries = ing_csv_parsing.parse_csv(file_path)
        result = ing_csv_parsing.process_entries(entries)
        income = dict(filter(lambda elem: elem[1] > 0.0, result.items()))
        expenses = dict(filter(lambda elem: elem[1] < 0.0, result.items()))
        self.widget = QWidget()
        self.widget.setMinimumSize(800, 600)
        layout = donut_chart.Widget(income, expenses)
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)
        self.widget.show()

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
