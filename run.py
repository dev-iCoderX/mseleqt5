from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QMainWindow,QWidget, QGridLayout, QApplication, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QFrame, QMessageBox
from PyQt5 import uic
import win32gui
import win32con
import winxpgui
import win32api
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import ctypes
user32 = ctypes.windll.user32
width,height = 400, 600


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        uic.loadUi("./Pyqt5/loadUi.ui", self)
        self.centralwidget = self.findChild(QWidget, "widgetShow")


        self.verticalLayout = QGridLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        
        self.chrome_options = Options()
        self.chrome_options.add_argument("disable-infobars")
        self.chrome_options.add_argument("--window-size=400,600")
        self.chrome_options.add_argument("--kiosk")
        self.chrome_options.add_argument("--window-position=-10,-10")
        #self.chrome_options.add_argument("--app=https://www.youtube.com/"); 
        self.s=Service(ChromeDriverManager().install())
        
        self.driver = webdriver.Chrome(service=self.s,options=self.chrome_options,service_log_path='NUL')
        self.driver.set_window_size(600, 600)
        
        #self.driver.get("https://www.youtube.com/")
        self.driver.execute_script('document.title = "My New Title"')

        self.driver2 = webdriver.Chrome(service=self.s,options=self.chrome_options,service_log_path='NUL')
        self.driver2.set_window_size(600, 600)
        
        #self.driver2.get("https://www.youtube.com/")
        self.driver2.execute_script('document.title = "My New Title"')
        time.sleep(0.5)

        

        self.hwnd = []
        self.tries = 30
        self.total_tries = 0
        while(len(self.hwnd)==0 and self.total_tries<=self.tries):
            try:
                win32gui.EnumWindows(self.hwnd_method, None)
                #win32gui.SetWindowLong (self.hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong (self.hwnd, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED )
                #winxpgui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(0,0,0), 255, win32con.LWA_ALPHA)
                count = 0
                for id in self.hwnd:
                    self.embed_window = QtGui.QWindow.fromWinId(id)
                    self.embed_widget = QtWidgets.QWidget.createWindowContainer(self.embed_window)
                    self.embed_widget.setFixedHeight(800)
                    self.verticalLayout.addWidget(self.embed_widget, int(count/2), count%2)  
                    count += 1
                    #self.verticalLayout.titleSubWindows()      
                #self.driver.execute_script("document.documentElement.requestFullscreen();")
                self.tries+= 1
                break
                time.sleep(1)
            except Exception as e:
                print(e)
                self.tries += 1
        self.show()
        
            
    def hwnd_method(self, hwnd, ctx):
        window_title = win32gui.GetWindowText(hwnd)
        #print(window_title)
        if self.driver.title in window_title:
            self.hwnd.append(hwnd)
            '''        
            old_style = win32gui.GetWindowLong(hwnd, -16)
            # building the new style(old style AND NOT Maximize AND NOT Minimize)
            new_style = old_style & ~win32con.WS_MAXIMIZEBOX & ~win32con.WS_MINIMIZEBOX
            # setting new style
            win32gui.SetWindowLong(hwnd, -16, new_style)
            # updating non - client area
            win32gui.SetWindowPos(hwnd, 0, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
            win32gui.UpdateWindow(hwnd)
            '''
            #win32gui.ShowWindow(hwnd , win32con.SW_HIDE)
            
            #win32gui.SetWindowLong (hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong (hwnd, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED )
            #winxpgui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0,0,0), 0, win32con.LWA_ALPHA)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))



import sys
app = QApplication(sys.argv)
uix = Ui_MainWindow()
sys.exit(app.exec_())