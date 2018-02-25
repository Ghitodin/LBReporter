from PyQt5.QtWidgets import QMessageBox

from AppConfig import APP_NAME


class EventLogger:
    @staticmethod
    def show_warning(str):
        if str is None:
            return

        QMessageBox.warning(None, APP_NAME, str, QMessageBox.Ok)