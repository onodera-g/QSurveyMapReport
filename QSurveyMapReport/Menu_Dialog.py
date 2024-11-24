# Menu_Dialog.py

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (
    QPushButton, QApplication, QMainWindow,
    QFileDialog, QLabel, QListWidget, QPlainTextEdit, QMessageBox
)
from qgis.core import (
    QgsVectorLayer, QgsProject, QgsPalLayerSettings,
    QgsVectorLayerSimpleLabeling, QgsMarkerSymbol, QgsProperty, QgsSymbolLayer
)
from qgis.gui import *
from PyQt5 import uic, QtWidgets

import os
import csv
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from .GUI import Ui_MainWindow  # 既存のGUIファイルをインポート
from .pdf_creator import PDFCreator
import unicodedata


QString = str


class Menu_Function:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas() if self.iface else None
        self.image_data = []
        self.current_index = -1

    # EXIFデータを取得する関数
    def get_exif_data(self, image_path):
        try:
            with Image.open(image_path) as image:
                exif_data = image._getexif()
                if not exif_data:
                    return None
                exif_dict = {}
                for tag, value in exif_data.items():
                    decoded_tag = TAGS.get(tag, tag)
                    exif_dict[decoded_tag] = value
                return exif_dict
        except Exception as e:
            print(f"EXIFデータの取得中にエラーが発生しました ({image_path}): {e}")
            return None

    # GPS情報を取得する関数
    def get_gps_info(self, exif_data):
        gps_info = exif_data.get("GPSInfo", None)
        if not gps_info:
            return None, None, None

        lat, lon, direction = None, None, None

        def convert_to_degrees(value):
            d, m, s = value

            def rational_to_float(rational):
                try:
                    return float(rational)
                except TypeError:
                    return float(rational.numerator) / float(rational.denominator)
            d = rational_to_float(d)
            m = rational_to_float(m)
            s = rational_to_float(s)
            return d + (m / 60.0) + (s / 3600.0)

        for key in gps_info.keys():
            decoded_key = GPSTAGS.get(key, key)
            if decoded_key == "GPSLatitude":
                lat = convert_to_degrees(gps_info[key])
                if gps_info.get("GPSLatitudeRef") == "S":
                    lat = -lat
            elif decoded_key == "GPSLongitude":
                lon = convert_to_degrees(gps_info[key])
                if gps_info.get("GPSLongitudeRef") == "W":
                    lon = -lon
            elif decoded_key == "GPSImgDirection":
                direction = gps_info[key]

        return lat, lon, direction

    # 画像一覧を更新
    def update_image_list(self, directory):
        self.image_data.clear()
        files = [f for f in os.listdir(
            directory) if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
        for index, file_name in enumerate(files):
            self.image_data.append(
                {"file_name": file_name, "text": "", "number": index + 1})
        if self.image_data:
            self.current_index = 0
        else:
            self.current_index = -1

    # 現在のテキストを保存
    def save_current_text(self, text):
        if self.current_index >= 0 and self.current_index < len(self.image_data):
            self.image_data[self.current_index]["text"] = text

    # CSVファイルの作成
    def prepare_csv_data(self, directory):
        output_data = []
        supported_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
        for index, image_info in enumerate(self.image_data, start=1):
            file_name = image_info.get("file_name")
            if not file_name.lower().endswith(supported_extensions):
                continue  # サポートされていないファイル形式はスキップ
            image_path = os.path.join(directory, file_name)
            exif_data = self.get_exif_data(image_path)
            if exif_data:
                lat, lon, direction = self.get_gps_info(exif_data)
            else:
                lat, lon, direction = None, None, None
            output_data.append([
                index,
                file_name,
                lat if lat is not None else "N/A",
                lon if lon is not None else "N/A",
                direction if direction is not None else "N/A"
            ])
        return output_data

    # CSVをポイントデータとしてレイヤに追加
    def load_csv_to_qgis(self, csv_file):
        required_headers = ["番号", "ファイル名", "緯度", "経度", "撮影方位"]
        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)
                if headers[:5] != required_headers:
                    return False, f"CSVファイルのヘッダーが正しくありません。\n必要なヘッダー: {', '.join(required_headers)}"
        except Exception as e:
            return False, f"CSVファイルの読み込み中にエラーが発生しました:\n{e}"

        try:
            uri = f"file:///{csv_file}?delimiter=,&xField=経度&yField=緯度&crs=EPSG:4326"
            layer_name = os.path.splitext(os.path.basename(csv_file))[0]
            csv_layer = QgsVectorLayer(uri, layer_name, "delimitedtext")
            if not csv_layer.isValid():
                return False, "CSVファイルからレイヤを作成できませんでした。"

            QgsProject.instance().addMapLayer(csv_layer)

            symbol = QgsMarkerSymbol.createSimple(
                {'name': 'triangle', 'color': 'red', 'size': '3'})
            if symbol.symbolLayerCount() > 0:
                symbol_layer = symbol.symbolLayer(0)
                if isinstance(symbol_layer, QgsSymbolLayer):
                    rotation_property = QgsProperty.fromExpression('"撮影方位"')
                    symbol_layer.setDataDefinedProperty(
                        QgsSymbolLayer.PropertyAngle, rotation_property)
                else:
                    return False, "シンボルレイヤーがサポートされていません。回転を設定できません。"
            else:
                return False, "シンボルにシンボルレイヤーが含まれていません。回転を設定できません。"

            csv_layer.renderer().setSymbol(symbol)
            csv_layer.triggerRepaint()

            labeling = QgsPalLayerSettings()
            labeling.fieldName = "番号"
            labeling.enabled = True
            csv_layer.setLabeling(QgsVectorLayerSimpleLabeling(labeling))
            csv_layer.setLabelsEnabled(True)

            return True, f"CSVファイルがレイヤとしてQGISに追加されました: {layer_name}"
        except Exception as e:
            return False, f"CSVファイルをQGISに追加する際にエラーが発生しました:\n{e}"


