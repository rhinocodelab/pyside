# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'updatedialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStackedWidget, QVBoxLayout,
    QWidget)
from .masked_password import Leforpassword

class Ui_UpdateDialog(object):
    def setupUi(self, UpdateDialog):
        if not UpdateDialog.objectName():
            UpdateDialog.setObjectName(u"UpdateDialog")
        UpdateDialog.resize(585, 440)
        icon = QIcon()
        icon.addFile(u"../resources/images/setting.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        UpdateDialog.setWindowIcon(icon)
        self.gridLayout_7 = QGridLayout(UpdateDialog)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.CHK_UpdateOnBoot = QCheckBox(UpdateDialog)
        self.CHK_UpdateOnBoot.setObjectName(u"CHK_UpdateOnBoot")
        self.CHK_UpdateOnBoot.setEnabled(True)
        self.CHK_UpdateOnBoot.setMinimumSize(QSize(250, 27))
        self.CHK_UpdateOnBoot.setMaximumSize(QSize(250, 27))

        self.gridLayout_7.addWidget(self.CHK_UpdateOnBoot, 2, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(188, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_5, 5, 1, 1, 2)

        self.line_3 = QFrame(UpdateDialog)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setMinimumSize(QSize(567, 1))
        self.line_3.setMaximumSize(QSize(567, 1))
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_7.addWidget(self.line_3, 1, 0, 1, 3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.LB_Method = QLabel(UpdateDialog)
        self.LB_Method.setObjectName(u"LB_Method")

        self.horizontalLayout_3.addWidget(self.LB_Method)

        self.CB_Method = QComboBox(UpdateDialog)
        self.CB_Method.setObjectName(u"CB_Method")
        self.CB_Method.setMinimumSize(QSize(161, 27))
        self.CB_Method.setMaximumSize(QSize(161, 27))

        self.horizontalLayout_3.addWidget(self.CB_Method)


        self.gridLayout_7.addLayout(self.horizontalLayout_3, 4, 0, 2, 1)

        self.line = QFrame(UpdateDialog)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(0, 1))
        self.line.setMaximumSize(QSize(16777215, 1))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_7.addWidget(self.line, 3, 0, 1, 3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.LB_Loading = QLabel(UpdateDialog)
        self.LB_Loading.setObjectName(u"LB_Loading")
        self.LB_Loading.setMinimumSize(QSize(32, 32))
        self.LB_Loading.setMaximumSize(QSize(32, 32))
        self.LB_Loading.setScaledContents(True)

        self.horizontalLayout_5.addWidget(self.LB_Loading)

        self.LB_ShowText = QLabel(UpdateDialog)
        self.LB_ShowText.setObjectName(u"LB_ShowText")

        self.horizontalLayout_5.addWidget(self.LB_ShowText)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalSpacer_6 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.PB_Save = QPushButton(UpdateDialog)
        self.PB_Save.setObjectName(u"PB_Save")
        self.PB_Save.setMinimumSize(QSize(0, 27))
        self.PB_Save.setMaximumSize(QSize(16777215, 27))

        self.horizontalLayout_4.addWidget(self.PB_Save)

        self.PB_SaveUpdate = QPushButton(UpdateDialog)
        self.PB_SaveUpdate.setObjectName(u"PB_SaveUpdate")
        self.PB_SaveUpdate.setMinimumSize(QSize(0, 27))
        self.PB_SaveUpdate.setMaximumSize(QSize(16777215, 27))

        self.horizontalLayout_4.addWidget(self.PB_SaveUpdate)

        self.PB_Close = QPushButton(UpdateDialog)
        self.PB_Close.setObjectName(u"PB_Close")
        self.PB_Close.setMinimumSize(QSize(0, 27))
        self.PB_Close.setMaximumSize(QSize(16777215, 27))

        self.horizontalLayout_4.addWidget(self.PB_Close)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)


        self.gridLayout_7.addLayout(self.horizontalLayout_6, 7, 0, 1, 3)

        self.stackedWidget = QStackedWidget(UpdateDialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setFrameShape(QFrame.Box)
        self.stackedWidget.setFrameShadow(QFrame.Raised)
        self.pageDHCP = QWidget()
        self.pageDHCP.setObjectName(u"pageDHCP")
        self.gridLayout_2 = QGridLayout(self.pageDHCP)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer_3 = QSpacerItem(20, 46, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(73, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.pageDHCP)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(self.pageDHCP)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.SB_ConfScopeID = QSpinBox(self.pageDHCP)
        self.SB_ConfScopeID.setObjectName(u"SB_ConfScopeID")
        self.SB_ConfScopeID.setMinimumSize(QSize(75, 27))
        self.SB_ConfScopeID.setMaximumSize(QSize(75, 27))
        self.SB_ConfScopeID.setMinimum(1)
        self.SB_ConfScopeID.setMaximum(999)
        self.SB_ConfScopeID.setValue(130)

        self.verticalLayout_4.addWidget(self.SB_ConfScopeID)

        self.SB_UpgScopeID = QSpinBox(self.pageDHCP)
        self.SB_UpgScopeID.setObjectName(u"SB_UpgScopeID")
        self.SB_UpgScopeID.setMinimumSize(QSize(75, 27))
        self.SB_UpgScopeID.setMaximumSize(QSize(75, 27))
        self.SB_UpgScopeID.setMinimum(1)
        self.SB_UpgScopeID.setMaximum(999)
        self.SB_UpgScopeID.setValue(131)

        self.verticalLayout_4.addWidget(self.SB_UpgScopeID)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(73, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 1, 2, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 46, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 2, 1, 1, 1)

        self.stackedWidget.addWidget(self.pageDHCP)
        self.pageHTTPFTP = QWidget()
        self.pageHTTPFTP.setObjectName(u"pageHTTPFTP")
        self.gridLayout_3 = QGridLayout(self.pageHTTPFTP)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_28 = QLabel(self.pageHTTPFTP)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(144, 0))
        self.label_28.setMaximumSize(QSize(144, 16777215))
        self.label_28.setWordWrap(True)

        self.gridLayout.addWidget(self.label_28, 0, 0, 1, 1)

        self.LE_IP = QLineEdit(self.pageHTTPFTP)
        self.LE_IP.setObjectName(u"LE_IP")
        self.LE_IP.setMinimumSize(QSize(195, 27))
        self.LE_IP.setMaximumSize(QSize(195, 27))
        self.LE_IP.setMaxLength(1000)

        self.gridLayout.addWidget(self.LE_IP, 0, 1, 1, 1)

        self.PB_LVFS_Refresh = QPushButton(self.pageHTTPFTP)
        self.PB_LVFS_Refresh.setObjectName(u"PB_LVFS_Refresh")

        self.gridLayout.addWidget(self.PB_LVFS_Refresh, 0, 2, 1, 1)

        self.LB_Username = QLabel(self.pageHTTPFTP)
        self.LB_Username.setObjectName(u"LB_Username")
        self.LB_Username.setMinimumSize(QSize(144, 0))
        self.LB_Username.setMaximumSize(QSize(144, 16777215))
        self.LB_Username.setWordWrap(True)

        self.gridLayout.addWidget(self.LB_Username, 1, 0, 1, 1)

        self.LE_Username = QLineEdit(self.pageHTTPFTP)
        self.LE_Username.setObjectName(u"LE_Username")
        self.LE_Username.setMinimumSize(QSize(195, 27))
        self.LE_Username.setMaximumSize(QSize(195, 27))
        self.LE_Username.setMaxLength(50)

        self.gridLayout.addWidget(self.LE_Username, 1, 1, 1, 1)

        self.LB_Password = QLabel(self.pageHTTPFTP)
        self.LB_Password.setObjectName(u"LB_Password")
        self.LB_Password.setMinimumSize(QSize(144, 0))
        self.LB_Password.setMaximumSize(QSize(144, 16777215))
        self.LB_Password.setWordWrap(True)

        self.gridLayout.addWidget(self.LB_Password, 2, 0, 1, 1)

        self.LE_Password = Leforpassword(self.pageHTTPFTP)
        self.LE_Password.setObjectName(u"LE_Password")
        self.LE_Password.setMinimumSize(QSize(195, 27))
        self.LE_Password.setMaximumSize(QSize(195, 27))
        self.LE_Password.setFocusPolicy(Qt.StrongFocus)

        self.gridLayout.addWidget(self.LE_Password, 2, 1, 1, 1)

        self.label_32 = QLabel(self.pageHTTPFTP)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setMinimumSize(QSize(144, 0))
        self.label_32.setMaximumSize(QSize(144, 16777215))
        self.label_32.setWordWrap(True)

        self.gridLayout.addWidget(self.label_32, 3, 0, 1, 1)

        self.LE_ConfFilename = QLineEdit(self.pageHTTPFTP)
        self.LE_ConfFilename.setObjectName(u"LE_ConfFilename")
        self.LE_ConfFilename.setMinimumSize(QSize(195, 27))
        self.LE_ConfFilename.setMaximumSize(QSize(195, 27))
        self.LE_ConfFilename.setMaxLength(255)

        self.gridLayout.addWidget(self.LE_ConfFilename, 3, 1, 1, 1)

        self.label_33 = QLabel(self.pageHTTPFTP)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setMinimumSize(QSize(144, 0))
        self.label_33.setMaximumSize(QSize(144, 16777215))
        self.label_33.setWordWrap(True)

        self.gridLayout.addWidget(self.label_33, 4, 0, 1, 1)

        self.LE_UpgFilename = QLineEdit(self.pageHTTPFTP)
        self.LE_UpgFilename.setObjectName(u"LE_UpgFilename")
        self.LE_UpgFilename.setMinimumSize(QSize(195, 27))
        self.LE_UpgFilename.setMaximumSize(QSize(195, 27))
        self.LE_UpgFilename.setMaxLength(255)

        self.gridLayout.addWidget(self.LE_UpgFilename, 4, 1, 1, 1)

        self.LB_BiosPassword = QLabel(self.pageHTTPFTP)
        self.LB_BiosPassword.setObjectName(u"LB_BiosPassword")
        self.LB_BiosPassword.setMinimumSize(QSize(144, 0))
        self.LB_BiosPassword.setMaximumSize(QSize(144, 16777215))
        self.LB_BiosPassword.setWordWrap(True)

        self.gridLayout.addWidget(self.LB_BiosPassword, 5, 0, 1, 1)

        self.LE_BiosPassword = Leforpassword(self.pageHTTPFTP)
        self.LE_BiosPassword.setObjectName(u"LE_BiosPassword")
        self.LE_BiosPassword.setMinimumSize(QSize(195, 27))
        self.LE_BiosPassword.setMaximumSize(QSize(195, 27))
        self.LE_BiosPassword.setFocusPolicy(Qt.StrongFocus)

        self.gridLayout.addWidget(self.LE_BiosPassword, 5, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.pageHTTPFTP)
        self.USB = QWidget()
        self.USB.setObjectName(u"USB")
        self.gridLayout_6 = QGridLayout(self.USB)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.verticalSpacer_8 = QSpacerItem(20, 63, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_8, 0, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(79, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_9, 1, 0, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label = QLabel(self.USB)
        self.label.setObjectName(u"label")

        self.verticalLayout_5.addWidget(self.label)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.LE_Filename = QLineEdit(self.USB)
        self.LE_Filename.setObjectName(u"LE_Filename")
        self.LE_Filename.setMinimumSize(QSize(290, 27))
        self.LE_Filename.setMaximumSize(QSize(290, 27))
        self.LE_Filename.setMaxLength(255)

        self.horizontalLayout_7.addWidget(self.LE_Filename)

        self.PB_Browse = QPushButton(self.USB)
        self.PB_Browse.setObjectName(u"PB_Browse")
        self.PB_Browse.setMinimumSize(QSize(27, 27))
        self.PB_Browse.setMaximumSize(QSize(27, 27))

        self.horizontalLayout_7.addWidget(self.PB_Browse)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)


        self.gridLayout_6.addLayout(self.verticalLayout_5, 1, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(79, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_10, 1, 2, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 63, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_7, 2, 1, 1, 1)

        self.stackedWidget.addWidget(self.USB)
        self.pageBuddy = QWidget()
        self.pageBuddy.setObjectName(u"pageBuddy")
        self.gridLayout_5 = QGridLayout(self.pageBuddy)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalSpacer_8 = QSpacerItem(61, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_8, 1, 3, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 36, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_5, 3, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(61, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_7, 1, 0, 1, 1)

        self.frame = QFrame(self.pageBuddy)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.line_2 = QFrame(self.frame)
        self.line_2.setObjectName(u"line_2")
        font = QFont()
        font.setBold(True)
        font.setKerning(True)
        self.line_2.setFont(font)
        self.line_2.setAutoFillBackground(False)
        self.line_2.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.line_2.setFrameShadow(QFrame.Plain)
        self.line_2.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_4.addWidget(self.line_2, 2, 0, 2, 5)

        self.RB_Client = QRadioButton(self.frame)
        self.RB_Client.setObjectName(u"RB_Client")
        self.RB_Client.setChecked(True)

        self.gridLayout_4.addWidget(self.RB_Client, 0, 1, 1, 1)

        self.PB_CSearch = QPushButton(self.frame)
        self.PB_CSearch.setObjectName(u"PB_CSearch")

        self.gridLayout_4.addWidget(self.PB_CSearch, 1, 4, 1, 1)

        self.RB_Server = QRadioButton(self.frame)
        self.RB_Server.setObjectName(u"RB_Server")

        self.gridLayout_4.addWidget(self.RB_Server, 3, 1, 2, 1)

        self.PB_SSerarch = QPushButton(self.frame)
        self.PB_SSerarch.setObjectName(u"PB_SSerarch")

        self.gridLayout_4.addWidget(self.PB_SSerarch, 4, 4, 1, 1)

        self.PB_SyncServer = QPushButton(self.frame)
        self.PB_SyncServer.setObjectName(u"PB_SyncServer")

        self.gridLayout_4.addWidget(self.PB_SyncServer, 4, 3, 1, 1)

        self.PB_TestSever = QPushButton(self.frame)
        self.PB_TestSever.setObjectName(u"PB_TestSever")
        self.PB_TestSever.setMinimumSize(QSize(41, 23))
        self.PB_TestSever.setMaximumSize(QSize(41, 23))

        self.gridLayout_4.addWidget(self.PB_TestSever, 1, 3, 1, 1)

        self.CB_IP = QComboBox(self.frame)
        self.CB_IP.setObjectName(u"CB_IP")
        self.CB_IP.setMinimumSize(QSize(200, 27))
        self.CB_IP.setEditable(True)

        self.gridLayout_4.addWidget(self.CB_IP, 1, 1, 1, 1)

        self.line_2.raise_()
        self.PB_CSearch.raise_()
        self.PB_SSerarch.raise_()
        self.RB_Server.raise_()
        self.RB_Client.raise_()
        self.CB_IP.raise_()
        self.PB_SyncServer.raise_()
        self.PB_TestSever.raise_()

        self.gridLayout_5.addWidget(self.frame, 1, 1, 1, 2)

        self.LB_NoteServer = QLabel(self.pageBuddy)
        self.LB_NoteServer.setObjectName(u"LB_NoteServer")
        self.LB_NoteServer.setEnabled(True)
        self.LB_NoteServer.setMinimumSize(QSize(0, 27))
        self.LB_NoteServer.setMaximumSize(QSize(16777215, 27))
        self.LB_NoteServer.setStyleSheet(u"color: blue;")

        self.gridLayout_5.addWidget(self.LB_NoteServer, 2, 1, 1, 2)

        self.verticalSpacer_6 = QSpacerItem(20, 24, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_6, 0, 2, 1, 1)

        self.stackedWidget.addWidget(self.pageBuddy)

        self.gridLayout_7.addWidget(self.stackedWidget, 6, 0, 1, 3)

        self.RB_PromptUser = QRadioButton(UpdateDialog)
        self.RB_PromptUser.setObjectName(u"RB_PromptUser")
        self.RB_PromptUser.setMinimumSize(QSize(0, 27))
        self.RB_PromptUser.setMouseTracking(False)

        self.gridLayout_7.addWidget(self.RB_PromptUser, 2, 1, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.LB_UpdateWith = QLabel(UpdateDialog)
        self.LB_UpdateWith.setObjectName(u"LB_UpdateWith")

        self.horizontalLayout_8.addWidget(self.LB_UpdateWith)

        self.CB_UpgradeType = QComboBox(UpdateDialog)
        self.CB_UpgradeType.setObjectName(u"CB_UpgradeType")
        self.CB_UpgradeType.setMinimumSize(QSize(161, 27))
        self.CB_UpgradeType.setMaximumSize(QSize(161, 27))
        self.CB_UpgradeType.setSizeIncrement(QSize(161, 27))

        self.horizontalLayout_8.addWidget(self.CB_UpgradeType)

        self.PB_LVFS_Device = QPushButton(UpdateDialog)
        self.PB_LVFS_Device.setObjectName(u"PB_LVFS_Device")
        self.PB_LVFS_Device.setMinimumSize(QSize(135, 27))

        self.horizontalLayout_8.addWidget(self.PB_LVFS_Device)

        self.horizontalSpacer_11 = QSpacerItem(78, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_11)


        self.gridLayout_7.addLayout(self.horizontalLayout_8, 0, 0, 1, 3)

        self.RB_UpdateOnBoot = QRadioButton(UpdateDialog)
        self.RB_UpdateOnBoot.setObjectName(u"RB_UpdateOnBoot")
        self.RB_UpdateOnBoot.setMinimumSize(QSize(0, 27))
        self.RB_UpdateOnBoot.setMouseTracking(False)

        self.gridLayout_7.addWidget(self.RB_UpdateOnBoot, 2, 2, 1, 1)

        QWidget.setTabOrder(self.CB_UpgradeType, self.PB_LVFS_Device)
        QWidget.setTabOrder(self.PB_LVFS_Device, self.CHK_UpdateOnBoot)
        QWidget.setTabOrder(self.CHK_UpdateOnBoot, self.RB_PromptUser)
        QWidget.setTabOrder(self.RB_PromptUser, self.RB_UpdateOnBoot)
        QWidget.setTabOrder(self.RB_UpdateOnBoot, self.CB_Method)
        QWidget.setTabOrder(self.CB_Method, self.SB_ConfScopeID)
        QWidget.setTabOrder(self.SB_ConfScopeID, self.SB_UpgScopeID)
        QWidget.setTabOrder(self.SB_UpgScopeID, self.LE_IP)
        QWidget.setTabOrder(self.LE_IP, self.PB_LVFS_Refresh)
        QWidget.setTabOrder(self.PB_LVFS_Refresh, self.LE_Username)
        QWidget.setTabOrder(self.LE_Username, self.LE_Password)
        QWidget.setTabOrder(self.LE_Password, self.LE_ConfFilename)
        QWidget.setTabOrder(self.LE_ConfFilename, self.LE_UpgFilename)
        QWidget.setTabOrder(self.LE_UpgFilename, self.LE_BiosPassword)
        QWidget.setTabOrder(self.LE_BiosPassword, self.LE_Filename)
        QWidget.setTabOrder(self.LE_Filename, self.PB_Browse)
        QWidget.setTabOrder(self.PB_Browse, self.RB_Client)
        QWidget.setTabOrder(self.RB_Client, self.CB_IP)
        QWidget.setTabOrder(self.CB_IP, self.PB_TestSever)
        QWidget.setTabOrder(self.PB_TestSever, self.PB_CSearch)
        QWidget.setTabOrder(self.PB_CSearch, self.RB_Server)
        QWidget.setTabOrder(self.RB_Server, self.PB_SyncServer)
        QWidget.setTabOrder(self.PB_SyncServer, self.PB_SSerarch)
        QWidget.setTabOrder(self.PB_SSerarch, self.PB_Save)
        QWidget.setTabOrder(self.PB_Save, self.PB_SaveUpdate)
        QWidget.setTabOrder(self.PB_SaveUpdate, self.PB_Close)

        self.retranslateUi(UpdateDialog)

        self.stackedWidget.setCurrentIndex(1)
        self.CB_IP.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(UpdateDialog)
    # setupUi

    def retranslateUi(self, UpdateDialog):
        UpdateDialog.setWindowTitle(QCoreApplication.translate("UpdateDialog", u"Firmware Updates", None))
        self.CHK_UpdateOnBoot.setText(QCoreApplication.translate("UpdateDialog", u"Check for update on boot", None))
        self.LB_Method.setText(QCoreApplication.translate("UpdateDialog", u"Method: ", None))
        self.LB_Loading.setText("")
        self.LB_ShowText.setText(QCoreApplication.translate("UpdateDialog", u"Updating...", None))
        self.PB_Save.setText(QCoreApplication.translate("UpdateDialog", u"Save ", None))
        self.PB_SaveUpdate.setText(QCoreApplication.translate("UpdateDialog", u"Save && Update", None))
        self.PB_Close.setText(QCoreApplication.translate("UpdateDialog", u"Close", None))
        self.label_2.setText(QCoreApplication.translate("UpdateDialog", u"Configuration Scope ID: ", None))
        self.label_3.setText(QCoreApplication.translate("UpdateDialog", u"Upgrade Scope ID: ", None))
        self.label_28.setText(QCoreApplication.translate("UpdateDialog", u"Server:", None))
        self.LE_IP.setText("")
        self.PB_LVFS_Refresh.setText("")
        self.LB_Username.setText(QCoreApplication.translate("UpdateDialog", u"Username: ", None))
        self.LE_Username.setText("")
        self.LB_Password.setText(QCoreApplication.translate("UpdateDialog", u"Password:", None))
        self.label_33.setText(QCoreApplication.translate("UpdateDialog", u"Upgrade File Path: ", None))
        self.LE_UpgFilename.setText("")
        self.LE_UpgFilename.setPlaceholderText(QCoreApplication.translate("UpdateDialog", u"eg: /home/test/test.tar.bz2", None))
        self.LB_BiosPassword.setText(QCoreApplication.translate("UpdateDialog", u"Bios Password:", None))
        self.label.setText(QCoreApplication.translate("UpdateDialog", u"Upgrade Filename", None))
        self.PB_Browse.setText(QCoreApplication.translate("UpdateDialog", u"...", None))
        self.RB_Client.setText(QCoreApplication.translate("UpdateDialog", u"Client", None))
        self.PB_CSearch.setText("")
        self.RB_Server.setText(QCoreApplication.translate("UpdateDialog", u"Server", None))
        self.PB_SSerarch.setText("")
#if QT_CONFIG(tooltip)
        self.PB_SyncServer.setToolTip(QCoreApplication.translate("UpdateDialog", u"Sync", None))
#endif // QT_CONFIG(tooltip)
        self.PB_SyncServer.setText("")
#if QT_CONFIG(tooltip)
        self.PB_TestSever.setToolTip(QCoreApplication.translate("UpdateDialog", u"Test Server", None))
#endif // QT_CONFIG(tooltip)
        self.PB_TestSever.setText("")
        self.LB_NoteServer.setText(QCoreApplication.translate("UpdateDialog", u"Note :  Changes will be applied after save click.", None))
        self.RB_PromptUser.setText(QCoreApplication.translate("UpdateDialog", u"Prompt User ", None))
        self.LB_UpdateWith.setText(QCoreApplication.translate("UpdateDialog", u"Upgrade Type :", None))
        self.PB_LVFS_Device.setText(QCoreApplication.translate("UpdateDialog", u"Firmware Details", None))
        self.RB_UpdateOnBoot.setText(QCoreApplication.translate("UpdateDialog", u"Auto", None))
        self.LE_ConfFilename.setText("")
        self.LE_ConfFilename.setPlaceholderText(QCoreApplication.translate("UpdateDialog", u"eg: /home/test/", None))
        self.label_32.setText(QCoreApplication.translate("UpdateDialog", u"Configuration File Directory: ", None))
    # retranslateUi

