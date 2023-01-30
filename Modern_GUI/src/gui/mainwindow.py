################################################################################
##
## BY:      Sunil Patel
## MODULE:  MainWindow Class - the underlying GUI layout and functionality
##
################################################################################


from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from src.app_settings import Settings
from src.gui.custom_grips import CustomGrip

from src.qtdesigner.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # QT DESIGNER USER INTERFACE CONVERTED TO PYTHON
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # INITIALISE COMPONENTS
        self.MAXIMISED_WINDOW = False       
        self.initialiseTitleBar()
        self.initialiseTitleRightInfo()
        self.initialiseGrips()
        self.initialiseDropShadowEffect()

        # TABLEWIDGET PARAMETERS
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # SET STANDARD WINDOW BUTTON ACTIONS - MINIMIZE, MAXIMIZE/RESTORE & CLOSE
        self.ui.minimizeAppBtn.clicked.connect(self.showMinimized)
        self.ui.maximizeRestoreAppBtn.clicked.connect(self.maximizeRestore)
        self.ui.closeAppBtn.clicked.connect(self.close)

        # SET MENU BUTTON ACTIONS (LEFT)
        self.ui.toggleButton.clicked.connect(self.toggleMenu)
        self.ui.btn_home.clicked.connect(self.menuButtonClick)
        self.ui.btn_widgets.clicked.connect(self.menuButtonClick)
        self.ui.btn_new.clicked.connect(self.menuButtonClick)
        self.ui.btn_save.clicked.connect(self.menuButtonClick)

        # SET BOX PANEL TOGGLE BUTTON ACTIONS (LEFT & RIGHT)
        self.ui.toggleLeftBox.clicked.connect(self.toggleLeftBox)
        self.ui.extraCloseColumnBtn.clicked.connect(self.toggleLeftBox)
        self.ui.settingsTopBtn.clicked.connect(self.toggleRightBox)
        
        # SET TO HOME PAGE
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)
        self.ui.btn_home.setStyleSheet(self.highlightMenuItem(self.ui.btn_home.styleSheet()))        
        self.show()        
         
    ## CLASS METHODS ==> INITIALISATION
    ######################################################################## 
    def initialiseTitleBar(self):
        self.setWindowTitle(Settings.TITLE) 
        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            # REMOVE STANDARD TITLE BAR
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)            
         
    def initialiseTitleRightInfo(self):
        self.ui.titleRightInfo.setText(Settings.DESCRIPTION)
        self.ui.titleRightInfo.mouseDoubleClickEvent = self.doubleClickMaximizeRestore
        self.ui.titleRightInfo.mouseMoveEvent = self.moveWindow
        
    def initialiseGrips(self):
        
        if Settings.ENABLE_CUSTOM_TITLE_BAR:

            # CUSTOM GRIPS
            self.left_grip = CustomGrip(self, Qt.LeftEdge, True)
            self.right_grip = CustomGrip(self, Qt.RightEdge, True)
            self.top_grip = CustomGrip(self, Qt.TopEdge, True)
            self.bottom_grip = CustomGrip(self, Qt.BottomEdge, True)

        else:
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.minimizeAppBtn.hide()
            self.ui.maximizeRestoreAppBtn.hide()
            self.ui.closeAppBtn.hide()
            self.ui.frame_size_grip.hide()

        # RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;") 
        
    def initialiseDropShadowEffect(self):    
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)
        
    ## CLASS METHODS ==> MOUSE CLICK EVENTS
    ########################################################################
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        # TODO Actions still to be set up    
            
    ## CLASS METHODS ==> MENU (LEFT)
    ########################################################################
    def menuButtonClick(self):
        # GET MENU BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.home) # SET PAGE
            btn.setStyleSheet(self.highlightMenuItem(btn.styleSheet())) # RESET MENU BACKGROUNDS

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.widgets)
            btn.setStyleSheet(self.highlightMenuItem(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            self.ui.stackedWidget.setCurrentWidget(self.ui.new_page)
            btn.setStyleSheet(self.highlightMenuItem(btn.styleSheet()))

        if btnName == "btn_save":
            print("Save BTN clicked!")

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')
        # TODO Add Exit button & any other buttons
    
    def toggleMenu(self):
        # GET WIDTH
        width = self.ui.leftMenuBg.width()
        maxExtend = Settings.MENU_WIDTH
        standard = 60

        # SET MAX WIDTH
        if width == 60:
            widthExtended = maxExtend
        else:
            widthExtended = standard

        # ANIMATION
        self.animation = QPropertyAnimation(self.ui.leftMenuBg, b"minimumWidth")
        self.animation.setDuration(Settings.TIME_ANIMATION)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def highlightMenuItem(self, getStyle):
        # RESET BACKGROUND FOR ALL MENU ITEMS        
        for w in self.ui.topMenu.findChildren(QPushButton):
            deselect = w.styleSheet().replace(Settings.MENU_SELECTED_STYLESHEET, "")
            w.setStyleSheet(deselect)
        # GET THE STYLESHEET FOR THE SELECTED BUTTON                    
        select = getStyle + Settings.MENU_SELECTED_STYLESHEET
        return select
       
    ## CLASS METHODS ==> BOX PANEL TOGGLES (LEFT & RIGHT)
    ########################################################################
    def toggleLeftBox(self):
        # GET WIDTH
        width = self.ui.extraLeftBox.width()
        widthRightBox = self.ui.extraRightBox.width()
        maxExtend = Settings.LEFT_BOX_WIDTH
        color = Settings.BTN_LEFT_BOX_COLOR
        standard = 0

        # GET BTN STYLE
        style = self.ui.toggleLeftBox.styleSheet()

        # SET MAX WIDTH
        if width == 0:
            widthExtended = maxExtend
            # SELECT BTN
            self.ui.toggleLeftBox.setStyleSheet(style + color)
            if widthRightBox != 0:
                style = self.ui.settingsTopBtn.styleSheet()
                self.ui.settingsTopBtn.setStyleSheet(style.replace(Settings.BTN_RIGHT_BOX_COLOR, ''))
        else:
            widthExtended = standard
            # RESET BTN
            self.ui.toggleLeftBox.setStyleSheet(style.replace(color, ''))
                
        self.boxAnimation(width, widthRightBox, "left")

    def toggleRightBox(self):
        # GET WIDTH
        width = self.ui.extraRightBox.width()
        widthLeftBox = self.ui.extraLeftBox.width()
        maxExtend = Settings.RIGHT_BOX_WIDTH
        color = Settings.BTN_RIGHT_BOX_COLOR
        standard = 0
        # GET BTN STYLE
        style = self.ui.settingsTopBtn.styleSheet()
        # SET MAX WIDTH
        if width == 0:
            widthExtended = maxExtend
            # SELECT BTN
            self.ui.settingsTopBtn.setStyleSheet(style + color)
            if widthLeftBox != 0:
                style = self.ui.toggleLeftBox.styleSheet()
                self.ui.toggleLeftBox.setStyleSheet(style.replace(Settings.BTN_LEFT_BOX_COLOR, ''))
        else:
            widthExtended = standard
            # RESET BTN
            self.ui.settingsTopBtn.setStyleSheet(style.replace(color, ''))

        self.boxAnimation(widthLeftBox, width, "right")

    def boxAnimation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0 

        # Check values
        if left_box_width == 0 and direction == "left":
            left_width = 240
        else:
            left_width = 0
        # Check values
        if right_box_width == 0 and direction == "right":
            right_width = 240
        else:
            right_width = 0       

        # ANIMATION LEFT BOX        
        self.left_box = QPropertyAnimation(self.ui.extraLeftBox, b"minimumWidth")
        self.left_box.setDuration(Settings.TIME_ANIMATION)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

        # ANIMATION RIGHT BOX        
        self.right_box = QPropertyAnimation(self.ui.extraRightBox, b"minimumWidth")
        self.right_box.setDuration(Settings.TIME_ANIMATION)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()

    ## CLASS METHODS ==> MOVE OR RESIZE WINDOW
    ########################################################################
    def moveWindow(self, event):
        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            # IF MAXIMIZED CHANGE TO NORMAL
            if self.MAXIMISED_WINDOW:
                self.maximizeRestore()
            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()  
                
    def resizeEvent(self, event):        
        def resize_grips():
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)
            
        # Update Size Grips
        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            resize_grips()    
    
    def maximizeRestore(self):
        if not self.MAXIMISED_WINDOW:
            self.showMaximized()
            self.MAXIMISED_WINDOW = True
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.maximizeRestoreAppBtn.setToolTip("Restore")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_restore.png"))
            self.ui.frame_size_grip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
        else:
            self.MAXIMISED_WINDOW = False
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.appMargins.setContentsMargins(10, 10, 10, 10)
            self.ui.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_maximize.png"))
            self.ui.frame_size_grip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()
  
    def doubleClickMaximizeRestore(self, event):
        # IF DOUBLE CLICK CHANGE STATUS
        if event.type() == QEvent.MouseButtonDblClick:
            QTimer.singleShot(250, self.maximizeRestore)
            