class Menu_Dialog(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, iface, parent=None):
        super(Menu_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.menu_function = Menu_Function(iface)

        # ボタンにスタイルシートを設定
        button_styles = """
            QPushButton {
                background-color: lightgray;  /* 通常時の背景色 */
            }
            QPushButton:hover {
                background-color: lightblue;  /* ホバー時の背景色 */
            }
        """
        for btn in [
            self.pushButton, self.pushButton_2, self.pushButton_3,
            self.pushButton_4, self.pushButton_5, self.pushButton_6,
            getattr(self, 'pushButton_7', None)  # pushButton_7が存在する場合
        ]:
            if btn:
                btn.setStyleSheet(button_styles)

        # lineEdit_2とlineEdit_4の設定
        self.lineEdit_2.setAlignment(Qt.AlignCenter)  # 中央揃え
        self.lineEdit_2.setReadOnly(True)  # 編集不可
        self.lineEdit_4.setAlignment(Qt.AlignCenter)  # 中央揃え
        self.lineEdit_4.setReadOnly(True)  # 編集不可

        # QLabel の中央揃えを設定
        self.label.setAlignment(Qt.AlignCenter)
        self.display_empty_image()  # 初期表示

        # シグナル接続
        self.pushButton.clicked.connect(self.on_select_path)
        self.pushButton_2.clicked.connect(self.on_load_csv_to_qgis)
        self.pushButton_3.clicked.connect(self.on_reset_and_update_images)
        self.pushButton_4.clicked.connect(self.on_save_csv)
        self.pushButton_5.clicked.connect(self.on_show_next_image)
        self.pushButton_6.clicked.connect(self.on_show_previous_image)
        self.pushButton_7.clicked.connect(self.on_create_pdf)

        # listWidget の選択変更時に display_selected_image を呼び出す
        self.listWidget.itemSelectionChanged.connect(
            self.display_selected_image)

    # ボタン押下時のスロット
    def on_select_path(self):
        directory = QFileDialog.getExistingDirectory(
            self, "ディレクトリを選択してください", "")
        if directory:
            self.lineEdit.setText(directory)
            self.menu_function.update_image_list(directory)
            self.update_list_widget()

    def on_save_csv(self):
        directory = self.lineEdit.text()
        if not directory:
            QMessageBox.warning(self, "警告", "画像が存在するディレクトリが指定されていません。")
            return

        output_data = self.menu_function.prepare_csv_data(directory)
        if not output_data:
            QMessageBox.warning(self, "警告", "画像データがありません。")
            return

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        csv_file, _ = QFileDialog.getSaveFileName(
            self, "CSVファイルを保存", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if not csv_file:
            return  # ユーザーがキャンセルした場合

        # ファイル名に拡張子が含まれていない場合、'.csv' を追加
        if not os.path.splitext(csv_file)[1].lower() == '.csv':
            csv_file += '.csv'

        try:
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["番号", "ファイル名", "緯度", "経度", "撮影方位"])
                writer.writerows(output_data)
            QMessageBox.information(
                self, "成功", f"CSVファイルが保存されました:\n{csv_file}")
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"CSVファイルの保存中にエラーが発生しました:\n{e}")

    def on_reset_and_update_images(self):
        directory = self.lineEdit.text()
        if directory:
            self.menu_function.update_image_list(directory)
            self.update_list_widget()
            # テキストのリセット
            self.textEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_4.clear()
            self.display_empty_image()  # 空の画像を表示

    def on_load_csv_to_qgis(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        csv_file, _ = QFileDialog.getOpenFileName(
            self, "CSVファイルを選択", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if not csv_file:
            return  # ユーザーがキャンセルした場合

        success, message = self.menu_function.load_csv_to_qgis(csv_file)
        if success:
            QMessageBox.information(self, "成功", message)
        else:
            QMessageBox.critical(self, "エラー", message)

    def on_show_previous_image(self):
        self.save_current_text()
        self.menu_function.current_index -= 1
        if self.menu_function.current_index < 0:
            self.menu_function.current_index = 0
            QMessageBox.warning(self, "警告", "これ以上前の画像はありません。")
        self.listWidget.setCurrentRow(self.menu_function.current_index)

    def on_show_next_image(self):
        self.save_current_text()
        self.menu_function.current_index += 1
        if self.menu_function.current_index >= len(self.menu_function.image_data):
            self.menu_function.current_index = len(
                self.menu_function.image_data) - 1
            QMessageBox.warning(self, "警告", "これ以上次の画像はありません。")
        self.listWidget.setCurrentRow(self.menu_function.current_index)

    def on_create_pdf(self):
        directory = self.lineEdit.text()
        if not directory:
            QMessageBox.warning(self, "警告", "画像が存在するディレクトリが指定されていません。")
            return

        image_paths = []
        data = []
        for image_info in self.menu_function.image_data:
            file_name = image_info.get("file_name")
            text = image_info.get("text", "")
            image_path = os.path.join(directory, file_name)
            if os.path.exists(image_path):
                image_paths.append(image_path)
                data.append(f"{file_name}, {text}")

        if not image_paths:
            QMessageBox.warning(self, "警告", "有効な画像がありません。")
            return

        pdf_file, _ = QFileDialog.getSaveFileName(
            self, "PDFファイルを保存", "", "PDF Files (*.pdf);;All Files (*)")
        if not pdf_file:
            return

        if not pdf_file.lower().endswith(".pdf"):
            pdf_file += ".pdf"

        success, message = PDFCreator.create_pdf(image_paths, pdf_file, data)
        if success:
            QMessageBox.information(self, "成功", message)
        else:
            QMessageBox.critical(self, "エラー", message)

    # リストウィジェットを更新
    def update_list_widget(self):
        self.listWidget.clear()
        for image_info in self.menu_function.image_data:
            self.listWidget.addItem(image_info["file_name"])
        if self.menu_function.image_data:
            self.listWidget.setCurrentRow(self.menu_function.current_index)
        else:
            self.display_empty_image()

    # 現在のテキストを保存
    def save_current_text(self):
        text = self.textEdit.toPlainText()  # QPlainTextEdit用に変更
        self.menu_function.save_current_text(text)

    # 選択した画像と付随する情報を表示
    def display_selected_image(self):
        selected_items = self.listWidget.selectedItems()
        if selected_items:
            selected_file = selected_items[0].text()
            directory = self.lineEdit.text()
            file_path = os.path.join(directory, selected_file)
            self.menu_function.current_index = self.listWidget.currentRow()

            # 画像番号、ファイル名、テキストの表示
            if 0 <= self.menu_function.current_index < len(self.menu_function.image_data):
                image_info = self.menu_function.image_data[self.menu_function.current_index]
                formatted_text = self.format_text_with_line_breaks(
                    image_info["text"])
                self.textEdit.setPlainText(
                    formatted_text)  # QPlainTextEdit用に変更
                self.lineEdit_2.setText(str(image_info["number"]))
                self.lineEdit_4.setText(image_info["file_name"])

            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.label.width(), self.label.height(),
                    Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.label.setPixmap(scaled_pixmap)
            else:
                self.label.setText("画像の読み込みに失敗しました")
        else:
            self.display_empty_image()

    # 真っ白な画像を表示
    def display_empty_image(self):
        blank_image = QImage(self.label.size(), QImage.Format_RGB32)
        blank_image.fill(Qt.white)
        self.label.setPixmap(QPixmap.fromImage(blank_image))

    def format_text_with_line_breaks(self, text, max_length=36):
        formatted_text = ""
        current_length = 0
        buffer = ""

        for char in text:
            char_width = 0.5 if unicodedata.east_asian_width(
                char) in "NaH" else 1
            if current_length + char_width > max_length:
                formatted_text += buffer
                buffer = ""
                current_length = 0
            buffer += char
            current_length += char_width

        formatted_text += buffer
        return formatted_text
