from PyQt5 import QtCore
from PyQt5.QtCore import QVariant


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, datalist, parent=None, *args):
        super(TableModel, self).__init__()
        self.datalist = datalist

    def update(self, dataIn):
        print('Updating Model')
        self.datalist = dataIn
        print('Datatable : {0}'.format(self.datalist))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.datalist)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 3

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        if index.row() >= len(self.datalist) or index.row() < 0:
            return QVariant()

        if role == QtCore.Qt.DisplayRole:
            data = self.datalist[index.row()]
            if index.column() == 0:
                return data.trade_id
            elif index.column() == 1:
                return data.seller_username
            elif index.column() == 2:
                return data.adv_owner_username
        else:
            return QVariant()

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled