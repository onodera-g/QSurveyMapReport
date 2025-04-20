from PyQt5.QtGui import QPdfWriter, QPainter, QPen, QImage, QFont
from PyQt5.QtCore import QSizeF, Qt, QRectF
import re


class PDFCreator:
    @staticmethod
    def create_pdf(image_paths, pdf_file, data):
        """
        image_paths: List of image paths
        data: List of Data strings-
        """
        try:
            writer = QPdfWriter(pdf_file)
            writer.setPageSizeMM(QSizeF(420, 297))
            writer.setResolution(300)

            painter = QPainter(writer)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.TextAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

            scale = writer.resolution() / 25.4
            painter.scale(scale, scale)

            # ページとマージン
            page_w, page_h = 420, 297
            margin = 10
            avail_w = page_w - 2 * margin
            avail_h = page_h - 2 * margin

            # ペン設定
            pen_w = 0.5
            pen = QPen(Qt.black, pen_w)
            pen.setCosmetic(False)
            painter.setPen(pen)
            adjust = pen_w / 2

            # グリッド：2行3列
            rows, cols = 2, 3
            cell_w = avail_w / cols
            cell_h = avail_h / rows
            cell_margin = 5

            # セル内3分割比率
            ratios = [0.72, 0.06, 0.22]

            idx = 0
            for row in range(rows):
                for col in range(cols):
                    # セル外枠位置
                    cell_x = margin + col * cell_w + adjust
                    cell_y = margin + row * cell_h + adjust
                    cw = cell_w - pen_w
                    ch = cell_h - pen_w

                    # 1列目のみ右に0.25mm
                    if col == 0:
                        cell_x += 0.25

                    # 表領域
                    table_x = cell_x + cell_margin
                    table_y = cell_y + cell_margin
                    tw = cw - 2 * cell_margin
                    th = ch - 2 * cell_margin

                    # 枠描画
                    painter.drawRect(QRectF(table_x, table_y, tw, th))

                    # セル内を3行1列のサブテーブルとして描画
                    y0 = table_y
                    heights = [th * r for r in ratios]
                    for i, h in enumerate(heights):
                        painter.drawRect(QRectF(table_x, y0, tw, h))
                        y0 += h

                    # サブセルごとにコンテンツ配置
                    y0 = table_y
                    # 1行目（画像）
                    if idx < len(image_paths):
                        img = QImage(image_paths[idx])
                        if not img.isNull():
                            area_h = heights[0]
                            area_w = tw
                            w_px = int(area_w * scale)
                            h_px = int(area_h * scale)
                            simg = img.scaled(
                                w_px, h_px, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            sw = simg.width() / scale
                            sh = simg.height() / scale
                            ix = table_x + (area_w - sw) / 2
                            iy = y0 + (area_h - sh) / 2
                            painter.drawImage(QRectF(ix, iy, sw, sh), simg)
                    y0 += heights[0]

                    # 2行目（写真No）
                    if idx < len(image_paths):
                        font = QFont("MS Gothic")
                        font.setStyleHint(QFont.Monospace)
                        font.setPointSizeF(0.8)
                        painter.setFont(font)
                        cw_mono = painter.fontMetrics().averageCharWidth()
                        rect = QRectF(
                            table_x + cw_mono,
                            y0,
                            tw - cw_mono,
                            heights[1]
                        )
                        painter.drawText(rect, Qt.AlignLeft |
                                         Qt.AlignVCenter, f"写真 No.{idx+1}")
                    y0 += heights[1]

                    # 3行目（Data text）
                    if idx < len(data):
                        txt = data[idx]
                        if "," in txt:
                            txt = txt.split(',', 1)[1].strip()
                        font2 = QFont("MS Gothic")
                        font2.setStyleHint(QFont.Monospace)
                        font2.setPointSizeF(0.8)
                        painter.setFont(font2)
                        lines = PDFCreator.wrap_text_custom(
                            txt, max_units=39)
                        sp = heights[2] / max(len(lines), 1)
                        yy = y0
                        for line in lines:
                            painter.drawText(
                                QRectF(table_x + cw_mono,
                                       yy, tw - cw_mono, sp),
                                Qt.AlignLeft | Qt.AlignVCenter, line)
                            yy += sp
                    idx += 1

            painter.end()
            return True, f"PDFを作成しました\n {pdf_file}"
        except Exception as e:
            return False, f"エラー発生:\n{e}"

    @staticmethod
    def wrap_text_custom(text, max_units=39):
        lines = []
        for para in text.splitlines():
            line, count = "", 0.0
            for ch in para:
                w = 0.5 if re.match(r'[ -~]', ch) else 1.0
                if count + w > max_units:
                    lines.append(line)
                    line, count = ch, w
                else:
                    line += ch
                    count += w
            if line:
                lines.append(line)
        return lines
