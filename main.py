# This is a sample Python script.

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QAction, QFileDialog, QMessageBox

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
        self.textLabel = QLabel("Please use File->Open to select the downloaded csv file from ING \n"
                                "The program relies on category_mappings.csv to be in the same folder with the program")
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
        mappings = ing_csv_parsing.read_category_mappings("category_mappings.csv")
        entries = ing_csv_parsing.parse_csv(file_path)
        income, expenses, not_mapped = ing_csv_parsing.process_entries(entries, mappings)
        if not_mapped:
            self.show_unmapped_entries(not_mapped)


        # income = dict(filter(lambda elem: elem[1] > 0.0, result.items()))
        # expenses = dict(filter(lambda elem: elem[1] < 0.0, result.items()))
        self.widget = QWidget()
        self.widget.setMinimumSize(800, 600)
        layout = donut_chart.Widget(income, expenses)
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)
        self.widget.show()

    def show_unmapped_entries(self, entries):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        text = "We found some entries with no categy, they will go to Other expenses\n"
        msg.setText(text)

        msg.setInformativeText("Please edit the category_mappings.csv to assign a category")
        msg.setWindowTitle("Unmapped entries")
        detailed_text = ""

        for entry in entries:
            detailed_text = detailed_text + entry + "\n"
        msg.setDetailedText(detailed_text)
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
