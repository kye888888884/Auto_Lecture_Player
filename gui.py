import sys
import PyQt5
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from random import random

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.labels = ('과목명', 'URL')
        self.initUI()

    def initUI(self):
        self.title_lbl = QLabel('전남대학교 강의 자동 재생기', self)

        self.table = QTableWidget()
        self.table.move(20, 80)
        self.table.setRowCount(10)
        self.table.setColumnCount(len(self.labels))
        self.table.setHorizontalHeaderLabels(self.labels)
        for r in range(10):
            for c in range(len(self.labels)):
                self.table.setItem(r, c, QTableWidgetItem(''))

        self.btn = QPushButton('Font', self)
        self.btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn.move(20, 20)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.title_lbl)
        self.layout.addWidget(self.btn)

        # 윈도우 설정
        self.setLayout(self.layout)
        self.setWindowTitle('CNU Auto Lecture Player')
        self.resize(800, 608)
        self.show()

    def createClassTable(self, classes:list):
        # self.table = QTableWidget()
        # self.table.setRowCount(len(classes))
        # self.table.setColumnCount(len(self.labels))
        # self.table.setHorizontalHeaderLabels(self.labels)
        for r in range(len(classes)):
            self.table.setItem(r, 0, QTableWidgetItem(classes[r]['class_name']))
            self.table.setItem(r, 1, QTableWidgetItem(classes[r]['class_url']))
        # self.table.show()
    
    def set_func(self, type: str, func: callable):
        match type:
            case 'btn_start':
                self.btn.clicked.connect(func)

def init() -> QApplication:
    app = QApplication(sys.argv)
    return app

def start(app: QApplication) -> None:
    sys.exit(app.exec_())