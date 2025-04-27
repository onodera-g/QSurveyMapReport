from PyQt5.QtGui import QPdfWriter, QPainter, QPen, QImage, QFont
from PyQt5.QtCore import QSizeF, Qt, QRectF
import re
import math


class PDFCreator:
    """PDF作成ユーティリティクラス"""
    # --- 定数定義 ---
    PAGE_SIZE_MM = QSizeF(420, 297)  # A3
    DPI = 300
    MARGIN_MM = 10
    ROWS = 2
    COLS = 3
    CELL_MARGIN_MM = 5
    RATIOS = (0.72, 0.06, 0.22)  # [画像／No／テキスト] の高さ比
    FONT_SIZE_PT = 0.8
    LETTER_SPACING_PERCENT = 83

    @staticmethod
    def _init_painter(painter, scale):
        """QPainter のレンダリング設定とスケール適用"""
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.scale(scale, scale)

    @staticmethod
    def _create_font():
        """MS Gothic 等幅フォントを生成"""
        font = QFont("MS Gothic")
        font.setStyleHint(QFont.Monospace)
        font.setPointSizeF(PDFCreator.FONT_SIZE_PT)
        font.setLetterSpacing(QFont.PercentageSpacing,
                              PDFCreator.LETTER_SPACING_PERCENT)
        return font

    @staticmethod
    def wrap_text_custom(text, max_units=36):
        """独自改行: 半角0.5, 全角1 で max_units を超えたら改行"""
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
        PDF を生成する
        :param image_paths: 画像ファイルパスのリスト
        :param pdf_file: 出力 PDF ファイルパス
        :param data: 各画像に対応するテキストリスト
        :return: (成功フラグ, メッセージ)
        """
        try:
            # --- PDFWriter 設定 ---
            writer = QPdfWriter(pdf_file)
            writer.setPageSizeMM(PDFCreator.PAGE_SIZE_MM)
            writer.setResolution(PDFCreator.DPI)
            scale = writer.resolution() / 25.4

            # --- レイアウト計算 ---
            pw, ph = PDFCreator.PAGE_SIZE_MM.width(), PDFCreator.PAGE_SIZE_MM.height()
            avail_w = pw - 2 * PDFCreator.MARGIN_MM
            avail_h = ph - 2 * PDFCreator.MARGIN_MM
            slots = PDFCreator.ROWS * PDFCreator.COLS
            cell_w = avail_w / PDFCreator.COLS
            cell_h = avail_h / PDFCreator.ROWS
            total = len(image_paths)
            if total == 0:
                return False, "画像が見つかりません"
            pages = math.ceil(total / slots)

            # --- ペンとペインタ初期化 ---
            pen = QPen(Qt.black, 0.5)
            painter = QPainter(writer)
            PDFCreator._init_painter(painter, scale)
            painter.setPen(pen)

            # --- ページ描画 ---
            for page_idx in range(pages):
                base = page_idx * slots
                for i in range(slots):
                    idx = base + i
                    if idx >= total:
                        break
                    # セル座標
                    row, col = divmod(i, PDFCreator.COLS)
                    x0 = PDFCreator.MARGIN_MM + col * cell_w + 0.25
                    y0 = PDFCreator.MARGIN_MM + row * cell_h
                    cw = cell_w - pen.widthF()
                    ch = cell_h - pen.widthF()
                    tx, ty = PDFCreator.CELL_MARGIN_MM, PDFCreator.CELL_MARGIN_MM
                    tw, th = cw - 2*tx, ch - 2*ty

                    # 外枠
                    painter.drawRect(QRectF(x0+tx, y0+ty, tw, th))

                    # サブ行枠
                    y_sub = y0 + ty
                    heights = [th * r for r in PDFCreator.RATIOS]
                    for h in heights:
                        painter.drawRect(QRectF(x0+tx, y_sub, tw, h))
                        y_sub += h

                    # 画像描画
                    y_img = y0 + ty
                    img = QImage(image_paths[idx])
                    if not img.isNull():
                        area_w, area_h = tw, heights[0]
                        w_px, h_px = int(area_w*scale), int(area_h*scale)
                        simg = img.scaled(
                            w_px, h_px, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        sw, sh = simg.width()/scale, simg.height()/scale
                        ix = x0 + tx + (area_w - sw)/2
                        iy = y_img + (area_h - sh)/2
                        painter.drawImage(QRectF(ix, iy, sw, sh), simg)

                    # 番号描画
                    y_no = y0 + ty + heights[0]
                    painter.setFont(PDFCreator._create_font())
                    fm = painter.fontMetrics().averageCharWidth()
                    painter.drawText(
                        QRectF(x0+tx+fm, y_no, tw-fm, heights[1]),
                        Qt.AlignLeft | Qt.AlignVCenter,
                        f"写真 No.{idx+1}"
                    )

                    # テキスト描画
                    y_txt = y_no + heights[1]
                    txt = data[idx].split(",", 1)[1].strip() if idx < len(
                        data) and "," in data[idx] else data[idx]
                    painter.setFont(PDFCreator._create_font())
                    lines = PDFCreator.wrap_text_custom(txt)
                    line_h = heights[2] / max(len(lines), 1)
                    y_line = y_txt
                    for line in lines:
                        painter.drawText(
                            QRectF(x0+tx+fm, y_line, tw-fm, line_h),
                            Qt.AlignLeft | Qt.AlignVCenter,
                            line
                        )
                        y_line += line_h

                # 改ページ
                if page_idx < pages-1:
                    painter.resetTransform()
                    writer.newPage()
                    PDFCreator._init_painter(painter, scale)
                    painter.setPen(pen)

            painter.end()
            return True, f"PDFを作成しました\n{pdf_file}"
        except Exception as e:
            return False, f"エラー発生:\n{e}"
