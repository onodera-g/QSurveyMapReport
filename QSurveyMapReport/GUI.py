# GUI.py
# GUIの構成を実装している
import os
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

        # **180度回転ボタンの追加**
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(
            QtCore.QRect(480, 540, 75, 75))  # サイズを大きく設定
        self.pushButton_8.setStyleSheet("border: 1px solid black;")
        self.pushButton_8.setObjectName("pushButton_8")

        # アイコンの設定
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # 180度回転アイコンの設定
        rotate_icon_path = os.path.join(script_dir, "rotate_180_icon.png")
        print(f"Icon path: {rotate_icon_path}")  # デバッグ用

        if os.path.exists(rotate_icon_path):
            rotate_icon = QtGui.QIcon(rotate_icon_path)
            if not rotate_icon.isNull():
                self.pushButton_8.setIcon(rotate_icon)
                self.pushButton_8.setIconSize(
                    QtCore.QSize(24, 24))  # アイコンのサイズを調整
                self.pushButton_8.setText("")  # ボタンテキストを非表示にする
                print("Rotate 180° icon loaded successfully.")
            else:
                print(
                    f"Icon at {rotate_icon_path} is null. Please check the image file.")
        else:
            print(f"Icon file not found at {rotate_icon_path}")

        # **複数のボタンにアイコンを設定する**
        # ボタン名と対応するアイコンファイル名の辞書
        button_icon_mapping = {
            "pushButton_2": "map.png",
            "pushButton_3": "update.png",
            "pushButton_4": "csv.png",
            "pushButton_5": "right.png",
            "pushButton_6": "left.png",
            "pushButton_7": "pdf.png",
        }

        # 各ボタンに対してアイコンを設定
        for button_name, icon_filename in button_icon_mapping.items():
            button = getattr(self, button_name, None)
            if button is not None:
                icon_path = os.path.join(script_dir, icon_filename)
                if os.path.exists(icon_path):
                    icon = QtGui.QIcon(icon_path)
                    if not icon.isNull():
                        button.setIcon(icon)
                        button.setIconSize(QtCore.QSize(15, 15))  # アイコンサイズ調整
                        button.setText("")  # テキストを非表示
                        print(f"{button_name} に {icon_filename} を設定しました。")
                    else:
                        print(
                            f"Icon at {icon_path} is null. Please check the image file.")
                else:
                    print(f"Icon file not found at {icon_path}")
            else:
                print(f"Button {button_name} が存在しません。")

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
        wrap_width = char_width * 72  # 72全角文字分の幅を計算

        # QPlainTextEdit の改行設定を行う
        self.textEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        # ウィジェットの幅を72全角文字分に設定
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
        MainWindow.setWindowTitle(_translate("MainWindow", "QSurveyMapReport"))
        self.pushButton.setText(_translate("MainWindow", "......"))
        self.pushButton_2.setText("input map ")  # アイコンのみ表示するためテキストを空に
        self.pushButton_3.setText("")  # アイコンのみ表示するためテキストを空に
        self.pushButton_4.setText("make csv ")  # アイコンのみ表示するためテキストを空に
        self.pushButton_5.setText("")  # アイコンのみ表示するためテキストを空に
        self.pushButton_6.setText("")  # アイコンのみ表示するためテキストを空に
        self.pushButton_7.setText("make pdf ")  # アイコンのみ表示するためテキストを空に
        self.label.setText(_translate("MainWindow", "TextLabel"))
        # 180度回転ボタンのテキストを非表示にしてアイコンのみにする
        self.pushButton_8.setText("")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
