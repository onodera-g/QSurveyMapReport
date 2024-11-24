# GUI.py
# GUIの構成を実装している
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(785, 635)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 他のウィジェットの設定
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(690, 20, 75, 23))
        self.pushButton.setStyleSheet("border: 1px solid black;")
        self.pushButton.setObjectName("pushButton")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 20, 651, 20))
        self.lineEdit.setObjectName("lineEdit")

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 70, 256, 461))
        self.listWidget.setStyleSheet("border: 1px solid black;")
        self.listWidget.setObjectName("listWidget")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(590, 590, 75, 23))
        self.pushButton_2.setStyleSheet("border: 1px solid black;")
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 540, 75, 23))
        self.pushButton_3.setStyleSheet("border: 1px solid black;")
        self.pushButton_3.setObjectName("pushButton_3")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 70, 441, 291))
        self.label.setStyleSheet("border: 1px solid black;")
        self.label.setObjectName("label")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(300, 370, 441, 20))
        self.lineEdit_2.setStyleSheet("border: 1px solid black;")
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(300, 430, 441, 101))
        self.textEdit.setStyleSheet("border: 1px solid black;")
        self.textEdit.setObjectName("textEdit")

        # 等幅フォントに設定（例: Courier New）
        font = QtGui.QFont("Courier New", 10)
        font.setStyleHint(QtGui.QFont.Monospace)
        self.textEdit.setFont(font)

        # フォントメトリクスを使用して1文字の幅を取得
        font_metrics = QtGui.QFontMetrics(font)
        char_width = font_metrics.horizontalAdvance('M')  # 'M' は幅の広い文字として使用
        print(f"Character width: {char_width}")  # デバッグ用
        wrap_width = char_width * 36  # 36文字分の幅を計算
        print(f"Wrap width (36 chars): {wrap_width}")  # デバッグ用

        # QTextEdit の改行設定を行う
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.FixedPixelWidth)
        self.textEdit.document().setTextWidth(wrap_width)

        # QTextEdit のフレーム幅とマージンを考慮して幅を設定
        frame_width = self.textEdit.frameWidth() * 2
        document_margin = self.textEdit.document().documentMargin() * 2
        total_wrap_width = wrap_width + frame_width + document_margin
        print(f"Total wrap width: {total_wrap_width}")  # デバッグ用

        # ウィジェットの幅を36文字分に設定
        self.textEdit.setFixedWidth(total_wrap_width)

        # 水平スクロールバーを非表示に設定
        self.textEdit.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(670, 540, 75, 23))
        self.pushButton_4.setStyleSheet("border: 1px solid black;")
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(590, 540, 75, 23))
        self.pushButton_5.setStyleSheet("border: 1px solid black;")
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(510, 540, 75, 23))
        self.pushButton_6.setStyleSheet("border: 1px solid black;")
        self.pushButton_6.setObjectName("pushButton_6")

        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(300, 400, 441, 20))
        self.lineEdit_4.setStyleSheet("border: 1px solid black;")
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(670, 590, 75, 23))
        self.pushButton_7.setStyleSheet("border: 1px solid black;")
        self.pushButton_7.setObjectName("pushButton_7")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "QSurveyMapReport", "QSurveyMapReport"))
        self.pushButton.setText(_translate("MainWindow", "......"))
        self.pushButton_2.setText(_translate("MainWindow", "input map"))
        self.pushButton_3.setText(_translate("MainWindow", "update list"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton_4.setText(_translate("MainWindow", "make csv"))
        self.pushButton_5.setText(_translate("MainWindow", "▶"))
        self.pushButton_6.setText(_translate("MainWindow", "◀"))
        self.pushButton_7.setText(_translate("MainWindow", "make pdf"))
