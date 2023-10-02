from PyQt5 import QtWidgets, uic, QtGui, QtCore
from mysql.connector import Error
from data.SqlHelper import close_db_connection, create_db_connection

class ThemTaiKhoan(QtWidgets.QDialog):
    def __init__(self):   
        self.db_connection = create_db_connection()     
        super(ThemTaiKhoan, self).__init__()
        uic.loadUi('ui/ThemTaiKhoan.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.btn_Save.clicked.connect(self.on_click_save_button)
        self.btn_Huy.clicked.connect(self.on_click_cancel_button)
        self.cbx_TypeKH.currentTextChanged.connect(self.on_combobox_changed)
        self.cbx_TypeTK.currentTextChanged.connect(self.on_combobox_changed2)

        if self.db_connection:
            mycursor = self.db_connection.cursor()

            res = mycursor.callproc("TaoMaTK", [0, ])
            self.txt_MaTK.setPlainText(str(res[0]))
            self.txt_MaTK.setDisabled(True)
            close_db_connection(mycursor)  

        self.txt_HanMuc.setDisabled(False)
        self.txt_SoNo.setDisabled(False)
        self.txt_LaiSuat.setDisabled(True)
        self.txt_SoDu.setDisabled(True)

        self.txt_LaiSuat.clear()
        self.txt_SoDu.clear()

        self.show()

    def on_combobox_changed(self, value):
        if value == "Khách hàng cá nhân":
            self.cbx_TypeTK.clear()
            self.cbx_TypeTK.addItem("Tài khoản tín dụng")
            self.cbx_TypeTK.addItem("Tài khoản gửi tiền")

            self.cbx_TypeTK.setCurrentText("Tài khoản tín dụng")
        else:
            self.cbx_TypeTK.clear()
            self.cbx_TypeTK.addItem("Tài khoản gửi tiền")
            self.cbx_TypeTK.addItem("Tài khoản vay tiền")

            self.cbx_TypeTK.setCurrentText("Tài khoản gửi tiền")

        self.txt_HanMuc.clear()
        self.txt_LaiSuat.clear()
        self.txt_SoDu.clear()
        self.txt_SoNo.clear()

    def on_combobox_changed2(self, value):
        if value == "Tài khoản tín dụng":
            self.txt_HanMuc.setDisabled(False)
            self.txt_SoNo.setDisabled(False)
            self.txt_LaiSuat.setDisabled(True)
            self.txt_SoDu.setDisabled(True)

            self.txt_LaiSuat.clear()
            self.txt_SoDu.clear()

        if value == "Tài khoản gửi tiền":
            self.txt_LaiSuat.setDisabled(False)
            self.txt_SoDu.setDisabled(False)
            self.txt_HanMuc.setDisabled(True)
            self.txt_SoNo.setDisabled(True)

            self.txt_HanMuc.clear()
            self.txt_SoNo.clear()

        if value == "Tài khoản vay tiền":
            self.txt_LaiSuat.setDisabled(False)
            self.txt_SoNo.setDisabled(False)
            self.txt_HanMuc.setDisabled(True)
            self.txt_SoDu.setDisabled(True)

            self.txt_HanMuc.clear()
            self.txt_SoDu.clear()

    def on_click_save_button(self):
        try:
            ma_tk = self.txt_MaTK.toPlainText().rstrip()
            hang_tk = self.txt_HangTK.toPlainText().rstrip()
            han_muc = self.txt_HanMuc.toPlainText().rstrip()
            lai_suat = self.txt_LaiSuat.toPlainText().rstrip()
            so_du = self.txt_SoDu.toPlainText().rstrip()
            so_no = self.txt_SoNo.toPlainText().rstrip()
            ma_kh = self.txt_MaKH.toPlainText().rstrip()
            ma_nv = self.txt_MaNV.toPlainText().rstrip()

            if self.cbx_TypeTK.currentText() == "Tài khoản tín dụng":
                if self.db_connection:
                    mycursor = self.db_connection.cursor()

                    mycursor.callproc("ThemTaiKhoanTinDung", [ma_kh, ma_nv, ma_tk, hang_tk, han_muc, so_no, ])

                    self.db_connection.commit()
                    close_db_connection(mycursor)

            if self.cbx_TypeTK.currentText() == "Tài khoản vay tiền":
                if self.db_connection:
                    mycursor = self.db_connection.cursor()

                    mycursor.callproc("ThemTaiKhoanVayTien", [ma_kh, ma_nv, ma_tk, hang_tk, lai_suat, so_no, ])

                    self.db_connection.commit()
                    close_db_connection(mycursor)

            if self.cbx_TypeTK.currentText() == "Tài khoản gửi tiền":
                if self.cbx_TypeKH.currentText() == "Khách hàng cá nhân":
                    if self.db_connection:
                        mycursor = self.db_connection.cursor()

                        mycursor.callproc("ThemTaiKhoanGuiTienCaNhan", [ma_kh, ma_nv, ma_tk, hang_tk, so_du, lai_suat, ])

                        self.db_connection.commit()
                        close_db_connection(mycursor)
                else:
                    if self.db_connection:
                        mycursor = self.db_connection.cursor()

                        mycursor.callproc("ThemTaiKhoanGuiTienToChucDoanhNghiep",
                                        [ma_kh, ma_nv, ma_tk, hang_tk, so_du, lai_suat, ])

                        self.db_connection.commit()
                        close_db_connection(mycursor)

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


class TimKiemTaiKhoan(QtWidgets.QDialog):
    def __init__(self):
        self.db_connection = create_db_connection()     
        super(TimKiemTaiKhoan, self).__init__()
        uic.loadUi('ui/TimKiemTaiKhoan.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.btn_Save.clicked.connect(self.on_click_search_button)
        self.tb_Result.clicked.connect(self.on_click_table)
        self.cbx_TypeKH.currentTextChanged.connect(self.on_combobox_changed)
        self.cbx_TypeTK.currentTextChanged.connect(self.on_combobox_changed2)

        self.show()

    def on_combobox_changed(self, value):
        if value == "Khách hàng cá nhân":
            self.cbx_TypeTK.clear()
            self.cbx_TypeTK.addItem("Tài khoản tín dụng")
            self.cbx_TypeTK.addItem("Tài khoản gửi tiền")

            self.cbx_TypeTK.setCurrentText("Tài khoản tín dụng")
        else:
            self.cbx_TypeTK.clear()
            self.cbx_TypeTK.addItem("Tài khoản gửi tiền")
            self.cbx_TypeTK.addItem("Tài khoản vay tiền")

            self.cbx_TypeTK.setCurrentText("Tài khoản gửi tiền")

        self.textEdit_3.clear()
        self.textEdit_4.clear()
        self.textEdit_5.clear()
        self.textEdit_6.clear()
        self.on_click_search_button()

    def on_combobox_changed2(self, value):
        if value == "Tài khoản tín dụng":
            self.textEdit_3.setDisabled(False)
            self.textEdit_6.setDisabled(False)
            self.textEdit_4.setDisabled(True)
            self.textEdit_5.setDisabled(True)

            self.textEdit_4.clear()
            self.textEdit_5.clear()

        if value == "Tài khoản gửi tiền":
            self.textEdit_4.setDisabled(True)
            self.textEdit_5.setDisabled(True)
            self.textEdit_3.setDisabled(False)
            self.textEdit_6.setDisabled(False)

            self.textEdit_3.clear()
            self.textEdit_6.clear()

        if value == "Tài khoản vay tiền":
            self.textEdit_4.setDisabled(True)
            self.textEdit_6.setDisabled(True)
            self.textEdit_3.setDisabled(False)
            self.textEdit_5.setDisabled(False)

            self.textEdit_3.clear()
            self.textEdit_5.clear()

        self.on_click_search_button()

