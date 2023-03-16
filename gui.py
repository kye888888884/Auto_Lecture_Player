import sys
import PyQt5
import threading
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from random import random

class MainWindow(QWidget):
    def __init__(self, selects:list):
        super().__init__()
        self.labels = ('자동재생', '과목명', 'URL')
        self.selects:list[int] = selects
        self.cboxes:list[QCheckBox] = []

        self.is_loaded = False
        self.table_rows = 10

        self.initUI()
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def initUI(self):
        self.title_lbl = QLabel('<h1>전남대학교 강의 자동 재생기</h1>', self)

        self.table = QTableWidget()
        self.table.move(20, 80)
        self.table.setRowCount(self.table_rows)
        self.table.setColumnCount(len(self.labels))
        self.table.setHorizontalHeaderLabels(self.labels)
        for r in range(self.table_rows):
            for c in range(len(self.labels)):
                self.table.setItem(r, c, QTableWidgetItem(''))
            _cb = QCheckBox()
            _cb.setDisabled(True)
            self.cboxes.append(_cb)
            self.table.setCellWidget(r, 0, self.cboxes[r])

        self.btn = QPushButton('시작하기!', self)
        self.btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn.move(20, 20)

        self.btn_play = QPushButton('자동재생 시작!', self)
        self.btn_play.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_play.move(80, 20)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_lbl)
        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.btn_play)
        self.layout.addWidget(self.table)

        # 윈도우 설정
        self.setLayout(self.layout)
        self.setWindowTitle('CNU Auto Lecture Player')
        self.resize(300, 608)
        self.show()

    def createClassTable(self, classes:list):
        for r in range(self.table_rows):
            self.cboxes[r].setDisabled(True)
        for r in range(len(classes)):
            self.table.setItem(r, 1, QTableWidgetItem(classes[r]['class_name']))
            self.table.setItem(r, 2, QTableWidgetItem(classes[r]['class_url']))
            self.cboxes[r].setDisabled(False)
        # self.table.show()
        self.is_loaded = True
    
    def getSelects(self):
        self.selects.clear()
        for idx, cbox in enumerate(self.cboxes):
            if not cbox.isEnabled():
                continue
            if cbox.isChecked():
                self.selects.append(idx)

    def setFunc(self, type: str, func: callable):
        match type:
            case 'btn_start':
                self.btn.clicked.connect(func)
            case 'btn_play':
                self.btn_play.clicked.connect(func)
    


def init() -> QApplication:
    app = QApplication(sys.argv)
    return app

def start(app: QApplication) -> None:
    sys.exit(app.exec_())