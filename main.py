import sys

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QSizePolicy, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import GiaoDich
import KhachHang
import NhanVien
import TaiKhoan
import TruyVan


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        uic.loadUi('UI/MainMenu.ui', self)
        # self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('assets/icon/icon.png'))

        self.action_add_staff.setIcon(QtGui.QIcon('assets/icon/staff.png'))
        self.action_search_staff.setIcon(
            QtGui.QIcon('assets/icon/searchstaff.png'))
        self.action_payroll.setIcon(QtGui.QIcon('assets/icon/salary.png'))
        self.action_add_customer.setIcon(
            QtGui.QIcon('assets/icon/customer.png'))
        self.action_search_customer.setIcon(
            QtGui.QIcon('assets/icon/searchcutomer.png'))
        self.action_create_account.setIcon(
            QtGui.QIcon('assets/icon/addaccount.png'))
        self.action_create_transaction.setIcon(
            QtGui.QIcon('assets/icon/transaction.png'))
        self.action_search_transaction.setIcon(
            QtGui.QIcon('assets/icon/searchtransaction.png'))
        self.action_report_ntd.setIcon(QtGui.QIcon('assets/icon/report.png'))
        self.action_report_total.setIcon(QtGui.QIcon('assets/icon/result.png'))
        self.action_report_td.setIcon(QtGui.QIcon('assets/icon/report2.png'))

        self.action_add_staff.triggered.connect(self.open_add_staff)
        self.action_search_staff.triggered.connect(self.open_search_staff)
        self.action_payroll.triggered.connect(self.open_payroll)
        self.action_add_customer.triggered.connect(self.open_add_customer)
        self.action_search_customer.triggered.connect(
            self.open_search_customer)
        self.action_create_account.triggered.connect(self.open_create_account)
        self.action_create_transaction.triggered.connect(
            self.open_create_transaction)
        self.action_search_transaction.triggered.connect(
            self.open_search_transaction)
        self.action_report_ntd.triggered.connect(self.open_report_ntd)
        self.action_report_td.triggered.connect(self.open_report_td)
        self.action_report_total.triggered.connect(self.open_report_total)

        self.QS_Body.setWidgetResizable(True)

        # Tạo một QWidget để chứa QLabel
        container = QWidget()
        self.QS_Body.setWidget(container)

        # Tạo một QVBoxLayout cho QWidget
        layout = QVBoxLayout(container)

        # Tạo một QLabel để hiển thị hình ảnh
        label = QLabel(self)

        # Đặt hình ảnh cho QLabel và làm nó lấp đầy QLabel
        pixmap = QPixmap('assets/icon/hinhnen.jpg')
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        # Làm cho hình ảnh tự điều chỉnh để lấp đầy QLabel
        label.setScaledContents(True)

        # Thêm QLabel vào QVBoxLayout
        layout.addWidget(label)

        # Đặt QVBoxLayout làm nội dung cho container
        container.setLayout(layout)

        # Đặt container làm nội dung cho QScrollArea
        self.QS_Body.setWidget(container)

        self.QS_Body.showFullScreen()

        self.show()

    def show_child(self, child_window, title):
        self.QS_Body = QScrollArea(self)
        self.QS_Body.setWidgetResizable(True)

        # Thêm container vào QScrollArea
        self.QS_Body.setWidget(child_window)

        self.setCentralWidget(self.QS_Body)

        self.QS_Body.setWindowTitle(title)
        self.QS_Body.showFullScreen()

    def open_add_staff(self):
        child_window = NhanVien.ThemNhanVien()
        title = "Nhân viên"
        self.show_child(child_window, title)

    def open_search_staff(self):
        child_window = NhanVien.TimKiemNhanVien()
        title = "Tìm kiếm nhân viên"
        self.show_child(child_window, title)

    def open_payroll(self):
        child_window = TruyVan.TinhLuong()
        title = "Tính lương nhân viên"
        self.show_child(child_window, title)

    def open_add_customer(self):
        child_window = KhachHang.ThemKhachHang()
        title = "Thêm khách hàng"
        self.show_child(child_window, title)

    def open_search_customer(self):
        child_window = KhachHang.TimKiemKhachHang()
        title = "Tìm kiếm khách hàng"
        self.show_child(child_window, title)

    def open_create_account(self):
        child_window = TaiKhoan.ThemTaiKhoan()
        title = "Tạo tài khoản"
        self.show_child(child_window, title)

    def open_create_transaction(self):
        child_window = GiaoDich.ThemGiaoDich()
        title = "Thêm giao dịch"
        self.show_child(child_window, title)

    def open_search_transaction(self):
        child_window = GiaoDich.TimKiemGiaoDich()
        title = "Thêm giao dịch"
        self.show_child(child_window, title)

    def open_report_ntd(self):
        child_window = TruyVan.LietKeNoTinDung()
        title = "Nợ tín dụng"
        self.show_child(child_window, title)

    def open_report_td(self):
        child_window = TruyVan.LietKeTinDung()
        title = "Tín dụng"
        self.show_child(child_window, title)

    def open_report_total(self):
        child_window = TruyVan.LietKeTongTienGui()
        title = "Tổng tiền gửi"
        self.show_child(child_window, title)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
