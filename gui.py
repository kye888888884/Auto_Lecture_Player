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
        self.labels = ('재생여부', '과목명')
        self.selects:list[int] = selects
        self.cboxes:list[QCheckBox] = []

        self.is_loaded = False
        self.table_rows = 11
        self.lecture_num = self.table_rows - 1

        self.initUI()
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def initUI(self):
        self.title_lbl = QLabel('<h1>전남대학교 강의 자동 재생기</h1>', self)
        self.title_lbl.setMaximumHeight(self.title_lbl.height())

        self.createClassTable()

        self.btn = QPushButton('시작하기', self)
        self.btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn.move(20, 20)

        self.btn_play = QPushButton('자동재생 시작', self)
        self.btn_play.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_play.move(80, 20)

        self.lo = QHBoxLayout()
        self.lo.addWidget(self.btn)
        self.lo.addWidget(self.btn_play)

        self.status_lbl = QLabel("<h4>'시작하기'를 눌러주세요.</h4>", self)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_lbl)
        self.layout.addLayout(self.lo)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.status_lbl)

        # 윈도우 설정
        self.setLayout(self.layout)
        self.setWindowTitle('CNU Auto Lecture Player')
        self.resize(300, 580)
        self.show()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, int((self.table.width()-80-2)))
        return super().resizeEvent(a0)

    def createClassTable(self):
        self.table = QTableWidget()
        self.table.move(20, 80)
        self.table.setRowCount(self.table_rows)
        self.table.setColumnCount(len(self.labels))
        self.table.setHorizontalHeaderLabels(self.labels)
        for r in range(self.lecture_num):
            self.table.setItem(r + 1, 0, QTableWidgetItem(str(r + 1)))

            _cb = QCheckBox()
            _cb.setDisabled(True)
            self.cboxes.append(_cb)

            self.table.setCellWidget(r + 1, 0, self.centerWidget(self.cboxes[r]))
        
        self.cb_all = QCheckBox()
        self.cb_all.clicked.connect(self.cbAllClicked)
        self.table.setCellWidget(0, 0, self.centerWidget(self.cb_all))

        self.table.verticalHeader().setVisible(False)
        self.table.setMaximumHeight(439)
    
    def centerWidget(self, content) -> QWidget:
        cellWidget = QWidget()
        layoutCB = QHBoxLayout(cellWidget)
        layoutCB.addWidget(content)
        layoutCB.setAlignment(Qt.AlignmentFlag.AlignCenter)            
        layoutCB.setContentsMargins(0,0,0,0)
        cellWidget.setLayout(layoutCB)
        return cellWidget

    def cbAllClicked(self, checked):
        for cb in self.cboxes:
            cb.setChecked(checked)

    def updateClassTable(self, classes:list):
        for r in range(self.lecture_num):
            self.cboxes[r].setDisabled(True)
        for r in range(len(classes)):
            self.table.setItem(r + 1, 1, QTableWidgetItem(classes[r]['class_name']))
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
    app.exec_()