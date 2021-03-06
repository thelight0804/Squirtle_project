# cmd에서 pip3 install PyQt5 명령어를 이용하여 PyQt5를 설치해야 한다
#박스 레이아웃 사용 (https://wikidocs.net/21945 참조)

# from operator import truediv
# import sys
import Timer, Main
from GUI import ConfigGUI #ConfigGUI import

from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *

class TimerGUI(QWidget): #클래스
    def __init__(self): #생성자
        self.Hour = 00
        self.Min = 00
        self.Sec = 00

        super().__init__()
        self.setWindowTitle('Squirtle') #프로그램 이름
        self.setWindowIcon(QIcon('Resource\Squirtle.ico')) #프로그램 아이콘
        font = QFont('나눔고딕', 15) #폰트 설정
        self.setFont(font)
        self.resize(540, 360) #창 사이즈
        self.init_UI()

    def init_UI(self):
        ##버튼 구현
        #환경설정 버튼
        ConfigBtn = QPushButton('', self) #ConfigBtn 버튼 구현
        ConfigBtn.setIcon(QtGui.QIcon('Resource\config.png')) #아이콘 구현 (상대경로)
        ConfigBtn.setIconSize(QtCore.QSize(50,50)) #아이콘 크기
        ConfigBtn.setFlat(True) #버튼 테두리 없애기
        ConfigBtn.clicked.connect(self.ConfigBtnClicked) #버튼 클릭 했을 때 ConfigBtn_clicked 함수 호출

        #Reset 버튼
        ResetBtn = QPushButton('', self)
        ResetBtn.setIcon(QtGui.QIcon(r'Resource\reset.png')) #\r은 옵션이라 \\r를 사용하였다
        ResetBtn.setIconSize(QtCore.QSize(50,50))
        ResetBtn.setFlat(True)
        ResetBtn.clicked.connect(self.ResetBtnCliked)

        #Start 버튼
        self.StartBtn = QPushButton('', self)
        self.StartBtn.setIcon(QtGui.QIcon('Resource\start.png'))
        self.StartBtn.setIconSize(QtCore.QSize(50,50))
        self.StartBtn.setFlat(True)
        self.StartBtn.clicked.connect(self.StartBtnCliked)

        ##QLable 구현
        self.LMarkLabel = QLabel(':', self) #왼쪽 ':'
        self.LMarkLabel.setAlignment(Qt.AlignCenter)
        self.RMarkLabel = QLabel(':', self) #오른쪽 ':'
        self.RMarkLabel.setAlignment(Qt.AlignCenter)
        self.HLabel = QLabel(str(int(Main.data.Sec/3600)).zfill(2), self) #시간
        self.HLabel.setAlignment(Qt.AlignCenter)
        self.MLabel = QLabel(str(int(Main.data.Sec/60%60)).zfill(2), self) #분
        self.MLabel.setAlignment(Qt.AlignCenter)
        self.SLabel = QLabel(str(Main.data.Sec%60).zfill(2), self) #초
        self.SLabel.setAlignment(Qt.AlignCenter)

        ##QLabel 폰트
        TimerFont = self.HLabel.font()
        TimerFont.setPointSize(50)
        TimerFont.setBold(True)

        self.HLabel.setFont(TimerFont)
        self.MLabel.setFont(TimerFont)
        self.SLabel.setFont(TimerFont)
        self.LMarkLabel.setFont(TimerFont)
        self.RMarkLabel.setFont(TimerFont)

        ##Box 레이아웃
        #수평
        hboxUp = QHBoxLayout() #수평 box 생성
        hboxUp.addWidget(ConfigBtn) #ConfigBtn 버튼 생성
        hboxUp.addStretch(1) #비율이 1인 빈 공간 생성
        
        hboxMid = QHBoxLayout() #시간 설정 레이아웃
        hboxMid.addStretch(1)
        hboxMid.addWidget(self.HLabel)
        hboxMid.addWidget(self.LMarkLabel)
        hboxMid.addWidget(self.MLabel)
        hboxMid.addWidget(self.RMarkLabel)
        hboxMid.addWidget(self.SLabel)
        hboxMid.addStretch(1)

        hboxDown = QHBoxLayout() #초기화, 타이머변경, 시작 레이아웃
        hboxDown.addStretch(10)
        hboxDown.addWidget(ResetBtn)
        hboxDown.addStretch(1)
        hboxDown.addStretch(1)
        hboxDown.addWidget(self.StartBtn)
        hboxDown.addStretch(10)
        
        #수직
        vbox = QVBoxLayout() #수직 box 생성
        vbox.addLayout(hboxUp)
        vbox.addStretch(10)
        vbox.addLayout(hboxMid)
        vbox.addStretch(10)        
        vbox.addLayout(hboxDown)
        vbox.setContentsMargins(0, 0, 0, 50)

        self.setLayout(vbox) #수직 box를 메인 레이아웃으로 설정

        ##창 출력
        self.center() #창을 화면 중앙으로
        self.show() #창 출력

    def ConfigBtnClicked(self): #Config 버튼 클릭
        ConfigUI = ConfigGUI.ConfigGUI()
        ConfigUI.exec_() #ConfigUI가 끝나기 전 까지 루프

    def StartBtnCliked(self): #Start 버튼 클릭
        if Timer.PauseTimer == False: #정지 상태일 때
            Timer.PauseTimer = True
            Timer.StartTimer() #Timer.StartTimer 호출
            self.StartBtn.setIcon(QtGui.QIcon('Resource\pause.png'))
        else: #진행중 일 때
            Timer.PauseTimer = False
            self.StartBtn.setIcon(QtGui.QIcon('Resource\start.png'))

    def ResetBtnCliked(self): #초기화 버튼
        Timer.ResetTimer()
        
    def timerEvent(self, e): #타이머 이벤트
        if self.step >= 100:
            self.timer.stop()
            return

        self.step = self.step + 1
        
    def center(self): #창의 화면을 중앙으로
        qr = self.frameGeometry() #창의 위치와 크기 정보를 가져온다
        cp = QDesktopWidget().availableGeometry().center() #현재 모니터의 위치를 파악한다
        qr.moveCenter(cp) #창을 cp로 이동한다
        self.move(qr.topLeft())