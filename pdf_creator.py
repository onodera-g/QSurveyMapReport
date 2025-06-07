from PyQt5.QtGui import QPdfWriter, QPainter, QPen, QImage, QFont
from PyQt5.QtCore import QSizeF, Qt, QRectF, QCoreApplication
import re
import math


class PDFCreator:
    """PDF creation utility class"""

    # --- Constant definitions ---
    PAGE_SIZE_MM = QSizeF(420, 297)  # A3
    DPI = 300
    MARGIN_MM = 10
    ROWS = 2
    COLS = 3
    CELL_MARGIN_MM = 5
    RATIOS = (0.72, 0.06, 0.22)  # [image / number / text] height ratios
    FONT_SIZE_PT = 0.8
    LETTER_SPACING_PERCENT = 83

    @staticmethod
    def tr(message):
        """Translation helper method"""
        return QCoreApplication.translate("PDFCreator", message)

    @staticmethod
    def _init_painter(painter, scale):
        """Set rendering hints on QPainter and apply scaling"""
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.scale(scale, scale)

    @staticmethod
    def _create_font():
        """Generate an MS Gothic monospaced font"""
        font = QFont("MS Gothic")
        font.setStyleHint(QFont.Monospace)
        font.setPointSizeF(PDFCreator.FONT_SIZE_PT)
        font.setLetterSpacing(QFont.PercentageSpacing,
                              PDFCreator.LETTER_SPACING_PERCENT)
        return font

    @staticmethod
    def wrap_text_custom(text, max_units=36):
        """Custom line wrapping: half-width = 0.5 units, full-width = 1 unit"""
        lines = []
        for para in text.splitlines():
            line, count = "", 0.0
            for ch in para:
                w = 0.5 if re.match(r"[ -~]", ch) else 1.0
                if count + w > max_units:
                    lines.append(line)
                    line, count = ch, w
                else:
                    line += ch
                    count += w
            if line:
                lines.append(line)
        return lines

    @staticmethod
    def create_pdf(image_paths, pdf_file, data):
        """
        Generate a PDF
        :param image_paths: list of image file paths
        :param pdf_file: output PDF file path
        :param data: list of text corresponding to each image
        :return: (success_flag, message)
        """
        try:
            # --- Configure QPdfWriter ---
            writer = QPdfWriter(pdf_file)
            writer.setPageSizeMM(PDFCreator.PAGE_SIZE_MM)
            writer.setResolution(PDFCreator.DPI)
            scale = writer.resolution() / 25.4

            # --- Layout calculation ---
            pw, ph = PDFCreator.PAGE_SIZE_MM.width(), PDFCreator.PAGE_SIZE_MM.height()
            avail_w = pw - 2 * PDFCreator.MARGIN_MM
            avail_h = ph - 2 * PDFCreator.MARGIN_MM
            slots = PDFCreator.ROWS * PDFCreator.COLS
            cell_w = avail_w / PDFCreator.COLS
            cell_h = avail_h / PDFCreator.ROWS
            total = len(image_paths)
            if total == 0:
                return False, PDFCreator.tr("No images found")
            pages = math.ceil(total / slots)

            # --- Initialize pen and painter ---
            pen = QPen(Qt.black, 0.5)
            painter = QPainter(writer)
            PDFCreator._init_painter(painter, scale)
            painter.setPen(pen)

            # --- Draw pages ---
            for page_idx in range(pages):
                base = page_idx * slots
                for i in range(slots):
                    idx = base + i
                    if idx >= total:
                        break

                    # Compute cell coordinates
                    row, col = divmod(i, PDFCreator.COLS)
                    x0 = PDFCreator.MARGIN_MM + col * cell_w + 0.25
                    y0 = PDFCreator.MARGIN_MM + row * cell_h
                    cw = cell_w - pen.widthF()
                    ch = cell_h - pen.widthF()
                    tx, ty = PDFCreator.CELL_MARGIN_MM, PDFCreator.CELL_MARGIN_MM
                    tw, th = cw - 2 * tx, ch - 2 * ty

                    # Draw outer rectangle
                    painter.drawRect(QRectF(x0 + tx, y0 + ty, tw, th))

                    # Draw sub-row rectangles
                    y_sub = y0 + ty
                    heights = [th * r for r in PDFCreator.RATIOS]
                    for h in heights:
                        painter.drawRect(QRectF(x0 + tx, y_sub, tw, h))
                        y_sub += h

                    # Draw image
                    y_img = y0 + ty
                    img = QImage(image_paths[idx])
                    if not img.isNull():
                        area_w, area_h = tw, heights[0]
                        w_px, h_px = int(area_w * scale), int(area_h * scale)
                        simg = img.scaled(
                            w_px, h_px, Qt.KeepAspectRatio, Qt.SmoothTransformation
                        )
                        sw, sh = simg.width() / scale, simg.height() / scale
                        ix = x0 + tx + (area_w - sw) / 2
                        iy = y_img + (area_h - sh) / 2
                        painter.drawImage(QRectF(ix, iy, sw, sh), simg)

                    # Draw number
                    y_no = y0 + ty + heights[0]
                    painter.setFont(PDFCreator._create_font())
                    fm = painter.fontMetrics().averageCharWidth()
                    no_text = PDFCreator.tr("Photo No.{0}").format(idx + 1)
                    painter.drawText(
                        QRectF(x0 + tx + fm, y_no, tw - fm, heights[1]),
                        Qt.AlignLeft | Qt.AlignVCenter,
                        no_text
                    )

                    # Draw text
                    y_txt = y_no + heights[1]
                    txt = ""
                    if idx < len(data) and "," in data[idx]:
                        txt = data[idx].split(",", 1)[1].strip()
                    else:
                        txt = data[idx] if idx < len(data) else ""
                    painter.setFont(PDFCreator._create_font())
                    lines = PDFCreator.wrap_text_custom(txt)
                    line_h = heights[2] / max(len(lines), 1)
                    y_line = y_txt
                    for line in lines:
                        painter.drawText(
                            QRectF(x0 + tx + fm, y_line, tw - fm, line_h),
                            Qt.AlignLeft | Qt.AlignVCenter,
                            line
                        )
                        y_line += line_h

                # New page if not last
                if page_idx < pages - 1:
                    painter.resetTransform()
                    writer.newPage()
                    PDFCreator._init_painter(painter, scale)
                    painter.setPen(pen)

            painter.end()
            success_msg = PDFCreator.tr("PDF created\n{0}").format(pdf_file)
            return True, success_msg

        except Exception as e:
            error_msg = PDFCreator.tr("Error occurred:\n{0}").format(e)
            return False, error_msg
