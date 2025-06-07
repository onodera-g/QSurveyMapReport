# -*- coding: utf-8 -*-
import os
from PyQt5.QtCore import QSettings, QTranslator, QCoreApplication

# プラグイン名を定義
PLUGIN_NAME = 'QSurveyMapReport'

# 翻訳ファイルをロードして QGIS にインストール
locale = QSettings().value('locale/userLocale')
if locale:
    locale = locale[0:2]
else:
    locale = 'en'
locale_path = os.path.join(os.path.dirname(
    __file__), 'i18n', f'{PLUGIN_NAME}_{locale}.qm')
if os.path.exists(locale_path):
    translator = QTranslator()
    translator.load(locale_path)
    QCoreApplication.installTranslator(translator)
    # Translator オブジェクトを保持しておく（ガベージコレクション対策）
    _translator = translator


def classFactory(iface):
    """Load QSurveyMapReport plugin class."""
    from .Menu_Button import QSurveyMapReport
    return QSurveyMapReport(iface)
