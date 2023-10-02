from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QHeaderView
import sys
import mysql.connector
from mysql.connector import Error
from data.SqlHelper import create_db_connection, close_db_connection
from common import common


class ThemNhanVien(QtWidgets.QDialog):
    def __init__(self):
        self.db_connection = create_db_connection()
        super(ThemNhanVien, self).__init__()
        uic.loadUi('ui/ThemNhanVien.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.btn_Save.clicked.connect(self.on_click_save_button)
        self.btn_Huy.clicked.connect(self.on_click_cancel_button)

        if self.db_connection:
            mycursor = self.db_connection.cursor()
            res = mycursor.callproc("TaoMaNV", [0, ])
            self.txt_MaNV.setPlainText(str(res[0]))
            self.txt_MaNV.setDisabled(True)
            close_db_connection(mycursor)
            self.db_connection.close()

        self.show()

    def on_click_save_button(self):
        try:
            self.db_connection = create_db_connection()

            ma_nv = self.txt_MaNV.toPlainText().rstrip()
            ten_nhan_vien = self.txt_Ten.toPlainText().rstrip()
            dia_chi = self.txt_DiaChi.toPlainText().rstrip()
            sdt = self.txt_Sdt.toPlainText().rstrip()
            cap_bac = self.txt_CapBac.toPlainText().rstrip()
            if self.db_connection:
                mycursor = self.db_connection.cursor()
                mycursor.callproc(
                    "ThemNhanVien", [ma_nv, ten_nhan_vien, dia_chi, cap_bac, sdt, ])
                self.db_connection.commit()
                close_db_connection(mycursor)
                self.db_connection.close()

            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Thông báo")
            msg.setText("Thêm thành công")
            msg.exec_()
        except Error as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi")
            msg.setText(e.msg)
            msg.exec_()

        self.close()

    def on_click_cancel_button(self):
        self.close()


class SuaNhanVien(QtWidgets.QDialog):
    def __init__(self):
        super(SuaNhanVien, self).__init__()
        uic.loadUi('ui/SuaNhanVien.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.btn_Save.clicked.connect(self.on_click_save_button)
        self.btn_Xoa.clicked.connect(self.on_click_delete_button)
        self.btn_Huy.clicked.connect(self.on_click_cancel_button)

        self.openDialog = None

        self.show()

    def on_click_save_button(self):
        try:
            self.db_connection = create_db_connection()

            ma_nv = self.txt_MaNV.toPlainText().rstrip()
            ten_nhan_vien = self.txt_Ten.toPlainText().rstrip()
            dia_chi = self.txt_DiaChi.toPlainText().rstrip()
            sdt = self.txt_Sdt.toPlainText().rstrip()
            cap_bac = self.txt_CapBac.toPlainText().rstrip()

            if self.db_connection:
                mycursor = self.db_connection.cursor()
                mycursor.callproc(
                    "SuaNhanVien", [ma_nv, ten_nhan_vien, dia_chi, cap_bac, sdt, ])
                self.db_connection.commit()
                close_db_connection(mycursor)
                self.db_connection.close()

            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Thông báo")
            msg.setText("Sửa thành công")
            msg.exec_()
        except Error as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi")
            msg.setText(e.msg)
            msg.exec_()

        self.close()
        self.openDialog.on_click_search_button()

    def on_click_delete_button(self):
        try:
            self.db_connection = create_db_connection()

            ma_nv = self.txt_MaNV.toPlainText().rstrip()

            if self.db_connection:
                mycursor = self.db_connection.cursor()
                mycursor.callproc("XoaNhanVien", [ma_nv, ])
                self.db_connection.commit()
                close_db_connection(mycursor)
                self.db_connection.close()

            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Thông báo")
            msg.setText("Xoá thành công")
            msg.exec_()
        except Error as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi")
            msg.setText(e.msg)
            msg.exec_()

        self.close()
        self.openDialog.on_click_search_button()

    def on_click_cancel_button(self):
        self.close()


class TimKiemNhanVien(QtWidgets.QDialog):
    def __init__(self):
        super(TimKiemNhanVien, self).__init__()
        uic.loadUi('ui/TimKiemNhanVien.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.btn_Search.clicked.connect(self.on_click_search_button)
        self.tb_Result.clicked.connect(self.on_click_table)

        self.show()

    def on_click_search_button(self):
        try:
            self.db_connection = create_db_connection()

            ma_nv = self.txt_MaNV.toPlainText().rstrip()
            ten_nhan_vien = self.txt_TenNV.toPlainText().rstrip()
            dia_chi = self.txt_DiaChi.toPlainText().rstrip()
            sdt = self.txt_Sdt.toPlainText().rstrip()
            cap_bac = self.txt_CapBac.toPlainText().rstrip()

            if self.db_connection:
                mycursor = self.db_connection.cursor()
                mycursor.callproc("TimKiemNhanVien", [
                                  ma_nv, ten_nhan_vien, dia_chi, cap_bac, sdt, ])
                myresult = mycursor.stored_results()
                self.tb_Result.setRowCount(0)

                for m in myresult:
                    for x in m.fetchall():
                        rowPosition = self.tb_Result.rowCount()
                        self.tb_Result.insertRow(rowPosition)

                        self.tb_Result.setItem(
                            rowPosition, 0, QtWidgets.QTableWidgetItem(str(x[0])))
                        self.tb_Result.setItem(
                            rowPosition, 1, QtWidgets.QTableWidgetItem(str(x[1])))
                        self.tb_Result.setItem(
                            rowPosition, 2, QtWidgets.QTableWidgetItem(str(x[2])))
                        self.tb_Result.setItem(
                            rowPosition, 3, QtWidgets.QTableWidgetItem(str(x[5])))
                        self.tb_Result.setItem(
                            rowPosition, 4, QtWidgets.QTableWidgetItem(str(x[3])))

                        self.tb_Result.item(rowPosition, 0).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 1).setTextAlignment(
                            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 2).setTextAlignment(
                            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 3).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 4).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

                close_db_connection(mycursor)
                self.db_connection.close()

            common.autosizeColumns(self.tb_Result)
            self.tb_Result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except Error as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi")
            msg.setText(e.msg)
            msg.exec_()

    def on_click_table(self, item):
        dialog = SuaNhanVien()
        dialog.openDialog = self

        dialog.txt_MaNV.setPlainText(
            self.tb_Result.item(item.row(), 0).text())
        dialog.txt_Ten.setPlainText(
            self.tb_Result.item(item.row(), 1).text())
        dialog.txt_DiaChi.setPlainText(
            self.tb_Result.item(item.row(), 2).text())
        dialog.txt_Sdt.setPlainText(
            self.tb_Result.item(item.row(), 3).text())
        dialog.txt_CapBac.setPlainText(
            self.tb_Result.item(item.row(), 4).text())

        dialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TimKiemNhanVien()
    app.exec_()
