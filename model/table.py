from PyQt5 import QtCore
from PyQt5.QtCore import QVariant, QAbstractTableModel, QModelIndex, Qt


class TableModel(QAbstractTableModel):
    __data = list()
    def __init__(self, datalist):
        super(TableModel, self).__init__()
        self.__data = datalist

    def insertRows(self, position, rows, item, parent=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        self.__data.append(item)  # Item must be an array
        self.endInsertRows()
        return True

    def rowCount(self, parent=QModelIndex(), **kwargs):
        return len(self.__data)

    def columnCount(self, parent=QModelIndex(), **kwargs):
        return 3

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        if index.row() >= len(self.__data) or index.row() < 0:
            return QVariant()

        if role == Qt.DisplayRole:
            data = self.__data[index.row()]
            if index.column() == 0:
                return data.trade_id
            elif index.column() == 1:
                return data.seller_username
            elif index.column() == 2:
                return data.adv_owner_username
        else:
            return QVariant()

    def flags(self, index):
        return Qt.ItemIsEnabled

    def get_data(self):
        return self.__data

    def headerData(self, section, Qt_Orientation, role=None):
        if role != Qt.DisplayRole:
            return QVariant()

        if Qt_Orientation == Qt.Horizontal:
            if section == 0:
                return 'Trade id'
            elif section == 1:
                return 'Seller username'
            elif section == 2:
                return 'Owner username'

        return QVariant()
