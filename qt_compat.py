from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QFont, QPainter, QImage, QPageSize
from qgis.PyQt.QtWidgets import QMessageBox, QPlainTextEdit, QFrame


QT_ALIGNMENT = getattr(Qt, "AlignmentFlag", Qt)
QT_ASPECT_RATIO_MODE = getattr(Qt, "AspectRatioMode", Qt)
QT_GLOBAL_COLOR = getattr(Qt, "GlobalColor", Qt)
QT_SCROLL_BAR_POLICY = getattr(Qt, "ScrollBarPolicy", Qt)
QT_TRANSFORMATION_MODE = getattr(Qt, "TransformationMode", Qt)

QFONT_STYLE_HINT = getattr(QFont, "StyleHint", QFont)
QFONT_SPACING_TYPE = getattr(QFont, "SpacingType", QFont)
QFRAME_SHAPE = getattr(QFrame, "Shape", QFrame)
QIMAGE_FORMAT = getattr(QImage, "Format", QImage)
QMESSAGEBOX_STANDARD_BUTTON = getattr(QMessageBox, "StandardButton", QMessageBox)
QPAINTER_COMPOSITION_MODE = getattr(QPainter, "CompositionMode", QPainter)
QPAINTER_RENDER_HINT = getattr(QPainter, "RenderHint", QPainter)
QPAGE_SIZE_UNIT = getattr(QPageSize, "Unit", QPageSize)
QPLAINTEXTEDIT_LINE_WRAP_MODE = getattr(
    QPlainTextEdit,
    "LineWrapMode",
    QPlainTextEdit
)

ALIGN_CENTER = QT_ALIGNMENT.AlignCenter
ALIGN_LEFT = QT_ALIGNMENT.AlignLeft
ALIGN_VCENTER = QT_ALIGNMENT.AlignVCenter
ANTIALIASING = QPAINTER_RENDER_HINT.Antialiasing
BLACK = QT_GLOBAL_COLOR.black
COMPOSITION_MODE_SOURCE_IN = QPAINTER_COMPOSITION_MODE.CompositionMode_SourceIn
FRAME_BOX = QFRAME_SHAPE.Box
FORMAT_RGB32 = QIMAGE_FORMAT.Format_RGB32
FONT_MONOSPACE = QFONT_STYLE_HINT.Monospace
FONT_PERCENTAGE_SPACING = QFONT_SPACING_TYPE.PercentageSpacing
HIGH_QUALITY_ANTIALIASING = getattr(
    QPAINTER_RENDER_HINT,
    "HighQualityAntialiasing",
    ANTIALIASING
)
KEEP_ASPECT_RATIO = QT_ASPECT_RATIO_MODE.KeepAspectRatio
SCROLL_BAR_ALWAYS_OFF = QT_SCROLL_BAR_POLICY.ScrollBarAlwaysOff
SCROLL_BAR_AS_NEEDED = QT_SCROLL_BAR_POLICY.ScrollBarAsNeeded
SMOOTH_PIXMAP_TRANSFORM = QPAINTER_RENDER_HINT.SmoothPixmapTransform
SMOOTH_TRANSFORMATION = QT_TRANSFORMATION_MODE.SmoothTransformation
TEXT_ANTIALIASING = QPAINTER_RENDER_HINT.TextAntialiasing
WIDGET_WIDTH = QPLAINTEXTEDIT_LINE_WRAP_MODE.WidgetWidth
WHITE = QT_GLOBAL_COLOR.white
MESSAGEBOX_NO = QMESSAGEBOX_STANDARD_BUTTON.No
MESSAGEBOX_YES = QMESSAGEBOX_STANDARD_BUTTON.Yes
PAGE_SIZE_MILLIMETER = QPAGE_SIZE_UNIT.Millimeter


def app_exec(app):
    exec_method = getattr(app, "exec", None)
    if exec_method is not None:
        return exec_method()
    return app.exec_()


def set_pdf_page_size(writer, size_mm):
    set_page_size_mm = getattr(writer, "setPageSizeMM", None)
    if set_page_size_mm is not None:
        set_page_size_mm(size_mm)
        return
    writer.setPageSize(QPageSize(size_mm, PAGE_SIZE_MILLIMETER))
