import os
import csv
import unicodedata
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QMessageBox,
    QListWidget, QLabel, QPlainTextEdit, QPushButton
)
from qgis.core import (
    QgsVectorLayer, QgsProject, QgsPalLayerSettings,
    QgsVectorLayerSimpleLabeling, QgsMarkerSymbol,
    QgsProperty, QgsSymbolLayer
)
from .GUI import Ui_MainWindow
from .pdf_creator import PDFCreator
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class Menu_Function:
    """画像リスト管理とEXIF/GPS取得機能を提供するクラス"""

    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas() if iface else None
        self.image_data = []  # {'file_name', 'text', 'number'} の辞書リスト
        self.current_index = -1

    def get_exif_data(self, image_path):
        """画像からEXIFデータを抽出し、辞書で返却"""
        try:
            with Image.open(image_path) as img:
                exif = img._getexif()
                return None if not exif else {TAGS.get(k, k): v for k, v in exif.items()}
        except Exception as e:
            print(f"EXIF取得エラー({image_path}): {e}")
            return None

    def get_gps_info(self, exif_data):
        """EXIFから緯度・経度・方位を計算して返却"""
        gps = exif_data.get("GPSInfo", {}) if exif_data else {}
        if not gps:
            return None, None, None

        def to_deg(vals):
            def rat2f(r):
                try:
                    return float(r)
                except:
                    return r.numerator / r.denominator
            d, m, s = vals
            return rat2f(d) + rat2f(m)/60 + rat2f(s)/3600

        lat = lon = dir_ = None
        for k, v in gps.items():
            key = GPSTAGS.get(k, k)
            if key == "GPSLatitude":
                lat = to_deg(v) * (-1 if gps.get(1) == "S" else 1)
            elif key == "GPSLongitude":
                lon = to_deg(v) * (-1 if gps.get(3) == "W" else 1)
            elif key == "GPSImgDirection":
                dir_ = v
        return lat, lon, dir_

    def update_image_list(self, directory):
        """ディレクトリ内の画像ファイル一覧を読み込む"""
        self.image_data.clear()
        files = [f for f in os.listdir(directory)
                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        for i, fn in enumerate(files, start=1):
            self.image_data.append({'file_name': fn, 'text': '', 'number': i})
        self.current_index = 0 if self.image_data else -1

    def save_current_text(self, text):
        """現在のインデックスに対応するテキストを保存"""
        idx = self.current_index
        if 0 <= idx < len(self.image_data):
            self.image_data[idx]['text'] = text

    def prepare_csv_data(self, directory):
        """CSV出力用データを作成して返却"""
        data = []
        for idx, info in enumerate(self.image_data, start=1):
            path = os.path.join(directory, info['file_name'])
            exif = self.get_exif_data(path) or {}
            lat, lon, dir_ = self.get_gps_info(exif)
            data.append([
                idx, info['file_name'],
                lat if lat is not None else 'N/A',
                lon if lon is not None else 'N/A',
                dir_ if dir_ is not None else 'N/A'
            ])
        return data

    def load_csv_to_qgis(self, csv_file):
        """CSVを読み込み、QGISにポイントレイヤとして追加"""
        headers = ["番号", "ファイル名", "緯度", "経度", "撮影方位"]
        try:
            with open(csv_file, encoding='utf-8') as f:
                reader = csv.reader(f)
                if next(reader)[:5] != headers:
                    return False, f"ヘッダー不正: {headers}"
        except Exception as e:
            return False, f"CSV読込エラー: {e}"

        uri = f"file:///{csv_file}?delimiter=,&xField=経度&yField=緯度&crs=EPSG:4326"
        layer = QgsVectorLayer(uri, os.path.splitext(os.path.basename(csv_file))[0], 'delimitedtext')
        if not layer.isValid():
            return False, 'レイヤ作成失敗'

        QgsProject.instance().addMapLayer(layer)
        sym = QgsMarkerSymbol.createSimple({'name': 'triangle', 'color': 'red', 'size': '3'})
        if sym.symbolLayerCount():
            sl = sym.symbolLayer(0)
            if isinstance(sl, QgsSymbolLayer):
                sl.setDataDefinedProperty(QgsSymbolLayer.PropertyAngle,
                                          QgsProperty.fromExpression('"撮影方位"'))
        layer.renderer().setSymbol(sym)
        layer.triggerRepaint()

        settings = QgsPalLayerSettings()
        settings.fieldName = '番号'
        settings.enabled = True
        layer.setLabeling(QgsVectorLayerSimpleLabeling(settings))
        layer.setLabelsEnabled(True)

        return True, 'QGISにレイヤ追加完了'


class Menu_Dialog(QMainWindow, Ui_MainWindow):
    """メインダイアログの動作を定義するクラス"""

    def __init__(self, iface, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.menu_function = Menu_Function(iface)

        # ボタンのスタイル設定
        btn_style = 'QPushButton {background:lightgray;} QPushButton:hover {background:lightblue;}'
        for btn in [self.pushButton, self.pushButton_2, self.pushButton_3,
                    self.pushButton_4, self.pushButton_5, self.pushButton_6,
                    self.pushButton_7, getattr(self, 'pushButton_8', None)]:
            if btn:
                btn.setStyleSheet(btn_style)

        # lineEdit_2, lineEdit_4 の設定
        for le in (self.lineEdit_2, self.lineEdit_4):
            le.setAlignment(Qt.AlignCenter)
            le.setReadOnly(True)

        # 画像表示エリアの初期化
        self.label.setAlignment(Qt.AlignCenter)
        self.display_empty_image()

        # シグナル接続
        self.pushButton.clicked.connect(self.on_select_path)
        self.pushButton_2.clicked.connect(self.on_load_csv_to_qgis)
        self.pushButton_3.clicked.connect(self.on_reset_and_update_images)
        self.pushButton_4.clicked.connect(self.on_save_csv)
        self.pushButton_5.clicked.connect(self.on_show_next_image)
        self.pushButton_6.clicked.connect(self.on_show_previous_image)
        self.pushButton_7.clicked.connect(self.on_create_pdf)
        self.pushButton_8.clicked.connect(self.on_rotate_image)
        self.listWidget.itemSelectionChanged.connect(self.on_list_selection_changed)

    def on_list_selection_changed(self):
        # リスト選択変更時にテキストを保存して表示を更新
        self.save_current_text()
        self.display_selected_image()

    def on_select_path(self):
        # ディレクトリ選択ダイアログを開き、画像一覧を更新
        d = QFileDialog.getExistingDirectory(self, "ディレクトリ選択", "")
        if not d:
            return
        self.lineEdit.setText(d)
        self.menu_function.update_image_list(d)
        self.update_list_widget()

    def on_reset_and_update_images(self):
        # 画像一覧とUIをリセットして再読み込み
        d = self.lineEdit.text()
        if not d:
            return
        self.menu_function.update_image_list(d)
        self.update_list_widget()
        self.textEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_4.clear()
        self.display_empty_image()

    def on_save_csv(self):
        # CSV保存処理
        d = self.lineEdit.text()
        data = self.menu_function.prepare_csv_data(d)
        if not data:
            QMessageBox.warning(self, "警告", "画像データがありません。")
            return
        opts = QFileDialog.Options()
        opts |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getSaveFileName(self, "CSV保存", "", "CSV (*.csv)", options=opts)
        if not path:
            return
        if not path.lower().endswith(".csv"):
            path += ".csv"
        try:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["番号", "ファイル名", "緯度", "経度", "撮影方位"])
                writer.writerows(data)
            QMessageBox.information(self, "成功", f"CSV保存: {path}")
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"保存失敗: {e}")

    def on_load_csv_to_qgis(self):
        # QGISにCSVをインポート
        opts = QFileDialog.Options()
        opts |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, "CSV選択", "", "CSV (*.csv)", options=opts)
        if not path:
            return
        ok, msg = self.menu_function.load_csv_to_qgis(path)
        if ok:
            QMessageBox.information(self, "成功", msg)
        else:
            QMessageBox.critical(self, "エラー", msg)

    def on_show_previous_image(self):
        # 前の画像に移動して表示更新
        self.save_current_text()
        ni = max(self.menu_function.current_index - 1, 0)
        if ni == self.menu_function.current_index:
            QMessageBox.warning(self, "警告", "これ以上前はありません。")
            return
        self.menu_function.current_index = ni
        self.listWidget.blockSignals(True)
        self.listWidget.setCurrentRow(ni)
        self.listWidget.blockSignals(False)
        self.display_selected_image()

    def on_show_next_image(self):
        # 次の画像に移動して表示更新
        self.save_current_text()
        ni = min(self.menu_function.current_index + 1, len(self.menu_function.image_data) - 1)
        if ni == self.menu_function.current_index:
            QMessageBox.warning(self, "警告", "これ以上次はありません。")
            return
        self.menu_function.current_index = ni
        self.listWidget.blockSignals(True)
        self.listWidget.setCurrentRow(ni)
        self.listWidget.blockSignals(False)
        self.display_selected_image()

    def on_create_pdf(self):
        # PDF作成処理
        self.save_current_text()
        d = self.lineEdit.text()
        paths, texts = [], []
        for info in self.menu_function.image_data:
            p = os.path.join(d, info['file_name'])
            if os.path.exists(p):
                paths.append(p)
                texts.append(f"{info['file_name']}, {info['text']}")
        if not paths:
            QMessageBox.warning(self, "警告", "有効な画像がありません。")
            return

        # 4行超え警告
        for info in self.menu_function.image_data:
            if len(self.force_wrap_text(info['text']).splitlines()) >= 4:
                ans = QMessageBox.question(self, "警告", "4行超があります。続行？",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if ans == QMessageBox.No:
                    return
                break

        file, _ = QFileDialog.getSaveFileName(self, "PDF保存", "", "PDF (*.pdf)")
        if not file:
            return
        if not file.lower().endswith('.pdf'):
            file += '.pdf'

        ok, msg = PDFCreator.create_pdf(paths, file, texts)
        if ok:
            QMessageBox.information(self, "成功", msg)
        else:
            QMessageBox.critical(self, "エラー", msg)

    def update_list_widget(self):
        # リストウィジェットを更新
        self.listWidget.clear()
        for info in self.menu_function.image_data:
            self.listWidget.addItem(info['file_name'])
        if self.menu_function.image_data:
            self.listWidget.setCurrentRow(self.menu_function.current_index)
        else:
            self.display_empty_image()

    def save_current_text(self):
        # テキスト保存ヘルパー
        txt = self.textEdit.toPlainText()
        self.menu_function.save_current_text(txt)

    def display_selected_image(self):
        # 選択中の画像とテキストを表示
        items = self.listWidget.selectedItems()
        if not items:
            return self.display_empty_image()
        row = self.listWidget.currentRow()
        self.menu_function.current_index = row
        info = self.menu_function.image_data[row]
        self.textEdit.setPlainText(info['text'])
        self.lineEdit_2.setText(str(info['number']))
        self.lineEdit_4.setText(info['file_name'])
        pix = QPixmap(os.path.join(self.lineEdit.text(), info['file_name']))
        if pix.isNull():
            self.label.setText("画像読み込み失敗")
        else:
            self.label.setPixmap(pix.scaled(self.label.width(), self.label.height(),Qt.KeepAspectRatio,Qt.SmoothTransformation))

    def display_empty_image(self):
        # 空画像を表示
        img = QImage(self.label.size(), QImage.Format_RGB32)
        img.fill(Qt.white)
        self.label.setPixmap(QPixmap.fromImage(img))

    def force_wrap_text(self, text, max_width=36.5):
        # 強制改行ロジック
        lines = []
        for para in text.splitlines():
            cur, w = '', 0
            for c in para:
                cw = 0.5 if unicodedata.east_asian_width(c) in 'NaH' else 1
                if w + cw > max_width:
                    lines.append(cur)
                    cur, w = c, cw
                else:
                    cur, w = cur + c, w + cw
            lines.append(cur)
        return '\n'.join(lines)

    def on_rotate_image(self):
        # 画像を180度回転して保存・再表示
        idx = self.menu_function.current_index
        if idx < 0:
            QMessageBox.warning(self, "警告", "選択された画像がありません。")
            return
        fn = self.menu_function.image_data[idx]['file_name']
        path = os.path.join(self.lineEdit.text(), fn)
        if not os.path.exists(path):
            QMessageBox.critical(self, "エラー", f"ファイルがありません: {path}")
            return
        try:
            with Image.open(path) as img:
                img.rotate(180, expand=True).save(path)
            QMessageBox.information(self, "成功", f"{fn} を回転しました")
            self.display_selected_image()
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"回転中エラー: {e}")
