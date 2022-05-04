#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年3月1日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: EmbedWindow
@description: 嵌入外部窗口
"""

__Author__ = 'By: Irony\nQQ: 892768447\nEmail: 892768447@qq.com'
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0

from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget,\
    QLabel
import win32con
import win32gui


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        layout = QVBoxLayout(self)

        self.myhwnd = int(self.winId())
        print(self.myhwnd)

        layout.addWidget(QPushButton('Show Tab', self,clicked=self._getWindowList, maximumHeight=30))
        layout.addWidget(
            QLabel('Double click to Embedd\nĐịnh dạng là: xử lý | xử lý mẹ | tiêu đề | tên lớp', self, maximumHeight=30))
        self.windowList = QListWidget(
            self, itemDoubleClicked=self.onItemDoubleClicked, maximumHeight=200)
        layout.addWidget(self.windowList)

    def closeEvent(self, event):
        """Cửa sổ đóng"""
        if self.layout().count() == 4:
            self.restore()
        super(Window, self).closeEvent(event)

    def _getWindowList(self):
        """Xóa danh sách ban đầu"""
        self.windowList.clear()
        win32gui.EnumWindows(self._enumWindows, None)

    def onItemDoubleClicked(self, item):
        """Nhấp đúp vào danh sách để chọn sự kiện"""
        # # đầu tiên hãy xóa mục này
        self.windowList.takeItem(self.windowList.indexFromItem(item).row())
        hwnd, phwnd, _, _ = item.text().split('|')
        # bắt đầu nhúng

        hwnd, phwnd = int(hwnd), int(phwnd)
        # Nhúng các thuộc tính trước đó
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        print('save', hwnd, style, exstyle)

        widget = QWidget.createWindowContainer(QWindow.fromWinId(hwnd))
        widget.setFixedHeight(800)
        widget.hwnd = hwnd  # id
        widget.phwnd = phwnd  # tay cầm cửa sổ cha
        widget.style = style  # kiểu cửa sổ
        widget.exstyle = exstyle  # cửa sổ thêm phong cách
        
        widget.setParent(self)
        layout = QVBoxLayout()
        layout.addWidget(widget)
        self.layout().addLayout(layout)
    def restore(self):
        """Cửa sổ trả lại"""
        # Có một lỗi, sau khi quay lại, cửa sổ không có kiểu WS_VISIBLE và ẩn
        widget = self.layout().itemAt(3).widget()
        print('restore', widget.hwnd, widget.style, widget.exstyle)
        # làm cho nó trở về cửa sổ mẹ của nó
        win32gui.SetParent(widget.hwnd, widget.phwnd)
        win32gui.SetWindowLong(
            widget.hwnd, win32con.GWL_STYLE, widget.style | win32con.WS_VISIBLE)  # khôi phục kiểu
        win32gui.SetWindowLong(
            widget.hwnd, win32con.GWL_EXSTYLE, widget.exstyle)  # khôi phục kiểu
        win32gui.ShowWindow(
            widget.hwnd, win32con.SW_SHOW)  # cửa sổ hiển thị
        widget.close()
        self.layout().removeWidget(widget)  # xóa khỏi bố cục
        widget.deleteLater()

    def _enumWindows(self, hwnd, _):
        """Hàm gọi lại theo chiều ngang"""
        if hwnd == self.myhwnd:
            return  # Ngăn bản thân nhúng tay vào
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            phwnd = win32gui.GetParent(hwnd)
            title = win32gui.GetWindowText(hwnd)
            name = win32gui.GetClassName(hwnd)
            self.windowList.addItem(
                '{0}|{1}|\tTiêu đề：{2}\t|\Lớp: {3}'.format(hwnd, phwnd, title, name))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
