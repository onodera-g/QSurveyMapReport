import os
from PyQt5.QtCore import QSettings, QTranslator, QCoreApplication, qVersion
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from .Menu_Dialog import Menu_Dialog


class QSurveyMapReport:
    """QSurveyMapReport プラグイン メインクラス"""
    PLUGIN_NAME = 'QSurveyMapReport'  # プラグイン名

    def __init__(self, iface):
        """:param iface: QGISのインターフェースインスタンス"""
        self.iface = iface
        self.canvas = iface.mapCanvas()  # マップキャンバスの参照
        self.plugin_dir = os.path.dirname(__file__)  # プラグインディレクトリのパス
        self._load_locale()  # 翻訳ファイルの読み込み
        self.actions = []  # 登録したアクションを保持
        self.menu = self.PLUGIN_NAME  # メニュー名
        self.toolbar = iface.addToolBar(self.PLUGIN_NAME)  # ツールバー作成
        self.toolbar.setObjectName(self.PLUGIN_NAME)

    def _load_locale(self):
        """ユーザーロケールに応じた翻訳ファイル (.qm) を読み込む"""
        locale = QSettings().value('locale/userLocale')[0:2]
        qm_path = os.path.join(
            self.plugin_dir,
            'i18n',
            f'{self.PLUGIN_NAME}_{locale}.qm'
        )
        if os.path.exists(qm_path):
            translator = QTranslator()
            translator.load(qm_path)
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(translator)

    def tr(self, message):
        """QGIS翻訳コンテキストでメッセージを翻訳する"""
        return QCoreApplication.translate(self.PLUGIN_NAME, message)

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
        """メニューとツールバーにアクションを追加する"""
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
        """GUIを初期化: メニューとツールバーにプラグイン起動アクションを追加"""
        self.add_action(
            icon_path=None,
            text=self.tr(self.PLUGIN_NAME),
            callback=self.open_plugin_dialog
        )

    def unload(self):
        """プラグインアンロード時: メニューとツールバーアイコンを削除"""
        for action in self.actions:
            self.iface.removePluginMenu(self.menu, action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def open_plugin_dialog(self):
        """プラグインダイアログを表示する"""
        self.dialog = Menu_Dialog(self.iface)  # ダイアログを保持して開く
        self.dialog.show()

    def run(self):
        """互換用エントリポイント: プラグインダイアログを開く"""
        self.open_plugin_dialog()
