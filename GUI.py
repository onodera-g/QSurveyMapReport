import os
from qgis.PyQt import QtCore, QtGui, QtWidgets

try:
    from .qt_compat import (
        COMPOSITION_MODE_SOURCE_IN,
        FONT_MONOSPACE,
        SCROLL_BAR_ALWAYS_OFF,
        SCROLL_BAR_AS_NEEDED,
        WIDGET_WIDTH,
        app_exec,
    )
except ImportError:
    from qt_compat import (
        COMPOSITION_MODE_SOURCE_IN,
        FONT_MONOSPACE,
        SCROLL_BAR_ALWAYS_OFF,
        SCROLL_BAR_AS_NEEDED,
        WIDGET_WIDTH,
        app_exec,
    )


class Ui_MainWindow(object):
    @staticmethod
    def _create_themed_icon(icon_path, color):
        pixmap = QtGui.QPixmap(icon_path)
        if pixmap.isNull():
            return QtGui.QIcon(icon_path)

        tinted = QtGui.QPixmap(pixmap.size())
        tinted.fill(QtGui.QColor(0, 0, 0, 0))

        painter = QtGui.QPainter(tinted)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(COMPOSITION_MODE_SOURCE_IN)
        painter.fillRect(tinted.rect(), color)
        painter.end()
        return QtGui.QIcon(tinted)

    @staticmethod
    def _apply_themed_panel(widget):
        base_color = widget.palette().base().color().name()
        border_color = widget.palette().mid().color().name()
        widget.setStyleSheet(
            f"background-color: {base_color}; border: 1px solid {border_color};"
        )

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(860, 635)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Path button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(745, 20, 75, 20))
        self.pushButton.setObjectName("pushButton")

        # make csv button
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(750, 540, 75, 20))
        self.pushButton_4.setObjectName("pushButton_4")

        # make pdf button
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(750, 570, 75, 20))
        self.pushButton_7.setObjectName("pushButton_7")

        # ◀／▶ button
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(570, 540, 75, 20))
        self.pushButton_6.setObjectName("pushButton_6")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(660, 540, 75, 20))
        self.pushButton_5.setObjectName("pushButton_5")

        # input map button
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(660, 570, 75, 20))
        self.pushButton_2.setObjectName("pushButton_2")

        # update list button
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 540, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")

        # 180度回転button
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(480, 540, 75, 20))
        self.pushButton_8.setObjectName("pushButton_8")

        # icon
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icons = {
            'pushButton_2': 'map.png',
            'pushButton_3': 'update.png',
            'pushButton_4': 'csv.png',
            'pushButton_5': 'right.png',
            'pushButton_6': 'left.png',
            'pushButton_7': 'pdf.png',
            'pushButton_8': 'rotate_180_icon.png',
        }
        for btn_name, ico in icons.items():
            btn = getattr(self, btn_name, None)
            if not btn:
                continue
            ico_path = os.path.join(script_dir, 'icon', ico)
            if os.path.exists(ico_path):
                icon_color = btn.palette().buttonText().color()
                icon = self._create_themed_icon(ico_path, icon_color)
                if not icon.isNull():
                    btn.setIcon(icon)
                    btn.setIconSize(QtCore.QSize(15, 15))

        # path select
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 20, 720, 20))
        self.lineEdit.setObjectName("lineEdit")

        # pic list
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 70, 256, 461))
        self.listWidget.setObjectName("listWidget")

        # pic box
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 70, 520, 290))
        self._apply_themed_panel(self.label)
        self.label.setObjectName("label")

        # pic number
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(300, 370, 520, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")

        # file list
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(300, 400, 520, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")

        # text box
        self.textEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(300, 430, 520, 100))
        self.textEdit.setObjectName("textEdit")

        # font
        font = QtGui.QFont("MS Gothic", 10)
        font.setStyleHint(FONT_MONOSPACE)
        self.textEdit.setFont(font)

        # scroll
        self.textEdit.setLineWrapMode(WIDGET_WIDTH)
        self.textEdit.setHorizontalScrollBarPolicy(
            SCROLL_BAR_ALWAYS_OFF)
        self.textEdit.setVerticalScrollBarPolicy(SCROLL_BAR_AS_NEEDED)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "Menu_Dialog", "QSurveyMapReport"))
        self.pushButton.setText(_translate("Menu_Dialog", "......"))
        self.pushButton_2.setText(_translate("Menu_Dialog", "input map"))
        self.pushButton_3.setText("")
        self.pushButton_4.setText(_translate("Menu_Dialog", "make csv"))
        self.pushButton_5.setText("")
        self.pushButton_6.setText("")
        self.pushButton_7.setText(_translate("Menu_Dialog", "make pdf"))
        self.label.setText(_translate("Menu_Dialog", "TextLabel"))
        self.pushButton_8.setText("")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app_exec(app))
