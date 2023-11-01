# -*- coding: utf-8 -*-
import sys
import time

from PyQt5 import Qt, QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QMainWindow, QApplication
from vcr_gui_v001 import Ui_MainWindow

# from Graphics import plot_graphics, data_read # тут логика графиков
# from MplForWidget import MyMplCanvas
# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar


# file_path = 'salesmonthly.csv'

import warnings
warnings.filterwarnings("ignore")
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("img\moon.png"))

        pBtn_style_sheet = "background-color: rgb(177, 255, 170);\n border-radius: 40px;\n color: rgb(43, 89, 250);\n border: 1px solid rgb(43, 89, 250);}\n QPushButton:hover{    \n background-color: #9CDF96;}"

        self.pBtn_production_acc.setStyleSheet(pBtn_style_sheet)
        self.pBtn_production_sales_acc.setStyleSheet(pBtn_style_sheet)
        self.pBtn_an_sales.setStyleSheet(pBtn_style_sheet)
        self.pBtn_recipe.setStyleSheet(pBtn_style_sheet)
        self.pBtn_products.setStyleSheet(pBtn_style_sheet)



        self.add_functions()

    def add_functions(self):
        self.pBtn_production_acc.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pBtn_production_sales_acc.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pBtn_an_sales.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.pBtn_recipe.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.pBtn_products.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))

        self.pBtn_back_to_main.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        # self.view_graphic.clicked.connect(lambda: self.plot())
        # self.view_graphic.clicked.connect(self.prepare_canvas_and_toolbar)
        # self.comboBox_2.currentIndexChanged.connect(self.prepare_canvas_and_toolbar)

def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


main()

