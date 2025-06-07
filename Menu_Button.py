import os
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from . import PLUGIN_NAME
from .Menu_Dialog import Menu_Dialog


class QSurveyMapReport:
    """Main class for the QSurveyMapReport plugin."""

    def __init__(self, iface):
        """
        :param iface: QGIS interface instance
        """
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.plugin_dir = os.path.dirname(__file__)
        # 翻訳はプラグイン読み込み時に適用済み
        self.actions = []  # List of QAction
        self.menu = PLUGIN_NAME  # Plugin menu name
        self.toolbar = iface.addToolBar(PLUGIN_NAME)
        self.toolbar.setObjectName(PLUGIN_NAME)

    def tr(self, message):
        """Return translated string using plugin locale."""
        return QCoreApplication.translate(PLUGIN_NAME, message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None
    ):
        """Create a QAction, add it to the menu and toolbar, and return it."""
        parent = parent or self.iface.mainWindow()
        icon = QIcon(icon_path) if icon_path else QIcon()
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled)
        if status_tip:
            action.setStatusTip(status_tip)
        if whats_this:
            action.setWhatsThis(whats_this)
        if add_to_toolbar:
            self.toolbar.addAction(action)
        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)
        self.actions.append(action)
        return action

    def initGui(self):
        """Initialize GUI: add the plugin entry to QGIS menu and toolbar."""
        # プラグインのメニューアクションを追加（クリックでダイアログを開く）
        self.add_action(
            icon_path=None,
            text=self.tr(PLUGIN_NAME),
            callback=self.open_plugin_dialog
        )

    def unload(self):
        """Remove plugin menu entries and toolbar icons when plugin is unloaded."""
        for action in self.actions:
            self.iface.removePluginMenu(self.menu, action)
            self.iface.removeToolBarIcon(action)
        # ツールバーを削除
        del self.toolbar

    def open_plugin_dialog(self):
        """Instantiate and show the main dialog."""
        self.dialog = Menu_Dialog(self.iface)
        self.dialog.show()

    def run(self):
        """Backward compatibility: directly open the plugin dialog."""
        self.open_plugin_dialog()
