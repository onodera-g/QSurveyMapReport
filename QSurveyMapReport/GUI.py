import os
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(860, 635)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 共通スタイル
        border_css = "border: 1px solid black;"

        # Path選択ボタン
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(745, 20, 75, 20))
        self.pushButton.setStyleSheet(border_css)
        self.pushButton.setObjectName("pushButton")

        # make csv ボタン
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(750, 540, 75, 20))
        self.pushButton_4.setStyleSheet(border_css)
        self.pushButton_4.setObjectName("pushButton_4")

        # make pdf ボタン
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(750, 570, 75, 20))
        self.pushButton_7.setStyleSheet(border_css)
        self.pushButton_7.setObjectName("pushButton_7")

        # ◀／▶ ボタン
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(570, 540, 75, 20))
        self.pushButton_6.setStyleSheet(border_css)
        self.pushButton_6.setObjectName("pushButton_6")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(660, 540, 75, 20))
        self.pushButton_5.setStyleSheet(border_css)
        self.pushButton_5.setObjectName("pushButton_5")

        # input map ボタン
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(660, 570, 75, 20))
        self.pushButton_2.setStyleSheet(border_css)
        self.pushButton_2.setObjectName("pushButton_2")

        # update list ボタン
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 540, 75, 23))
        self.pushButton_3.setStyleSheet(border_css)
        self.pushButton_3.setObjectName("pushButton_3")

        # 180度回転ボタン
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(480, 540, 75, 20))
        self.pushButton_8.setStyleSheet(border_css)
        self.pushButton_8.setObjectName("pushButton_8")

        # icon設定
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
                icon = QtGui.QIcon(ico_path)
                if not icon.isNull():
                    btn.setIcon(icon)
                    btn.setIconSize(QtCore.QSize(15, 15))

        # path表示
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 20, 720, 20))
        self.lineEdit.setStyleSheet(border_css)
        self.lineEdit.setObjectName("lineEdit")

        # 画像一覧
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 70, 256, 461))
        self.listWidget.setStyleSheet(border_css)
        self.listWidget.setObjectName("listWidget")

        # 画像表示
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 70, 520, 290))
        self.label.setStyleSheet(border_css)
        self.label.setObjectName("label")

        # 画像番号
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(300, 370, 520, 20))
        self.lineEdit_2.setStyleSheet(border_css)
        self.lineEdit_2.setObjectName("lineEdit_2")

        # ファイル名表示
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(300, 400, 520, 20))
        self.lineEdit_4.setStyleSheet(border_css)
        self.lineEdit_4.setObjectName("lineEdit_4")

        # テキスト入力
        self.textEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(300, 430, 520, 100))
        self.textEdit.setStyleSheet(border_css)
        self.textEdit.setObjectName("textEdit")

        # 等幅フォント
        font = QtGui.QFont("MS Gothic", 10)
        font.setStyleHint(QtGui.QFont.Monospace)
        self.textEdit.setFont(font)

        # テキストラップとスクロール設定
        self.textEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        self.textEdit.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QSurveyMapReport"))
        self.pushButton.setText(_translate("MainWindow", "......"))
        self.pushButton_2.setText(_translate("MainWindow", "input map"))
        self.pushButton_3.setText("")
        self.pushButton_4.setText(_translate("MainWindow", "make csv"))
        self.pushButton_5.setText("")
        self.pushButton_6.setText("")
        self.pushButton_7.setText(_translate("MainWindow", "make pdf"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton_8.setText("")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
