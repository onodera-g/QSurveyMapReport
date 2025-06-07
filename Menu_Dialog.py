import os
import csv
import unicodedata
from PyQt5.QtCore import Qt, QCoreApplication
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
    """Provides image list management and EXIF/GPS retrieval functionality"""

    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas() if iface else None
        # List of dicts: {'file_name': ..., 'text': ..., 'number': ...}
        self.image_data = []
        self.current_index = -1

    def get_exif_data(self, image_path):
        """Extracts EXIF data from image and returns it as a dict."""
        try:
            with Image.open(image_path) as img:
                exif = img._getexif()
                return None if not exif else {TAGS.get(k, k): v for k, v in exif.items()}
        except Exception as e:
            print(f"EXIF retrieval error ({image_path}): {e}")
            return None

    def get_gps_info(self, exif_data):
        """Calculates latitude, longitude, and direction from EXIF GPS info."""
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
            return rat2f(d) + rat2f(m) / 60 + rat2f(s) / 3600

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
        """Loads list of image files in the specified directory."""
        self.image_data.clear()
        files = [f for f in os.listdir(directory)
                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        for i, fn in enumerate(files, start=1):
            self.image_data.append({'file_name': fn, 'text': '', 'number': i})
        self.current_index = 0 if self.image_data else -1

    def save_current_text(self, text):
        """Saves the given text to the current image entry."""
        idx = self.current_index
        if 0 <= idx < len(self.image_data):
            self.image_data[idx]['text'] = text

    def prepare_csv_data(self, directory):
        """Creates and returns data for CSV export."""
        data = []
        for idx, info in enumerate(self.image_data, start=1):
            # For each image entry, compile CSV row
            lat, lon, dir_ = self.get_gps_info(
                self.get_exif_data(os.path.join(directory, info['file_name']))
            )
            data.append([
                info['number'],
                info['file_name'],
                lat if lat is not None else 'N/A',
                lon if lon is not None else 'N/A',
                dir_ if dir_ is not None else 'N/A'
            ])
        return data

    def load_csv_to_qgis(self, csv_file):
        """Loads a CSV as a point layer into QGIS."""
        headers = ["Number", "File Name", "Latitude", "Longitude", "Direction"]
        try:
            with open(csv_file, encoding='utf-8') as f:
                reader = csv.reader(f)
                if next(reader)[:5] != headers:
                    msg = QCoreApplication.translate(
                        "Menu_Dialog", "Invalid header:")
                    return False, f"{msg} {headers}"
        except Exception as e:
            msg = QCoreApplication.translate("Menu_Dialog", "CSV load error:")
            return False, f"{msg} {e}"

        uri = (
            f"file:///{csv_file}"
            "?delimiter=,&xField=Longitude&yField=Latitude&crs=EPSG:4326"
        )
        layer = QgsVectorLayer(
            uri,
            os.path.splitext(os.path.basename(csv_file))[0],
            'delimitedtext'
        )
        if not layer.isValid():
            msg = QCoreApplication.translate(
                "Menu_Dialog", "Layer creation failed")
            return False, msg

        QgsProject.instance().addMapLayer(layer)

        sym = QgsMarkerSymbol.createSimple(
            {'name': 'triangle', 'color': 'red', 'size': '3'})
        if sym.symbolLayerCount():
            sl = sym.symbolLayer(0)
            if isinstance(sl, QgsSymbolLayer):
                sl.setDataDefinedProperty(
                    QgsSymbolLayer.PropertyAngle,
                    QgsProperty.fromExpression('"Direction"')
                )
        layer.renderer().setSymbol(sym)
        layer.triggerRepaint()

        settings = QgsPalLayerSettings()
        settings.fieldName = 'Number'
        settings.enabled = True
        layer.setLabeling(QgsVectorLayerSimpleLabeling(settings))
        layer.setLabelsEnabled(True)

        msg = QCoreApplication.translate("Menu_Dialog", "Layer added to QGIS")
        return True, msg


class Menu_Dialog(QMainWindow, Ui_MainWindow):
    """Defines the behavior of the main dialog."""

    def __init__(self, iface, parent=None):
        super().__init__(parent)

        # ─── UIをセットアップ（翻訳ファイルはプラグイン読み込み時に適用済み） ───
        self.setupUi(self)
        self.retranslateUi(self)
        # ───────────────────────────────────────────────────────────────

        self.iface = iface
        self.menu_function = Menu_Function(iface)

        # Button style settings
        btn_style = (
            'QPushButton {background:lightgray;} '
            'QPushButton:hover {background:lightblue;}'
        )
        for btn in [
            self.pushButton, self.pushButton_2, self.pushButton_3,
            self.pushButton_4, self.pushButton_5, self.pushButton_6,
            self.pushButton_7, getattr(self, 'pushButton_8', None)
        ]:
            if btn:
                btn.setStyleSheet(btn_style)

        # Configure lineEdit_2 and lineEdit_4
        for le in (self.lineEdit_2, self.lineEdit_4):
            le.setAlignment(Qt.AlignCenter)
            le.setReadOnly(True)

        # Initialize image display area
        self.label.setAlignment(Qt.AlignCenter)
        self.display_empty_image()

        # Connect signals to slots
        self.pushButton.clicked.connect(self.on_select_path)
        self.pushButton_2.clicked.connect(self.on_load_csv_to_qgis)
        self.pushButton_3.clicked.connect(self.on_reset_and_update_images)
        self.pushButton_4.clicked.connect(self.on_save_csv)
        self.pushButton_5.clicked.connect(self.on_show_next_image)
        self.pushButton_6.clicked.connect(self.on_show_previous_image)
        self.pushButton_7.clicked.connect(self.on_create_pdf)
        self.pushButton_8.clicked.connect(self.on_rotate_image)
        self.listWidget.itemSelectionChanged.connect(
            self.on_list_selection_changed)

    def tr(self, message):
        """Translation helper method for dialog strings."""
        return QCoreApplication.translate("Menu_Dialog", message)

    def on_list_selection_changed(self):
        # Save current text and update display when list selection changes
        self.save_current_text()
        self.display_selected_image()

    def on_select_path(self):
        # Open directory selection dialog and update image list
        d = QFileDialog.getExistingDirectory(
            self, self.tr("Select Directory"), "")
        if not d:
            return
        self.lineEdit.setText(d)
        self.menu_function.update_image_list(d)
        self.update_list_widget()

    def on_reset_and_update_images(self):
        # Reset image list and UI, then reload
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
        # CSV save process
        d = self.lineEdit.text()
        data = self.menu_function.prepare_csv_data(d)
        if not data:
            QMessageBox.warning(
                self, self.tr("Warning"), self.tr("No image data available.")
            )
            return

        # ※ ネイティブダイアログを使用するので、Opts 関連は不要
        path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Save CSV"),
            "",
            self.tr("CSV (*.csv)")
        )
        if not path:
            return
        if not path.lower().endswith(".csv"):
            path += ".csv"

        try:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    self.tr("Number"),
                    self.tr("File Name"),
                    self.tr("Latitude"),
                    self.tr("Longitude"),
                    self.tr("Direction")
                ])
                writer.writerows(data)
            QMessageBox.information(
                self,
                self.tr("Success"),
                self.tr("CSV saved.\n{0}").format(path)
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Error"),
                self.tr("Failed to save CSV.\n{0}").format(e)
            )

    def on_load_csv_to_qgis(self):
        # Import CSV into QGIS
        # ※ ネイティブダイアログを使用するので、Opts 関連は不要
        path, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Select CSV"),
            "",
            self.tr("CSV (*.csv)")
        )
        if not path:
            return
        ok, msg = self.menu_function.load_csv_to_qgis(path)
        if ok:
            QMessageBox.information(self, self.tr("Success"), msg)
        else:
            QMessageBox.critical(self, self.tr("Error"), msg)

    def on_show_previous_image(self):
        # Move to previous image and update display
        self.save_current_text()
        ni = max(self.menu_function.current_index - 1, 0)
        if ni == self.menu_function.current_index:
            QMessageBox.warning(
                self,
                self.tr("Warning"),
                self.tr("No previous images available.")
            )
            return
        self.menu_function.current_index = ni
        self.listWidget.blockSignals(True)
        self.listWidget.setCurrentRow(ni)
        self.listWidget.blockSignals(False)
        self.display_selected_image()

    def on_show_next_image(self):
        # Move to next image and update display
        self.save_current_text()
        ni = min(
            self.menu_function.current_index + 1,
            len(self.menu_function.image_data) - 1
        )
        if ni == self.menu_function.current_index:
            QMessageBox.warning(
                self,
                self.tr("Warning"),
                self.tr("No more images available.")
            )
            return
        self.menu_function.current_index = ni
        self.listWidget.blockSignals(True)
        self.listWidget.setCurrentRow(ni)
        self.listWidget.blockSignals(False)
        self.display_selected_image()

    def on_create_pdf(self):
        # PDF creation process
        self.save_current_text()
        d = self.lineEdit.text()
        paths, texts = [], []
        for info in self.menu_function.image_data:
            p = os.path.join(d, info['file_name'])
            if os.path.exists(p):
                paths.append(p)
                texts.append(f"{info['file_name']}, {info['text']}")
        if not paths:
            QMessageBox.warning(
                self, self.tr("Warning"), self.tr("No valid images.")
            )
            return

        # Warning if text exceeds 4 lines
        for info in self.menu_function.image_data:
            if len(self.force_wrap_text(info['text']).splitlines()) >= 4:
                ans = QMessageBox.question(
                    self,
                    self.tr("Warning"),
                    self.tr(
                        "Text exceeds 4 lines.\n"
                        "Text longer than 4 lines may disrupt PDF layout.\n"
                        "Continue?"
                    ),
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if ans == QMessageBox.No:
                    return
                break

        file, _ = QFileDialog.getSaveFileName(
            self, self.tr("Save PDF"), "", self.tr("PDF (*.pdf)")
        )
        if not file:
            return
        if not file.lower().endswith('.pdf'):
            file += '.pdf'

        ok, msg = PDFCreator.create_pdf(paths, file, texts)
        if ok:
            QMessageBox.information(self, self.tr("Success"), msg)
        else:
            QMessageBox.critical(self, self.tr("Error"), msg)

    def update_list_widget(self):
        # Update the list widget with current image files
        self.listWidget.clear()
        for info in self.menu_function.image_data:
            self.listWidget.addItem(info['file_name'])
        if self.menu_function.image_data:
            self.listWidget.setCurrentRow(self.menu_function.current_index)
        else:
            self.display_empty_image()

    def save_current_text(self):
        # Helper to save current text from textEdit
        txt = self.textEdit.toPlainText()
        self.menu_function.save_current_text(txt)

    def display_selected_image(self):
        # Display the currently selected image and its text
        items = self.listWidget.selectedItems()
        if not items:
            self.display_empty_image()
            return
        row = self.listWidget.currentRow()
        self.menu_function.current_index = row
        info = self.menu_function.image_data[row]
        self.textEdit.setPlainText(info['text'])
        self.lineEdit_2.setText(str(info['number']))
        self.lineEdit_4.setText(info['file_name'])
        pix = QPixmap(os.path.join(self.lineEdit.text(), info['file_name']))
        if pix.isNull():
            self.label.setText(self.tr("Failed to load image"))
        else:
            self.label.setPixmap(
                pix.scaled(
                    self.label.width(),
                    self.label.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

    def display_empty_image(self):
        # Display an empty (white) image in the label
        img = QImage(self.label.size(), QImage.Format_RGB32)
        img.fill(Qt.white)
        self.label.setPixmap(QPixmap.fromImage(img))

    def force_wrap_text(self, text, max_width=36.5):
        # Custom line-wrap logic: half-width char = 0.5, full-width char = 1 unit
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
        # Rotate the selected image 180 degrees and save/display
        idx = self.menu_function.current_index
        if idx < 0:
            QMessageBox.warning(
                self, self.tr("Warning"), self.tr("No image selected.")
            )
            return
        fn = self.menu_function.image_data[idx]['file_name']
        path = os.path.join(self.lineEdit.text(), fn)
        if not os.path.exists(path):
            QMessageBox.critical(
                self,
                self.tr("Error"),
                self.tr("File not found.\n{0}").format(path)
            )
            return
        try:
            with Image.open(path) as img:
                img.rotate(180, expand=True).save(path)
            QMessageBox.information(
                self,
                self.tr("Success"),
                self.tr("{0} rotated.").format(fn)
            )
            self.display_selected_image()
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Error"),
                self.tr("Rotation failed.\n{0}").format(e)
            )
