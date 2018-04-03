from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from EventLogger import EventLogger
from LocalBitcoins import LocalBitcoins
from AppConfig import APP_NAME
from Settings import AppSettings
from data.DataModel import User
from data.source.TradesRepository import TradesRepository
from model.table import TableModel
from ui.autogen_ui.Ui_MainWindow import Ui_MainWindow
from ui.settings_dialog.SettingsDialog import SettingsDialog


class MainWindow(QMainWindow):
    app_settings = AppSettings()
    user = User()
    local_bitcoins = LocalBitcoins()
    trades_repo = TradesRepository()
    main_table_model = TableModel(list())

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.__init_ui()
        # set action events:
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionSettings.triggered.connect(self.open_settings_dialog)
        self.ui.actionUpdate.triggered.connect(self.__on_update_trades, type=Qt.QueuedConnection)
        # set other callbacks:
        self.local_bitcoins.on_error_occurred.connect(self.__on_api_error)
        self.local_bitcoins.on_user_received.connect(self.__on_user_obtained)
        self.local_bitcoins.on_request_started.connect(self.__on_request_to_api_ui_lock)
        self.local_bitcoins.on_request_finished.connect(self.__on_request_to_api_ui_unlock)
        # self.local_bitcoins.on_error_occurred.connect(self.__on_request_to_api_ui_unlock)
        self.local_bitcoins.on_trades_received.connect(self.__on_trades_obtained)
        # set models:
        self.ui.tableView.setModel(self.main_table_model)

        self.__renew_user()

    def open_settings_dialog(self):
        try:
            settings_dialog = SettingsDialog(app_settings=self.app_settings)
            settings_dialog.on_data_changed.connect(self.__renew_user, type=Qt.QueuedConnection)
            settings_dialog.exec()
        except ValueError:
            QMessageBox.warning(self, APP_NAME, 'Something wrong', QMessageBox.Ok)

    def __init_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__redraw_current_user()
        self.setWindowTitle(APP_NAME)

    def __renew_user(self):
        if not self.app_settings.hmac or not self.app_settings.hmac_secret:
            self.__on_request_to_api_ui_lock()
            return
        try:
            self.local_bitcoins.get_user(self.app_settings.hmac, self.app_settings.hmac_secret)

        except ValueError:
            pass

    def __on_user_obtained(self, user):
        self.user = user
        self.__redraw_current_user()

    def __on_api_error(self, err_str):
        EventLogger.show_warning(err_str)

    def __redraw_current_user(self):
        # hide ui elements:
        if self.user.is_empty():
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
            self.ui.usernameLabel.setText(self.user.username)
            # url:
            self.ui.urlFieldLabel.show()
            self.ui.urlLabel.show()
            self.ui.urlLabel.setText(self.user.url)
            # feedback_score:
            self.ui.feedbackScoreFieldLabel.show()
            self.ui.feedbackScoreLabel.show()
            self.ui.feedbackScoreLabel.setText(self.user.feedback_score)
            # feedback_count:
            self.ui.feedbackCountFieldLabel.show()
            self.ui.feedbackCountLabel.show()
            self.ui.feedbackCountLabel.setText(str(self.user.feedback_count))
            # trade_volume:
            self.ui.tradeVolumeFieldLabel.show()
            self.ui.tradeVolumeLabel.show()
            self.ui.tradeVolumeLabel.setText(self.user.trade_volume)
            # created_at:
            self.ui.createdAtFieldLabel.show()
            self.ui.createdAtLabel.show()
            self.ui.createdAtLabel.setText(self.user.created_at)

    def __on_request_to_api_ui_lock(self):
        self.ui.actionUpdate.setDisabled(True)

    def __on_request_to_api_ui_unlock(self):
        self.ui.actionUpdate.setDisabled(False)

    def __on_update_trades(self):
        self.local_bitcoins.get_released_trades_test(self.app_settings.hmac, self.app_settings.hmac_secret)

    def __on_trades_obtained(self, trades):
        print(self.user)

        #self.trades_repo.save_trades(trades, self.user) # TODO: collisions %D

        for trade in trades:
            print(trade)
            self.main_table_model.insertRows(0, 1, trade, QModelIndex())

    def __data_updated(self):
        self.ui.actionUpdate.setDisabled(False)
