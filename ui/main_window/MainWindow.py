from PyQt5.QtWidgets import QMainWindow, QMessageBox

from LocalBitcoins import LocalBitcoins
from AppConfig import APP_NAME
from Settings import AppSettings
from User import User
from ui.autogen_ui.Ui_MainWindow import Ui_MainWindow
from ui.settings_dialog.SettingsDialog import SettingsDialog


class MainWindow(QMainWindow):
    app_settings = AppSettings()
    user = User()
    local_bitcoins = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # init ui:
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()
        # set action events:
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionSettings.triggered.connect(self.open_settings_dialog)
        self.ui.actionUpdate.triggered.connect(self.test_connection)

    def open_settings_dialog(self):
        try:
            settings_dialog = SettingsDialog(app_settings=self.app_settings)
            settings_dialog.on_data_changed.connect(self.test_connection)
            settings_dialog.exec()
        except ValueError:
            QMessageBox.warning(self, APP_NAME, 'Something wrong', QMessageBox.Ok)

    def init_ui(self):
        self.draw_user(self.user)

    def test_connection(self):
        print('Test connection clicked')

        try:
            LocalBitcoins.get_user(self.app_settings.hmac, self.app_settings.hmac_secret)
        except ValueError:
            pass

    def draw_user(self, user):
        # hide ui elements:
        if user.is_empty():
            self.ui.usernameLabel.setText("No user")
            self.ui.urlFieldLabel.hide()
            self.ui.urlLabel.hide()
            self.ui.feedbackScoreFieldLabel.hide()
            self.ui.feedbackScoreLabel.hide()
            self.ui.feedbackCountFieldLabel.hide()
            self.ui.feedbackCountLabel.hide()
            self.ui.tradeVolumeFieldLabel.hide()
            self.ui.tradeVolumeLabel.hide()
            self.ui.createdAtFieldLabel.hide()
            self.ui.createdAtLabel.hide()
        # show ui elements:
        else:
            self.ui.usernameLabel.setText(user.username)
            # url:
            self.ui.urlFieldLabel.show()
            self.ui.urlLabel.show()
            self.ui.urlLabel.setText(user.url)
            # feedback_score:
            self.ui.feedbackScoreFieldLabel.show()
            self.ui.feedbackScoreLabel.show()
            self.ui.feedbackScoreLabel.setText(user.feedback_score)
            # feedback_count:
            self.ui.feedbackCountFieldLabel.show()
            self.ui.feedbackCountLabel.show()
            self.ui.feedbackCountLabel.setText(user.feedback_count)
            # trade_volume:
            self.ui.tradeVolumeFieldLabel.show()
            self.ui.tradeVolumeLabel.show()
            self.ui.tradeVolumeLabel.setText(user.trade_volume)
            # created_at:
            self.ui.createdAtFieldLabel.show()
            self.ui.createdAtLabel.show()
            self.ui.createdAtLabel.setText(user.created_at)
