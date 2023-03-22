import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

class Msg:
    START = "'시작하기'를 눌러주세요."
    OPENING = "브라우저를 여는 중입니다..."
    LOGIN = "로그인 해주세요."
    LOGIN_FAILED = "로그인에 실패했습니다. 다시 로그인 해주세요."
    LOADING = "강의 목록을 불러오는 중입니다..."
    SELECT = "자동재생을 원하는 강의를 선택하고, '자동재생 시작'을 눌러주세요\n강의가 보이지 않으면 표의 아무 부분을 클릭해주세요."
    PLAY = "자동재생 중입니다... 브라우저를 조작하지 말아주세요."
    BROWSER_ERROR = "브라우저가 비정상적으로 종료되었습니다. 다시 실행하려면'시작하기'를 눌러주세요."
    COMPLETE = "재생이 완료되었습니다. 다시 실행하려면 '시작하기'를 눌러주세요."

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

        self.btn_start = QPushButton('시작하기', self)
        self.btn_start.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_start.move(20, 20)

        self.btn_play = QPushButton('자동재생 시작', self)
        self.btn_play.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_play.move(80, 20)
        self.btn_play.setEnabled(False)

        self.lo = QHBoxLayout()
        self.lo.addWidget(self.btn_start)
        self.lo.addWidget(self.btn_play)

        self.status_lbl = QLabel(self)
        self.status_lbl.setWordWrap(True)
        self.setStatus(Msg.START)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_lbl)
        self.layout.addLayout(self.lo)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.status_lbl)

        # 윈도우 설정
        self.setLayout(self.layout)
        self.setWindowTitle('CNU Auto Lecture Player')
        self.resize(300, 600)
        self.show()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, int((self.table.width()-80-2)))
        return super().resizeEvent(a0)

    def createClassTable(self) -> None:
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
        self.table.update()
    
    def clearClassTable(self) -> None:
        for cb in self.cboxes:
            cb.setDisabled(True)
        for r in range(self.table_rows):
            self.table.setItem(r, 1, QTableWidgetItem(''))

    def updateClassTable(self, classes:list) -> None:
        self.clearClassTable()
        for r in range(self.lecture_num):
            self.cboxes[r].setDisabled(True)
        for r in range(len(classes)):
            self.table.setItem(r + 1, 1, QTableWidgetItem(classes[r]['class_name']))
            self.cboxes[r].setDisabled(False)
        # self.table.show()
        self.is_loaded = True
        self.setButtonEnable(btn2=True)

    def centerWidget(self, content) -> QWidget:
        cellWidget = QWidget()
        layoutCB = QHBoxLayout(cellWidget)
        layoutCB.addWidget(content)
        layoutCB.setAlignment(Qt.AlignmentFlag.AlignCenter)            
        layoutCB.setContentsMargins(0,0,0,0)
        cellWidget.setLayout(layoutCB)
        return cellWidget

    def cbAllClicked(self, checked) -> None:
        for cb in self.cboxes:
            if not cb.isEnabled():
                continue
            cb.setChecked(checked)

    def setStatus(self, msg:str) -> None:
        self.status_lbl.setText('<h4>'+msg+'</h4>')
    
    def getSelects(self) -> None:
        self.selects.clear()
        for idx, cbox in enumerate(self.cboxes):
            if not cbox.isEnabled():
                continue
            if cbox.isChecked():
                self.selects.append(idx)

    def setButtonEnable(self, btn1:int|bool=-1, btn2:int|bool=-1) -> None:
        if btn1 != -1:
            self.btn_start.setEnabled(btn1)
        if btn2 != -1:
            self.btn_play.setEnabled(btn2)
        # print(btn1, btn2)

    def setFunc(self, type: str, func: callable) -> None:
        match type:
            case 'btn_start':
                self.btn_start.clicked.connect(func)
            case 'btn_play':
                self.btn_play.clicked.connect(func)

def init() -> QApplication:
    app = QApplication(sys.argv)
    return app

def start(app: QApplication) -> None:
    app.exec_()