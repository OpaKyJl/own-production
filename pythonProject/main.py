# -*- coding: utf-8 -*-
import datetime
import sys
import time
from collections import defaultdict
from math import ceil

from PyQt5 import Qt, QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from vcr_gui_v015 import Ui_MainWindow
import server as srv

# from Graphics import plot_graphics, data_read # тут логика графиков
# from MplForWidget import MyMplCanvas
# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar


# file_path = 'salesmonthly.csv'

import warnings
warnings.filterwarnings("ignore")
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self)
        self.reload()

    def reload(self):
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("img\moon.png"))
        # self.showMaximized()

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

    def closeEvent(self, event):
        # закрытие соединения с БД
        srv.close_connection(connection)
        srv.check_connection(connection)

    def add_functions(self):
        self.calendarWidget_5.clicked.connect(self.date_select)
        self.calendarWidget_6.clicked.connect(self.date_select)
        self.calendarWidget.clicked.connect(self.date_select)
        self.calendarWidget_2.clicked.connect(self.date_select)

        self.pushButton_8.clicked.connect(lambda: self.add_combox(self.verticalLayout_6, db_products_accounting))
        self.pushButton_8.clicked.connect(self.add_spinbox)
        # добавляем запись в таблицу справа
        self.pushButton_10.clicked.connect(lambda: self.add_tablerow(self.tableWidget, db_recipe_cost, self.stackedWidget.currentIndex()))

        self.pushButton_9.clicked.connect(lambda: self.add_combox(self.verticalLayout_19, db_sales_accounting))

        self.pushButton_5.clicked.connect(lambda: self.add_tablerow(self.tableWidget_2, db_recipe, self.stackedWidget.currentIndex()))

        self.comboBox_2.currentIndexChanged.connect(lambda: self.load_info("3-2"))

        self.pushButton_6.clicked.connect(lambda: self.insert_data_to_table(db_products_accounting))
        self.pushButton_7.clicked.connect(lambda: self.insert_data_to_table(db_sales_accounting))

    def add_spinbox(self):
        self.spinBox = QtWidgets.QSpinBox()

        self.spinBox.setMinimumSize(QtCore.QSize(300, 0))
        self.spinBox.setMaximumSize(QtCore.QSize(300, 16777215))
        self.spinBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                     "color: rgb(43, 89, 250);")
        self.spinBox.setMaximum(999999)

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)

        self.spinBox.setFont(font)
        self.spinBox.setObjectName(f'{self.verticalLayout_11.objectName()}_{len(self.verticalLayout_11)}')
        self.verticalLayout_11.addWidget(self.spinBox)


    def add_combox(self, layout, db_name):
        self.comboBox = QtWidgets.QComboBox()

        combox = self.comboBox

        combox.setMinimumSize(QtCore.QSize(300, 0))
        combox.setMaximumSize(QtCore.QSize(300, 16777215))
        combox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "color: rgb(43, 89, 250);")

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)

        combox.setFont(font)

        self.fill_combox(db_name, combox)
        # устанавливаем имя добавляемого комбобокса как  "имя лэйаута" + "порядковый номер(начиная с 0)"
        combox.setObjectName(f'{layout.objectName()}_{len(layout)}')
        layout.addWidget(combox)


    def add_checkbox(self, text):
        # print("click")

        layout = self.verticalLayout_43
        self.checkBox = QtWidgets.QCheckBox()
        checkbox = self.checkBox

        checkbox.setMinimumSize(QtCore.QSize(300, 0))
        checkbox.setMaximumSize(QtCore.QSize(300, 16777215))
        checkbox.setStyleSheet("background-color: rgb(255, 233, 190);\n"
                                      "color: rgb(43, 89, 250);")

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)

        checkbox.setFont(font)

        checkbox.setObjectName(f'{layout.objectName()}_{len(layout)}')
        checkbox.setText(text)
        layout.addWidget(checkbox)


    def date_select(self):
        self.textEdit_4.setText(self.calendarWidget_5.selectedDate().toString('dd-MM-yyyy'))
        self.textEdit_5.setText(self.calendarWidget_6.selectedDate().toString('dd-MM-yyyy'))

        self.textEdit_2.setText(self.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
        self.textEdit_3.setText(self.calendarWidget_2.selectedDate().toString('dd-MM-yyyy'))

    def btn_navigation(self):
        self.pBtn_production_acc.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        self.pBtn_production_sales_acc.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pBtn_production_sales_acc.clicked.connect(lambda: self.load_info(self.stackedWidget.currentIndex()))

        self.pBtn_an_sales.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.pBtn_an_sales.clicked.connect(lambda: self.load_info(self.stackedWidget.currentIndex()))

        self.pBtn_recipe.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))

        self.pBtn_products.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.pBtn_products.clicked.connect(lambda: self.load_info(self.stackedWidget.currentIndex()))

        self.pBtn_an_sales_product.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(2))
        # загрузка комбобокса
        self.pBtn_an_sales_product.clicked.connect(lambda: self.fill_combox(db_products_accounting, self.comboBox_2))
        self.pBtn_an_sales_product.clicked.connect(lambda: (self.load_info(f'{self.stackedWidget.currentIndex()}-{self.stackedWidget_2.currentIndex()}')))
        self.pBtn_an_sales_production.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(1))
        self.pBtn_an_sales_production.clicked.connect(lambda: (self.load_info(f'{self.stackedWidget.currentIndex()}-{self.stackedWidget_2.currentIndex()}')))

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
    def load_info(self, current_page):
        match current_page:
            case 1:
                print("1")

            case 2:
                print("Учёт продаж собственной продукции")
                self.add_combox(self.verticalLayout_6, db_products_accounting)
                self.add_spinbox()
                self.add_tablerow(self.tableWidget, db_recipe_cost, self.stackedWidget.currentIndex())

            case 3:
                print("Анализ продаж")

            case "3-1":
                print("Анализ продаж продукции")
                self.add_combox(self.verticalLayout_19, db_sales_accounting)
                production_acc = srv.select_from_table(connection, db_products_accounting)
                production_acc_list = defaultdict(list)

                for row in production_acc:
                    production_acc_list[row[1]].append([row[2], row[3],float(row[4]), float(row[5])])

                products_from_table = srv.select_from_table(connection, db_products)
                product_list = defaultdict(list)

                for row in products_from_table:
                    product_list[row[0]].append([row[1], float(row[2])])

            case "3-2":
                print("Анализ продаж продуктов")
                self.clear_layout(self.verticalLayout_43)

                production_acc = srv.select_from_table(connection, db_products_accounting)
                production_acc_list = defaultdict(list)
                product_id_list = defaultdict(list)

                for row in production_acc:
                    production_acc_list[row[1]].append([row[2], row[3], float(row[4]), float(row[5])])
                    product_id_list[row[1]].append(row[2])

                products_from_table = srv.select_from_table(connection, db_products)
                product_list = defaultdict(list)

                for row in products_from_table:
                    product_list[row[0]].append([row[1], float(row[2])])

                recipe = srv.select_from_table(connection, db_recipe_cost)
                recipe_list = defaultdict(list)

                for row in recipe:
                    recipe_list[row[0]].append(row[1])

                for id in product_id_list:
                    product_id_list[id] = set(product_id_list[id])

                for index in product_id_list: # 1 2
                    for id in product_id_list[index]:
                        # print(id)
                        if self.comboBox_2.currentText() == recipe_list[index][0]:
                            self.add_checkbox(product_list[id][0][0])
                # print(production_acc_list)
                # print(product_list)
                # print(product_id_list)
                # print(recipe_list)

            case 4:
                print("4")

            case 5:
                print("Учёт продуктов на изготовление собственной продукции")
                self.fill_combox(db_recipe, self.comboBox_3)
                self.add_tablerow(self.tableWidget_2, db_recipe, self.stackedWidget.currentIndex())

    def insert_data_to_table(self, db_name):
        match db_name:
            case "products_accounting":
                print("тут insert to "+ db_name)
                insert_data = defaultdict(list)
                rows = self.tableWidget_2.rowCount()

                #id продукции
                # insert_data[0] = 0
                select_data_from_table = srv.select_from_table(connection, db_recipe_cost)
                for row in select_data_from_table:
                    if row[1] == self.comboBox_3.currentText():
                        insert_data[0].append(row[0])

                #id продукта
                select_data_from_table = srv.select_from_table(connection, db_products)

                for row_table in range(rows):
                    for row in select_data_from_table:
                        if row[1] == self.tableWidget_2.item(row_table, 0).text():
                            insert_data[1].append(row[0])

                #дата
                insert_data[2] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                #использовано продукта
                for row in range(rows):
                    insert_data[3].append(float(self.tableWidget_2.item(row, 1).text()))

                #цена использованного продукта
                for row_table in range(rows):
                    for row in select_data_from_table:
                        if row[1] == self.tableWidget_2.item(row_table, 0).text():
                            insert_data[4].append((float(self.tableWidget_2.item(row_table, 1).text()) * float(row[2])) / 100)

                # проверяем, что запишется в БД
                # for row in range(len(insert_data[1])):
                #      print(f'{insert_data[0][0]}, {insert_data[1][row]}, {insert_data[2]}, {insert_data[3][row]}, {insert_data[4][row]}')

                # записываем в БД
                srv.insert_into_table(connection, db_name, insert_data)

            case "sales_accounting":
                print("тут insert to " + db_name)


    def add_tablerow(self, table, db_name, page):
        match page:
            case 2:
                recipe = srv.select_from_table(connection, db_name)
                recipe_cost_list = defaultdict(list)

                for row in recipe:
                    recipe_cost_list[row[1]].append(float(row[2]))

                table.clearContents()
                table.setRowCount(len(self.verticalLayout_6))
                rows = len(self.verticalLayout_6)

                #########################################################################
                # РАБОТАЕТ !!!!!!!!!!!!!!!!!!!!!!!!!!
                # print(self.verticalLayout_6.itemAt(0).widget().currentText())
                #########################################################################
                sum = 0

                for row in range(rows):
                    name_production = self.verticalLayout_6.itemAt(row).widget().currentText()
                    gram = self.verticalLayout_11.itemAt(row).widget().value()
                    table.setItem(row, 0, QTableWidgetItem(name_production))
                    table.setItem(row, 1, QTableWidgetItem(str(gram)))
                    if name_production in recipe_cost_list:
                        cost = recipe_cost_list[name_production]
                        table.setItem(row, 2, QTableWidgetItem(str(gram * cost[0])))
                        sum = sum + (gram * cost[0])

                self.label_14.setText("СУММА: " + str(sum))
            case 5:
                recipe = srv.select_from_table(connection, db_name)
                recipe_list = defaultdict(list)

                for row in recipe:
                    recipe_list[row[1]].append([row[2], float(row[3])])

                table.clearContents()

                ####################################################################################
                # получаем всю информацию из таблицы рецепты
                select_data_from_table = srv.select_from_table(connection, db_recipe_cost)
                select_production = defaultdict(list)

                # составляем отдельный список id
                for row in select_data_from_table:
                    select_production[row[0]].append(row[1])

                name = self.comboBox_3.currentText()
                product = srv.select_from_table(connection, db_products)
                product_list = defaultdict(list)

                for row in product:
                    product_list[row[0]].append([row[1], float(row[2])])

                text_of_recipe = "Тут рецепт на 100 грамм продукции"

                # 100 грамм - одна порция
                for id in recipe_list.keys():
                    if name == select_production[id][0]:
                        text_of_recipe = f'{text_of_recipe}\n ------<{name}>------'
                        table.setRowCount(len(recipe_list[id]))
                        for row in range(len(recipe_list[id])):
                            product_name = str(product_list[recipe_list[id][row][0]][0][0])
                            table.setItem(row, 0, QTableWidgetItem(product_name))
                            text_of_recipe = f'{text_of_recipe} \n {product_name} - '
                            gram_of_product = recipe_list[id][row][1]
                            value = (gram_of_product * self.spinBox_3.value()) / 100
                            text_of_recipe = f'{text_of_recipe}{ceil(recipe_list[id][row][1])} гр.\n'
                            table.setItem(row, 1, QTableWidgetItem(str(ceil(value))) )
                self.textEdit.setText(text_of_recipe)

    def fill_combox(self, db_name, combox):
        # получаем всю информацию из таблицы
        select_data_from_table = srv.select_from_table(connection, db_name)
        select_production = []

        # составляем отдельный список id
        for row in select_data_from_table:
            select_production.append(row[1])

        # удаляем лишние id
        select_production_id = set(select_production)

        # превратим индексы продукции в наименование
        select_data_from_table = srv.select_from_table(connection, db_recipe_cost)
        select_production_name = []

        # ищем имена по индексам
        for id in select_production_id:
            for row in select_data_from_table:
                if id == row[0]:
                    select_production_name.append(row[1])

        for name in select_production_name:
            combox.addItem(str(name))

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)

        combox.setFont(font)

    def btn_back(self):
        self.pBtn_back_to_main_9.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_9.clicked.connect(lambda: self.reload())

        self.pBtn_back_to_main_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        # сдесь установление стандартных параметров страницы
        self.pBtn_back_to_main_2.clicked.connect(lambda: self.reload())

        self.pBtn_back_to_main_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_3.clicked.connect(lambda: self.reload())

        self.pBtn_back_to_main_4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_4.clicked.connect(lambda: self.reload())

        self.pBtn_back_to_main_5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_5.clicked.connect(lambda: self.reload())

        #################################################################################################
        # тут нужно вернуться на выбор анализа

        self.pBtn_back_to_main_6.clicked.connect(lambda: self.reload())
        self.pBtn_back_to_main_6.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))

        self.pBtn_back_to_main_7.clicked.connect(lambda: self.reload())
        self.pBtn_back_to_main_7.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))

        #################################################################################################


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

db_products = "products"
db_products_accounting = "products_accounting"
db_recipe = "recipe"
db_recipe_cost = "recipe_cost"
db_sales_accounting = "sales_accounting"

connection = None
connection = srv.set_connection(connection)
connection.autocommit = True
srv.check_connection(connection)

main()

