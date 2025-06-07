# -*- coding: utf-8 -*-
import os
from PyQt5.QtCore import QSettings, QTranslator, QCoreApplication

PLUGIN_NAME = 'QSurveyMapReport'

# road langage file
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
    _translator = translator


def classFactory(iface):
    """Load QSurveyMapReport plugin class."""
    from .Menu_Button import QSurveyMapReport
    return QSurveyMapReport(iface)
