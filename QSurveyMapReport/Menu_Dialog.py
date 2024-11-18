from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtCore import QPropertyAnimation, QRect
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
from qgis.gui import *
from PyQt5 import uic, QtWidgets, QtCore

import os

from .GUI import Ui_MainWindow

QString = str

# 文字コード変換用
try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class Menu_Function:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        # GUIの表示
        self.dlg = Menu_Dialog()
        # ボタン接続
        self.dlg.pushButton.clicked.connect(self.func_select_path)
        self.dlg.pushButton_5.clicked.connect(self.show_previous_image)
        self.dlg.pushButton_6.clicked.connect(self.show_next_image)
        # listWidget の選択変更時に display_selected_image を呼び出す
        self.dlg.listWidget.itemSelectionChanged.connect(
            self.display_selected_image)
        # データ管理リスト
        self.image_data = []
        self.current_index = -1

        # ボタンにスタイルシートを設定
        self.dlg.pushButton.setStyleSheet("""
            QPushButton {
                background-color: lightgray;  /* 通常時の背景色 */
            }
            QPushButton:hover {
                background-color: lightblue;  /* ホバー時の背景色 */
            }
        """)
        self.dlg.pushButton_5.setStyleSheet("""
            QPushButton {
                background-color: lightgray;
            }
            QPushButton:hover {
                background-color: lightgreen;
            }
        """)
        self.dlg.pushButton_6.setStyleSheet("""
            QPushButton {
                background-color: lightgray;
            }
            QPushButton:hover {
                background-color: lightpink;
            }
        """)

    def func_select_path(self):
        directory = QFileDialog.getExistingDirectory(
            self.dlg, "ディレクトリを選択してください", "")
        if directory:
            self.dlg.lineEdit.setText(directory)
            self.update_image_list(directory)

    def update_image_list(self, directory):
        self.dlg.listWidget.clear()
        self.image_data.clear()
        files = [f for f in os.listdir(
            directory) if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
        for index, file_name in enumerate(files):
            self.dlg.listWidget.addItem(file_name)
            self.image_data.append(
                {"file_name": file_name, "text": "", "number": index + 1})
        if self.image_data:
            self.current_index = 0
            self.dlg.listWidget.setCurrentRow(0)

    def save_current_text(self):
        if self.current_index >= 0 and self.current_index < len(self.image_data):
            self.image_data[self.current_index]["text"] = self.dlg.lineEdit_3.text()

    def show_previous_image(self):
        self.save_current_text()
        current_row = self.dlg.listWidget.currentRow()
        if current_row > 0:
            self.dlg.listWidget.setCurrentRow(current_row - 1)

    def show_next_image(self):
        self.save_current_text()
        current_row = self.dlg.listWidget.currentRow()
        if current_row < self.dlg.listWidget.count() - 1:
            self.dlg.listWidget.setCurrentRow(current_row + 1)

    def display_selected_image(self):
        self.save_current_text()
        selected_items = self.dlg.listWidget.selectedItems()
        if selected_items:
            selected_file = selected_items[0].text()
            directory = self.dlg.lineEdit.text()
            file_path = os.path.join(directory, selected_file)
            self.current_index = self.dlg.listWidget.currentRow()
            if self.current_index >= 0 and self.current_index < len(self.image_data):
                self.dlg.lineEdit_3.setText(
                    self.image_data[self.current_index]["text"])
                self.dlg.lineEdit_2.setText(
                    str(self.image_data[self.current_index]["number"]))
                self.dlg.lineEdit_2.setReadOnly(True)
                self.dlg.lineEdit_4.setText(
                    self.image_data[self.current_index]["file_name"])
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(self.dlg.label.width(), self.dlg.label.height(),
                                              Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.dlg.label.setPixmap(scaled_pixmap)
            else:
                self.dlg.label.setText("画像の読み込みに失敗しました")
        else:
            self.display_empty_image()

    def display_empty_image(self):
        blank_image = QImage(self.dlg.label.size(), QImage.Format_RGB32)
        blank_image.fill(Qt.white)
        self.dlg.label.setPixmap(QPixmap.fromImage(blank_image))


class Menu_Dialog(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Menu_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.listWidget.itemSelectionChanged.connect(
            self.display_selected_image)
        self.label.setAlignment(Qt.AlignCenter)
        self.display_empty_image()

    def display_selected_image(self):
        selected_items = self.listWidget.selectedItems()
        if selected_items:
            selected_file = selected_items[0].text()
            directory = self.lineEdit.text()
            file_path = os.path.join(directory, selected_file)
            index = self.listWidget.row(selected_items[0])
            self.lineEdit_2.setText(f"{index + 1}")
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(self.label.width(), self.label.height(),
                                              Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.label.setPixmap(scaled_pixmap)
            else:
                self.label.setText("画像の読み込みに失敗しました")
        else:
            self.display_empty_image()

    def display_empty_image(self):
        blank_image = QImage(self.label.size(), QImage.Format_RGB32)
        blank_image.fill(Qt.white)
        self.label.setPixmap(QPixmap.fromImage(blank_image))


class Menu_Dialog(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Menu_Dialog, self).__init__(parent)
        self.setupUi(self)
        # listWidget の項目が選択されたときに display_selected_image メソッドを呼び出す
        self.listWidget.itemSelectionChanged.connect(
            self.display_selected_image)
        # QLabel の中央揃えを設定
        self.label.setAlignment(Qt.AlignCenter)
        self.display_empty_image()  # 選択がない場合も空白の画像を表示

    # 選択された写真を表示する
    def display_selected_image(self):
        # listWidget で選択されている文字列(ファイル名)を取得
        selected_items = self.listWidget.selectedItems()
        #  selected_items が空でない
        if selected_items:
            selected_file = selected_items[0].text()  # 選択されたアイテムのファイル名を取得
            directory = self.lineEdit.text()  # 現在のディレクトリパスを　lineEdit　から取得
            file_path = os.path.join(directory, selected_file)  # フルパスを作成

            # 画像のインデックスを取得し、lineEdit_2 に表示
            index = self.listWidget.row(selected_items[0])
            self.lineEdit_2.setText(f"{index + 1}")  # 1から始まる番号で表示

            pixmap = QPixmap(file_path)  # 画像をロード
            if not pixmap.isNull():  # 画像が有効な場合
                # QLabel のサイズを取得し、画像をそのサイズ内でスケーリング
                scaled_pixmap = pixmap.scaled(self.label.width(), self.label.height(),
                                              Qt.KeepAspectRatio, Qt.SmoothTransformation)
                # ピクセルマップを中央揃えで設定
                self.label.setPixmap(scaled_pixmap)
            else:
                self.label.setText("画像の読み込みに失敗しました")  # 無効な画像の場合のメッセージ
        else:
            self.display_empty_image()  # 選択がない場合も空白の画像を表示

    # 　真っ白な画像を表示
    def display_empty_image(self):
        # 真っ白な画像を生成して QLabel に設定
        blank_image = QImage(self.label.size(), QImage.Format_RGB32)
        blank_image.fill(Qt.white)  # 白色で塗りつぶす
        self.label.setPixmap(QPixmap.fromImage(blank_image))
