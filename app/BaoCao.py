from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QHeaderView
from mysql.connector import Error
from data.SqlHelper import create_db_connection, close_db_connection
from common import common

class LietKeTinDung(QtWidgets.QDialog):
    def __init__(self):
        self.db_connection = create_db_connection()     
        super(LietKeTinDung, self).__init__()
        uic.loadUi('ui/LietKeTinDung.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))
        
        # Tạo QDateEdit và đặt ngày mặc định
        self.dateEdit.setDateRange(QtCore.QDate(1900, 1, 1), QtCore.QDate(2100, 12, 31))  # Đặt khoảng ngày cho QDateEdit
        self.dateEdit.setDate(QtCore.QDate.currentDate())  # Đặt ngày mặc định là ngày hiện tại
        self.dateEdit.setCalendarPopup(True)
        # Định dạng ngày hiển thị thành dd/MM/yyyy
        self.dateEdit.setDisplayFormat("dd/MM/yyyy")
        
        self.dateEdit_2.setDateRange(QtCore.QDate(1900, 1, 1), QtCore.QDate(2100, 12, 31))  # Đặt khoảng ngày cho QDateEdit
        self.dateEdit_2.setDate(QtCore.QDate.currentDate())  # Đặt ngày mặc định là ngày hiện tại
        self.dateEdit_2.setCalendarPopup(True)
        # Định dạng ngày hiển thị thành dd/MM/yyyy
        self.dateEdit_2.setDisplayFormat("dd/MM/yyyy")

        self.pushButton.clicked.connect(self.on_click_process_button)

        self.show()

    def on_click_process_button(self):
        try:
            start_date = self.dateEdit.date()
            start_date = start_date.toPyDate()

            end_date = self.dateEdit_2.date()
            end_date = end_date.toPyDate()

            if self.db_connection:
                mycursor = self.db_connection.cursor()

                mycursor.callproc("LietKeTinDung", [start_date.strftime(
                    "%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), ])

                myresult = mycursor.stored_results()

                self.tableWidget.setRowCount(0)

                for m in myresult:
                    for x in m.fetchall():
                        rowPosition = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(rowPosition)

                        self.tableWidget.setItem(
                            rowPosition, 0, QtWidgets.QTableWidgetItem(str(x[0])))
                        self.tableWidget.setItem(
                            rowPosition, 1, QtWidgets.QTableWidgetItem(str(x[1])))

                        self.tableWidget.item(rowPosition, 0).setTextAlignment(
                            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 1).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        
                close_db_connection(mycursor)
            
            common.autosizeColumns(self.tableWidget)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                
        except Error as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi")
            msg.setText(e.msg)
            msg.exec_()


class LietKeNoTinDung(QtWidgets.QDialog):
    def __init__(self):
        self.db_connection = create_db_connection()     
        super(LietKeNoTinDung, self).__init__()
        uic.loadUi('ui/LietKeNoTinDung.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        try:
            if self.db_connection:
                mycursor = self.db_connection.cursor()

                mycursor.callproc("LietKeNoTinDung", [])

                myresult = mycursor.stored_results()

                self.tableWidget.setRowCount(0)

                for m in myresult:
                    for x in m.fetchall():
                        rowPosition = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(rowPosition)

                        self.tableWidget.setItem(
                            rowPosition, 0, QtWidgets.QTableWidgetItem(str(x[0])))
                        self.tableWidget.setItem(
                            rowPosition, 1, QtWidgets.QTableWidgetItem(str(x[1])))

                        self.tableWidget.item(rowPosition, 0).setTextAlignment(
                            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 1).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                
                close_db_connection(mycursor)
            
            common.autosizeColumns(self.tableWidget)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except Error as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi")
            msg.setText(e.msg)
            msg.exec_()

        self.show()


class LietKeTongTienGui(QtWidgets.QDialog):
    def __init__(self):
        self.db_connection = create_db_connection()     
        super(LietKeTongTienGui, self).__init__()
        uic.loadUi('ui/LietKeTongTienGui.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        try:
            if self.db_connection:
                mycursor = self.db_connection.cursor()

                mycursor.callproc("LietKeTienGui", [])

                myresult = mycursor.stored_results()

                self.tableWidget.setRowCount(0)

                for m in myresult:
                    for x in m.fetchall():
                        if x[0] is None or x[0] == "":
                            continue

                        rowPosition = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(rowPosition)

                        self.tableWidget.setItem(
                            rowPosition, 0, QtWidgets.QTableWidgetItem(str(x[0])))
                        self.tableWidget.setItem(
                            rowPosition, 1, QtWidgets.QTableWidgetItem(str(x[1])))
                        self.tableWidget.setItem(
                            rowPosition, 2, QtWidgets.QTableWidgetItem(str(x[2])))
                        self.tableWidget.setItem(
                            rowPosition, 3, QtWidgets.QTableWidgetItem(str(x[3])))
                        self.tableWidget.setItem(
                            rowPosition, 4, QtWidgets.QTableWidgetItem(str(x[4])))

                        self.tableWidget.item(rowPosition, 0).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 1).setTextAlignment(
                            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 2).setTextAlignment(
                            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 3).setTextAlignment(
                            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 4).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

                    close_db_connection(mycursor)
                    
                common.autosizeColumns(self.tableWidget)
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except Error as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi")
            msg.setText(e.msg)
            msg.exec_()

        self.show()
