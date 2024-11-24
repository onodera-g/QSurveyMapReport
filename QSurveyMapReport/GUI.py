# GUI.py
# GUIの構成を実装している
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # ウィンドウサイズ
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(860, 635)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # path選択ボタン
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(750, 20, 75, 20))
        self.pushButton.setStyleSheet("border: 1px solid black;")
        self.pushButton.setObjectName("pushButton")
        # make csv ボタン
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(750, 540, 75, 20))
        self.pushButton_4.setStyleSheet("border: 1px solid black;")
        self.pushButton_4.setObjectName("pushButton_4")
        # make pdfボタン
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(750, 590, 75, 20))
        self.pushButton_7.setStyleSheet("border: 1px solid black;")
        self.pushButton_7.setObjectName("pushButton_7")
        # ◀ ボタン
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(570, 540, 75, 20))
        self.pushButton_6.setStyleSheet("border: 1px solid black;")
        self.pushButton_6.setObjectName("pushButton_6")
        # ▶ ボタン
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(660, 540, 75, 20))
        self.pushButton_5.setStyleSheet("border: 1px solid black;")
        self.pushButton_5.setObjectName("pushButton_5")
        # input mapボタン
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(660, 590, 75, 20))
        self.pushButton_2.setStyleSheet("border: 1px solid black;")
        self.pushButton_2.setObjectName("pushButton_2")
        # update list ボタン
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 540, 75, 23))
        self.pushButton_3.setStyleSheet("border: 1px solid black;")
        self.pushButton_3.setObjectName("pushButton_3")

        # pathの表示ボックス
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 20, 715, 20))
        self.lineEdit.setObjectName("lineEdit")
        # 写真の一覧表示ボックス
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 70, 256, 461))
        self.listWidget.setStyleSheet("border: 1px solid black;")
        self.listWidget.setObjectName("listWidget")
        # 写真の表示ボックス
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 70, 525, 290))
        self.label.setStyleSheet("border: 1px solid black;")
        self.label.setObjectName("label")
        # 写真番号ボックス
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(300, 370, 525, 20))
        self.lineEdit_2.setStyleSheet("border: 1px solid black;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        # テキスト入力ボックス
        self.textEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(300, 430, 540, 100))
        self.textEdit.setStyleSheet("border: 1px solid black;")
        self.textEdit.setObjectName("textEdit")
        # 写真ファイル名表示ボックス
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(300, 400, 525, 20))
        self.lineEdit_4.setStyleSheet("border: 1px solid black;")
        self.lineEdit_4.setObjectName("lineEdit_4")

        # 等幅フォントに設定（MSゴシック）
        font = QtGui.QFont("MS Gothic", 10)
        font.setStyleHint(QtGui.QFont.Monospace)
        self.textEdit.setFont(font)

        # フォントメトリクスを使用して1文字の幅を取得
        font_metrics = QtGui.QFontMetrics(font)
        char_width = font_metrics.horizontalAdvance('M')  # 'M' は幅の広い文字として使用
        wrap_width = char_width * 72  # 74全角文字分の幅を計算

        # QPlainTextEdit の改行設定を行う
        self.textEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        # ウィジェットの幅を74全角文字分に設定
        total_wrap_width = wrap_width + 20  # フレーム幅やマージンを考慮して調整
        self.textEdit.setFixedWidth(total_wrap_width)

        # 水平スクロールバーを非表示に設定
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
