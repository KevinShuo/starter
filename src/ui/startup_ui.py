# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'startup.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class StartupUI(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet(u"QTabWidget > QWidget{\n"
                                 "	background-color:#f5f4f1;\n"
                                 "}\n"
                                 "\n"
                                 "QTabWidget{\n"
                                 "	background-color: #f5f4f1;\n"
                                 "	font-family: Arial;\n"
                                 "	font-weight: bold;\n"
                                 "}")
        self.actionProjects = QAction(MainWindow)
        self.actionProjects.setObjectName(u"actionProjects")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.West)

        self.horizontalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 800, 30))
        # self.menuSettings = QMenu(self.menuBar)
        # self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menuBar)

        # self.menuBar.addAction(self.menuSettings.menuAction())
        # self.menuSettings.addAction(self.actionProjects)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionProjects.setText(QCoreApplication.translate("MainWindow", u"Projects", None))
        # self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi
