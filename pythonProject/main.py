# -*- coding: utf-8 -*-
import sys
import time

from PyQt5 import Qt, QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QMainWindow, QApplication
from vcr_gui_v010 import Ui_MainWindow

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
        self.pBtn_an_sales_product.setStyleSheet(pBtn_style_sheet)
        self.pBtn_an_sales_production.setStyleSheet(pBtn_style_sheet)

        self.add_functions()
        self.btn_navigation()
        self.btn_back()
        self.date_select()

    def add_functions(self):
        # self.view_graphic.clicked.connect(lambda: self.plot())
        # self.view_graphic.clicked.connect(self.prepare_canvas_and_toolbar)
        # self.comboBox_2.currentIndexChanged.connect(self.prepare_canvas_and_toolbar)

        self.calendarWidget_5.clicked.connect(self.date_select)
        self.calendarWidget_6.clicked.connect(self.date_select)
        self.calendarWidget.clicked.connect(self.date_select)
        self.calendarWidget_2.clicked.connect(self.date_select)

        # clicked.connect(
        #     lambda checked, button=button, i=i, j=j: self._on_clicked_cell(button, i, j)
        # )
        self.pushButton_8.clicked.connect(lambda : self.add_combox(self.verticalLayout_6))
        self.pushButton_8.clicked.connect(self.add_spinbox)
        self.pushButton_9.clicked.connect(lambda : self.add_combox(self.verticalLayout_19))


    def add_spinbox(self):
        self.spinBox = QtWidgets.QSpinBox()

        self.spinBox.setMinimumSize(QtCore.QSize(300, 0))
        self.spinBox.setMaximumSize(QtCore.QSize(300, 16777215))
        self.spinBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                     "color: rgb(43, 89, 250);")
        self.spinBox.setMaximum(999999)

        self.verticalLayout_11.addWidget(self.spinBox)


    def add_combox(self, layout):
        # print("click")
        self.comboBox = QtWidgets.QComboBox()

        self.comboBox.setMinimumSize(QtCore.QSize(300, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(300, 16777215))
        self.comboBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "color: rgb(43, 89, 250);")

        layout.addWidget(self.comboBox)
        # verticalScrollBar()->setValue(ui.textEdit->verticalScrollBar()->maximum());
        # не получается
        # self.scrollArea_2.verticalScrollBar().setValue(self.scrollArea_2.maximum())


    def date_select(self):
        self.textEdit_4.setText(self.calendarWidget_5.selectedDate().toString('dd-MM-yyyy'))
        self.textEdit_5.setText(self.calendarWidget_6.selectedDate().toString('dd-MM-yyyy'))

        self.textEdit_2.setText(self.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
        self.textEdit_3.setText(self.calendarWidget_2.selectedDate().toString('dd-MM-yyyy'))

    def btn_navigation(self):
        self.pBtn_production_acc.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pBtn_production_sales_acc.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pBtn_an_sales.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.pBtn_recipe.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.pBtn_products.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))

    def btn_back(self):
        self.pBtn_back_to_main_9.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        self.pBtn_an_sales_product.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(2))
        self.pBtn_an_sales_production.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(1))

        self.pBtn_back_to_main_6.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(0))
        self.pBtn_back_to_main_7.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(0))

def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


main()

