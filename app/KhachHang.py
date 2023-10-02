import sys

import mysql.connector
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QHeaderView
from mysql.connector import Error
from data.SqlHelper import close_db_connection, create_db_connection
from common import common


class ThemKhachHang(QtWidgets.QDialog):
    def __init__(self):
        self.db_connection = create_db_connection()
        super(ThemKhachHang, self).__init__()
        uic.loadUi('ui/ThemKhachHang.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.btn_Save.clicked.connect(self.on_click_save_button)
        self.btn_Huy.clicked.connect(self.on_click_cancel_button)
        self.cbx_TypeKH.currentTextChanged.connect(self.on_combobox_changed)

        if self.db_connection:
            mycursor = self.db_connection.cursor()
            res = mycursor.callproc("TaoMaKH", [0, ])
            self.txt_MaKH.setPlainText(str(res[0]))
            self.txt_MaKH.setDisabled(True)
            close_db_connection(mycursor)
            self.db_connection.close()

        self.show()

    def on_combobox_changed(self, value):
        if value == "Khách hàng cá nhân":
            self.txt_NgheNghiep.setDisabled(False)
            self.txt_ThuNhap.setDisabled(False)
            self.txt_NguoiDaiDien.setDisabled(True)
            self.txt_QuyMo.setDisabled(True)

            self.txt_NguoiDaiDien.clear()
            self.txt_QuyMo.clear()
        else:
            self.txt_NgheNghiep.setDisabled(True)
            self.txt_ThuNhap.setDisabled(True)
            self.txt_NguoiDaiDien.setDisabled(False)
            self.txt_QuyMo.setDisabled(False)

            self.txt_NgheNghiep.clear()
            self.txt_ThuNhap.clear()

    def on_click_save_button(self):
        try:
            self.db_connection = create_db_connection()

            ma_kh = self.txt_MaKH.toPlainText().rstrip()
            ten_khach_hang = self.txt_Ten.toPlainText().rstrip()
            dia_chi = self.txt_DiaChi.toPlainText().rstrip()
            sdt = self.txt_Sdt.toPlainText().rstrip()
            nghe_nghiep = self.txt_NgheNghiep.toPlainText().rstrip()
            thu_nhap = self.txt_ThuNhap.toPlainText().rstrip()
            dai_dien = self.txt_NguoiDaiDien.toPlainText().rstrip()
            quy_mo = self.txt_QuyMo.toPlainText().rstrip()

            if self.cbx_TypeKH.currentText() == "Khách hàng cá nhân":
                if self.db_connection:
                    mycursor = self.db_connection.cursor()

                    mycursor.callproc("ThemKhachHangCaNhan", [
                        ma_kh, ten_khach_hang, dia_chi, sdt, nghe_nghiep, thu_nhap, ])

                    self.db_connection.commit()
                    close_db_connection(mycursor)
                    self.db_connection.close()
            else:
                if self.db_connection:
                    mycursor = self.db_connection.cursor()

                    mycursor.callproc("ThemKhachHangToChucDoanhNghiep",
                                      [ma_kh, ten_khach_hang, dia_chi, sdt, dai_dien, quy_mo, ])

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


class SuaKhachHang(QtWidgets.QDialog):
    def __init__(self):
        super(SuaKhachHang, self).__init__()
        uic.loadUi('ui/SuaKhachHang.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.btn_Luu.clicked.connect(self.on_click_save_button)
        self.btn_Xoa.clicked.connect(self.on_click_delete_button)
        self.btn_Huy.clicked.connect(self.on_click_cancel_button)

        self.openDialog = None

        self.show()

    def on_click_save_button(self):
        try:
            self.db_connection = create_db_connection()

            ma_kh = self.txt_MaKH.toPlainText().rstrip()
            ten_khach_hang = self.txt_TenKH.toPlainText().rstrip()
            dia_chi = self.txt_DiaChi.toPlainText().rstrip()
            sdt = self.txt_Sdt.toPlainText().rstrip()
            nghe_nghiep = self.txt_NgheNghiep.toPlainText().rstrip()
            thu_nhap = self.txt_ThuNhap.toPlainText().rstrip()
            dai_dien = self.txt_NguoiDaiDien.toPlainText().rstrip()
            quy_mo = self.txt_QuyMo.toPlainText().rstrip()

            if self.cbx_TypeKH.currentText() == "Khách hàng cá nhân":
                if self.db_connection:
                    mycursor = self.db_connection.cursor()

                    mycursor.callproc("SuaKhachHangCaNhan", [
                        ma_kh, ten_khach_hang, dia_chi, sdt, nghe_nghiep, thu_nhap, ])

                    self.db_connection.commit()
                    close_db_connection(mycursor)
                    self.db_connection.close()
            else:
                if self.db_connection:
                    mycursor = self.db_connection.cursor()

                    mycursor.callproc("SuaKhachHangToChucDoanhNghiep",
                                      [ma_kh, ten_khach_hang, dia_chi, sdt, dai_dien, quy_mo, ])

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

            ma_kh = self.txt_MaKH.toPlainText().rstrip()
            if self.db_connection:
                mycursor = self.db_connection.cursor()

                if self.cbx_TypeKH.currentText() == "Khách hàng cá nhân":
                    mycursor.callproc("XoaKhachHangCaNhan", [ma_kh, ])
                else:
                    mycursor.callproc(
                        "XoaKhachHangToChucDoanhNghiep", [ma_kh, ])

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


class TimKiemKhachHang(QtWidgets.QDialog):
    def __init__(self):
        super(TimKiemKhachHang, self).__init__()
        uic.loadUi('ui/TimKiemKhachHang.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.btn_Search.clicked.connect(self.on_click_search_button)
        self.tb_Result.clicked.connect(self.on_click_table)
        self.cbx_TypeKH.currentTextChanged.connect(self.on_combobox_changed)

        self.show()

    def on_combobox_changed(self, value):
        if value == "Khách hàng cá nhân":
            self.tb_Result.setHorizontalHeaderLabels(
                ["Mã khách hàng", "Tên", "Địa chỉ", "Số điện thoại", "Nghề nghiệp", "Thu nhập"])
        else:
            self.tb_Result.setHorizontalHeaderLabels(
                ["Mã khách hàng", "Tên", "Địa chỉ", "Số điện thoại", "Người đại diện", "Quy mô"])

        self.on_click_search_button()

    def on_click_search_button(self):
        try:
            self.db_connection = create_db_connection()

            ma_kh = self.txt_MaKH.toPlainText().rstrip()
            ten = self.txt_TenKH.toPlainText().rstrip()
            sdt = self.txt_Sdt.toPlainText().rstrip()

            if self.db_connection:
                mycursor = self.db_connection.cursor()

                if self.cbx_TypeKH.currentText() == "Khách hàng cá nhân":
                    mycursor.callproc("TimKiemKhachHangCaNhan",
                                      [ma_kh, ten, sdt, ])
                else:
                    mycursor.callproc("TimKiemKhachHangToChucDoanhNghiep", [
                        ma_kh, ten, sdt, ])

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
                            rowPosition, 3, QtWidgets.QTableWidgetItem(str(x[4])))
                        self.tb_Result.setItem(
                            rowPosition, 4, QtWidgets.QTableWidgetItem(str(x[6])))
                        self.tb_Result.setItem(
                            rowPosition, 5, QtWidgets.QTableWidgetItem(str(x[7])))

                        self.tb_Result.item(rowPosition, 0).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 1).setTextAlignment(
                            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 2).setTextAlignment(
                            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 3).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 4).setTextAlignment(
                            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 5).setTextAlignment(
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
        dialog = SuaKhachHang()
        dialog.openDialog = self

        dialog.cbx_TypeKH.setCurrentText(self.cbx_TypeKH.currentText())

        if dialog.cbx_TypeKH.currentText() == "Khách hàng cá nhân":
            dialog.txt_MaKH.setPlainText(
                self.tb_Result.item(item.row(), 0).text())
            dialog.txt_TenKH.setPlainText(
                self.tb_Result.item(item.row(), 1).text())
            dialog.txt_DiaChi.setPlainText(
                self.tb_Result.item(item.row(), 2).text())
            dialog.txt_Sdt.setPlainText(
                self.tb_Result.item(item.row(), 3).text())
            dialog.txt_NgheNghiep.setPlainText(
                self.tb_Result.item(item.row(), 4).text())
            dialog.txt_ThuNhap.setPlainText(
                self.tb_Result.item(item.row(), 5).text())

            # Điều chỉnh lại view
            dialog.txt_NgheNghiep.setDisabled(False)
            dialog.txt_ThuNhap.setDisabled(False)
            dialog.txt_NguoiDaiDien.setDisabled(True)
            dialog.txt_QuyMo.setDisabled(True)
            dialog.txt_NguoiDaiDien.clear()
            dialog.txt_QuyMo.clear()
        else:
            dialog.txt_MaKH.setPlainText(
                self.tb_Result.item(item.row(), 0).text())
            dialog.txt_TenKH.setPlainText(
                self.tb_Result.item(item.row(), 1).text())
            dialog.txt_DiaChi.setPlainText(
                self.tb_Result.item(item.row(), 2).text())
            dialog.txt_Sdt.setPlainText(
                self.tb_Result.item(item.row(), 3).text())
            dialog.txt_NguoiDaiDien.setPlainText(
                self.tb_Result.item(item.row(), 4).text())
            dialog.txt_QuyMo.setPlainText(
                self.tb_Result.item(item.row(), 5).text())

            # Điều chỉnh lại view
            dialog.txt_NgheNghiep.setDisabled(True)
            dialog.txt_ThuNhap.setDisabled(True)
            dialog.txt_NguoiDaiDien.setDisabled(False)
            dialog.txt_QuyMo.setDisabled(False)
            dialog.txt_NgheNghiep.clear()
            dialog.txt_ThuNhap.clear()

        dialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ThemKhachHang()
    app.exec_()
