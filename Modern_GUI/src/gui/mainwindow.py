# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////


import os

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
# APP SETTINGS
from src.app_settings import Settings
from src.gui.custom_grips import CustomGrip
# GUI FILE
from src.qtdesigner.ui_mainwindow import Ui_MainWindow

#from src.app_functions import *
#FIXME Inherit from GUI instead


# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////

widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "PyDracula - Modern GUI"
        description = "PyDracula APP - Theme with colors based on Dracula for Python."
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        self.uiDefinitions()
        self.MAXIMISED_WINDOW = False

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # WINDOW BUTTONS - MINIMIZE, MAXIMIZE/RESTORE & CLOSE
        self.ui.minimizeAppBtn.clicked.connect(self.showMinimized)
        self.ui.maximizeRestoreAppBtn.clicked.connect(self.maximize_restore)
        self.ui.closeAppBtn.clicked.connect(self.close)

        # MENU BUTTONS (LEFT)
        widgets.toggleButton.clicked.connect(self.toggleMenu)
        widgets.btn_home.clicked.connect(self.menuButtonClick)
        widgets.btn_widgets.clicked.connect(self.menuButtonClick)
        widgets.btn_new.clicked.connect(self.menuButtonClick)
        widgets.btn_save.clicked.connect(self.menuButtonClick)

        # TOGGLE BOX PANELS (LEFT & RIGHT)
        widgets.toggleLeftBox.clicked.connect(self.toggleLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(self.toggleLeftBox)
        widgets.settingsTopBtn.clicked.connect(self.toggleRightBox)
        
        


        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "Modern_GUI\\themes\\py_dracula_light.qss"
        # FIXME Amend the folder
        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            self.theme(themeFile, True)

            # SET HACKS
            #AppFunctions.setThemeHack(self)
            # FIXME Inherit rather than circular call

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(self.highlightMenuItem(widgets.btn_home.styleSheet()))
        
        
        self.show()


   


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        self.resize_grips()

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
            
            
            
            
            


    # MENU FUNCTIONS (LEFT)
    # ///////////////////////////////////////////////////////////////
    def menuButtonClick(self):
        # GET MENU BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home) # SET PAGE
            btn.setStyleSheet(self.highlightMenuItem(btn.styleSheet())) # RESET MENU BACKGROUNDS

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            btn.setStyleSheet(self.highlightMenuItem(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)
            btn.setStyleSheet(self.highlightMenuItem(btn.styleSheet()))

        if btnName == "btn_save":
            print("Save BTN clicked!")

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')
    
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
       
    # TOGGLE BOX PANELS (LEFT & RIGHT)
    # ///////////////////////////////////////////////////////////////
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


    # IMPORT THEMES FILES QSS/CSS
    # ///////////////////////////////////////////////////////////////
    def theme(self, file, useCustomTheme):
        if useCustomTheme:
            str = open(file, 'r').read()
            self.ui.styleSheet.setStyleSheet(str)

    # START - GUI DEFINITIONS
    # ///////////////////////////////////////////////////////////////
    def uiDefinitions(self):
        def doubleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, self.maximize_restore)
        self.ui.titleRightInfo.mouseDoubleClickEvent = doubleClickMaximizeRestore

        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            # REMOVE STANDARD TITLE BAR
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            # MOVE WINDOW / MAXIMIZE / RESTORE
            def moveWindow(event):
                # IF MAXIMIZED CHANGE TO NORMAL
                if self.MAXIMISED_WINDOW:
                    self.maximize_restore()
                # MOVE WINDOW
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.dragPos)
                    self.dragPos = event.globalPos()
                    event.accept()
            self.ui.titleRightInfo.mouseMoveEvent = moveWindow

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

        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)

        # RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")


    def maximize_restore(self):
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
        
        
        
        
        

    def resize_grips(self):
        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)

    # ///////////////////////////////////////////////////////////////
    # END - GUI DEFINITIONS