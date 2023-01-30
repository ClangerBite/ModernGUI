################################################################################
##
## BY:      Sunil Patel
## MODULE:  Splash screen whilst loading the application
##
################################################################################

import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QEvent,
                          QMetaObject, QObject, QPoint, QPropertyAnimation,
                          QRect, QSize, Qt, QTime, QUrl)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                         QFontDatabase, QIcon, QKeySequence, QLinearGradient,
                         QPainter, QPalette, QPixmap, QRadialGradient)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
                             QDateTimeEdit, QDial, QDoubleSpinBox,
                             QFontComboBox, QGraphicsDropShadowEffect, QLabel,
                             QLCDNumber, QLineEdit, QMainWindow, QProgressBar,
                             QPushButton, QRadioButton, QSlider, QSpinBox,
                             QTimeEdit, QVBoxLayout, QWidget)

from src.qtdesigner.ui_splashscreen import Ui_SplashScreen
from .mainwindow import MainWindow


class SplashScreen(QMainWindow):    
    def __init__(self):
        super().__init__()

        # QT DESIGNER USER INTERFACE LINK
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # INITIALISE COMPONENTS
        self.ui.label_stage.setText("WELCOME TO <strong>DAISYCATTAX</strong>")
        self.initialiseTitleBar()
        self.initialiseDropShadowEffect()

        # SET UP TIMER PROGRESS BAR
        self.counter = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)

        # BUILD STEPS
        milliseconds = 20
        self.timer.start(milliseconds)
        self.timer.singleShot(800, lambda: self.ui.label_stage.setText("LOADING <strong>DATABASE</strong>"))
        self.timer.singleShot(1200, lambda: self.ui.label_stage.setText("MATCHING <strong>TRANSACTIONS</strong>"))
        self.timer.singleShot(1500, lambda: self.ui.label_stage.setText("LOADING <strong>USER INTERFACE</strong>"))
        # TODO Replace with build steps (split into stages & use a timer/pause for each stage to match to progress)

        self.show()

    ## CLASS METHODS ==> INITIALISATION
    ######################################################################## 
    def initialiseTitleBar(self):
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
     
    def initialiseDropShadowEffect(self):
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
        
    ## CLASS METHODS ==> PROGRESS BAR
    ########################################################################  
    def progress(self):
        self.ui.progressBar.setValue(self.counter)
        self.counter += 1
        
        if self.counter > 100:
            self.timer.stop()
            self.main = MainWindow()
            self.main.show()
            self.close()

