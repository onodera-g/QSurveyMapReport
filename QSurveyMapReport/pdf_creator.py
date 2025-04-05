# pdf_creator.py
import re
from PIL import Image
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os


class PDFCreator:
    @staticmethod
    def create_pdf(image_paths, output_pdf, data=None):
        try:
            # フォント登録
            PDFCreator.register_font()

            # PDFの基本設定
            page_width, page_height = landscape(A3)
            c = canvas.Canvas(output_pdf, pagesize=landscape(A3))
            c.setFont("Japanese-Bold", 10)

            # レイアウト設定
            layout_params = PDFCreator.calculate_layout(
                page_width, page_height)

            for i, image_path in enumerate(image_paths):
                if i > 0 and i % (layout_params["max_columns"] * layout_params["max_rows"]) == 0:
                    c.showPage()
                    c.setFont("Japanese-Bold", 10)

                # 画像とテキストを描画
                PDFCreator.draw_content(
                    c, i, image_path, data, layout_params)

            c.save()
            return True, f"PDFが正常に作成されました: {output_pdf}"
        except Exception as e:
            return False, f"PDF作成中にエラーが発生しました: {e}"

    @staticmethod
    def register_font():
        """日本語フォントを登録"""
        current_dir = os.path.dirname(__file__)
        font_path = os.path.join(current_dir, "ipam.ttf")
        pdfmetrics.registerFont(TTFont("Japanese-Bold", font_path))

    @staticmethod
    def calculate_layout(page_width, page_height):
        """レイアウトパラメータを計算"""
        margin_x, margin_y = 20, 20
        spacing_x, spacing_y = 20, 60
        max_columns, max_rows = 3, 2
        available_width = page_width - 2 * \
            margin_x - (max_columns - 1) * spacing_x
        available_height = (page_height - 2 * margin_y -
                            (max_rows - 1) * spacing_y) / max_rows
        image_width = available_width / max_columns
        total_height = available_height
        image_height = total_height * 0.8
        remaining_height = total_height * 0.2

        return {
            "margin_x": margin_x,
            "margin_y": margin_y,
            "spacing_x": spacing_x,
            "spacing_y": spacing_y,
            "max_columns": max_columns,
            "max_rows": max_rows,
            "image_width": image_width,
            "image_height": image_height,
            "total_height": total_height,
            "remaining_height": remaining_height,
        }

    @staticmethod
    def wrap_text_custom(text, max_width=36.5):
        """半角と全角を考慮して文字列を改行し、既存の改行も尊重"""
        lines = []
        for paragraph in text.split('\n'):
            current_line = ""
            current_width = 0
            for char in paragraph:
                char_width = 0.5 if re.match(r'[ -~]', char) else 1
                if current_width + char_width > max_width:
                    lines.append(current_line)
                    current_line = char
                    current_width = char_width
                else:
                    current_line += char
                    current_width += char_width
            if current_line:
                lines.append(current_line)
        return lines

    @staticmethod
    def draw_content(c, i, image_path, data, layout_params):
        """画像とテキストを描画"""
        row = (i // layout_params["max_columns"]) % layout_params["max_rows"]
        col = i % layout_params["max_columns"]

        x = layout_params["margin_x"] + col * \
            (layout_params["image_width"] + layout_params["spacing_x"])
        y_offset = layout_params["spacing_y"] // 2 if row == 1 else 0
        y = (landscape(A3)[1] - layout_params["margin_y"] -
             (row + 1) * layout_params["total_height"] - y_offset)

        c.rect(x, y, layout_params["image_width"],
               layout_params["total_height"])

        if os.path.exists(image_path):
            PDFCreator.draw_image(c, image_path, x, y, layout_params)

        PDFCreator.draw_text(c, i, data, x, y, layout_params)

    @staticmethod
    def draw_image(c, image_path, x, y, layout_params):
        """画像を描画"""
        img = Image.open(image_path)
        aspect = img.width / img.height
        display_width, display_height = layout_params["image_width"] * \
            0.95, layout_params["image_height"] * 0.95

        if layout_params["image_width"] / layout_params["image_height"] > aspect:
            display_height = layout_params["image_height"] * 0.95
            display_width = aspect * display_height
        else:
            display_width = layout_params["image_width"] * 0.95
            display_height = display_width / aspect

        offset_x = (layout_params["image_width"] - display_width) / 2
        offset_y = (layout_params["image_height"] - display_height) / 2
        c.drawImage(ImageReader(img), x + offset_x, y +
                    layout_params["remaining_height"] + offset_y, display_width, display_height)

    @staticmethod
    def draw_text(c, i, data, x, y, layout_params):
        """番号とテキストを描画"""
        line1_y = y + layout_params["remaining_height"]
        c.line(x, line1_y, x + layout_params["image_width"], line1_y)

        padding = 5
        text1_y = line1_y - 15
        c.drawString(x + padding, text1_y, f"写真 No. {i + 1}")

        line2_y = text1_y - 10
        c.line(x, line2_y, x + layout_params["image_width"], line2_y)

        if data and i < len(data):
            text = data[i]
            if "," in text:
                _, text = text.split(",", 1)
            wrapped_text = PDFCreator.wrap_text_custom(
                text.strip(), max_width=36.5)
            text_start_y = line2_y - 15
            for line in wrapped_text:
                c.drawString(x + padding, text_start_y, line)
                text_start_y -= 12
