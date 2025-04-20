# Menu_Button.py

# QGIS
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
from qgis.gui import *
from .resources import *

# Python
import os
import sys
import codecs

# Menu_Dialogの読み込み
from .Menu_Dialog import Menu_Dialog  # 修正: Menu_Dialog クラスをインポート

# 文字コード変換用
QString = str
try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class QSurveyMapReport:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            f'QSurveyMapReport_{locale}.qm'
        )
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        self.actions = []
        self.menu = u'QSurveyMapReport'
        self.toolbar = self.iface.addToolBar(u'QSurveyMapReport')
        self.toolbar.setObjectName(u'QSurveyMapReport')

    def tr(self, message):
        return QCoreApplication.translate('QSurveyMapReport', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        icon = QIcon(icon_path) if icon_path else QIcon()
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        if status_tip:
            action.setStatusTip(status_tip)
        if whats_this:
            action.setWhatsThis(whats_this)
        if add_to_toolbar:
            self.toolbar.addAction(action)
        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)
        self.actions.append(action)
        return action

    def initGui(self):
        self.win = self.iface.mainWindow()
        icon_path = ':/plugins/QSurveyMapReport/icon/icon.png'
        # メニュー設定
        self.add_action(
            icon_path=None,
            text=u"QSurveyMapReport",
            callback=self.Menu02,
            parent=self.win)

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(
                u'QSurveyMapReport',
                action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def Menu02(self):
        # Menu_Dialog表示
        self.dialog = Menu_Dialog(self.iface)
        self.dialog.show()

    def run(self):
        pass
