# This is a sample Python script.

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QAction, QFileDialog, QMessageBox, QComboBox, QVBoxLayout

from PyQt5.QtGui import QIcon
import sys
import ing_csv_parsing
import donut_chart
from pathlib import Path


class MainWidget(QWidget):
    def __init__(self, filepath):
        super().__init__()
        self.file_path = filepath
        self.initUI()

    def initUI(self):
        self.setMinimumSize(800, 600)
        mappings = ing_csv_parsing.read_category_mappings("category_mappings.csv")
        entries = ing_csv_parsing.parse_csv(self.file_path)
        self.income, self.expenses, not_mapped = ing_csv_parsing.process_entries(entries, mappings)
        if not_mapped:
            self.show_unmapped_entries(not_mapped)

        all_entries = list(set(self.income.keys()))
        all_entries.sort()
        self.months_combo = QComboBox()

        for entry in all_entries:
            self.months_combo.addItem(entry)

        self.months_combo.currentIndexChanged.connect(self.update_month)

        main_layout = QVBoxLayout()

        self.data_layout = donut_chart.Widget(self.income[self.months_combo.currentText()],
                                              self.expenses[self.months_combo.currentText()])
        main_layout.addWidget(self.months_combo)
        main_layout.addWidget(self.data_layout)
        self.setLayout(main_layout)
        self.show()

    def clearLayout(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_month(self):
        self.layout().takeAt(1).widget().deleteLater()

        self.data_layout = donut_chart.Widget(self.income[self.months_combo.currentText()],
                                              self.expenses[self.months_combo.currentText()])
        self.layout().addWidget(self.data_layout)


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
        self.process_csv("/home/veaceslav/Downloads/NL42INGB0660362848_01-01-2020_01-10-2020.csv")
        self.show()

    def showDialog(self):

        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir, filter="*.csv")

        if fname[0]:
            self.process_csv(fname[0])

    def process_csv(self,file_path):
        self.widget = MainWidget(file_path)
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
