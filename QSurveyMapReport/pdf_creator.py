from PIL import Image
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
import textwrap


class PDFCreator:
    @staticmethod
    def create_pdf(image_paths, output_pdf, data=None):
        try:
            # 現在のディレクトリからフォントファイルのパスを取得
            current_dir = os.path.dirname(__file__)
            font_path = os.path.join(
                current_dir, "NotoSansJP-Black.ttf")  # フォントファイルを指定

            # 日本語フォントを登録
            pdfmetrics.registerFont(
                TTFont("Japanese-Bold", font_path))  # 太字用フォント登録

            # PDFの基本設定
            page_width, page_height = landscape(A3)
            c = canvas.Canvas(output_pdf, pagesize=landscape(A3))

            # 日本語フォントを設定（太字）
            c.setFont("Japanese-Bold", 10)

            # レイアウト設定
            margin_x, margin_y = 20, 20
            spacing_x, spacing_y = 20, 60  # 行間に余白を増加
            max_columns, max_rows = 3, 2
            available_width = page_width - 2 * \
                margin_x - (max_columns - 1) * spacing_x
            available_height = (page_height - 2 * margin_y -
                                (max_rows - 1) * spacing_y) / max_rows

            # 各画像と表枠のサイズ
            image_width = available_width / max_columns
            total_height = available_height  # 枠の高さ全体
            image_height = total_height * 0.8  # 60%を画像に割り当て
            remaining_height = total_height * 0.2  # 残り40%を番号とテキスト用に

            # テキストの改行を処理する関数
            def wrap_text_fixed(text, max_chars=36):
                """36文字ごとに改行"""
                return textwrap.fill(text, max_chars).splitlines()

            for i, image_path in enumerate(image_paths):
                row = (i // max_columns) % max_rows
                col = i % max_columns

                # ページ切り替え
                if i > 0 and i % (max_columns * max_rows) == 0:
                    c.showPage()
                    c.setFont("Japanese-Bold", 10)  # ページ切り替え後にフォントを再設定

                # 座標の計算
                x = margin_x + col * (image_width + spacing_x)
                y_offset = spacing_y // 2 if row == 1 else 0
                y = page_height - margin_y - \
                    (row + 1) * total_height - y_offset

                # 外枠を描画
                c.rect(x, y, image_width, total_height)

                # 画像を描画
                if os.path.exists(image_path):
                    img = Image.open(image_path)
                    aspect = img.width / img.height
                    display_width, display_height = image_width * \
                        0.95, image_height * 0.95  # 枠内に余白を持たせる
                    if image_width / image_height > aspect:
                        display_height = image_height * 0.95
                        display_width = aspect * display_height
                    else:
                        display_width = image_width * 0.95
                        display_height = display_width / aspect

                    offset_x = (image_width - display_width) / 2
                    offset_y = (image_height - display_height) / 2
                    c.drawImage(ImageReader(img), x + offset_x, y +
                                remaining_height + offset_y, display_width, display_height)

                # 写真と写真番号の間の線
                line1_y = y + remaining_height
                c.line(x, line1_y, x + image_width, line1_y)

                # 番号を描画（太字）
                padding = 5
                text1_y = line1_y - 15
                c.drawString(x + padding, text1_y, f"写真 No. {i + 1}")

                # 写真番号とテキストの間の線
                line2_y = text1_y - 10
                c.line(x, line2_y, x + image_width, line2_y)

                # テキストを描画
                if data and i < len(data):
                    text = data[i]  # 各写真に対応するテキストを取得
                    # ファイル名が含まれている場合は削除（改行文字列のみ使用）
                    if "," in text:
                        _, text = text.split(",", 1)
                    wrapped_text = wrap_text_fixed(text.strip())  # 36文字ごとに改行
                    text_start_y = line2_y - 15
                    for line in wrapped_text:
                        c.drawString(x + padding, text_start_y, line)  # 各行を描画
                        text_start_y -= 12  # 行間を設定

            c.save()
            return True, f"PDFが正常に作成されました: {output_pdf}"
        except Exception as e:
            return False, f"PDF作成中にエラーが発生しました: {e}"
