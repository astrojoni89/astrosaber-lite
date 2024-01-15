from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtGui import QIcon, QPixmap
from PySide6 import QtCore

from prepare_widget import prepareWidget
from optimize_widget import optimizeWidget
from saber_widget import saberWidget


class mainWidget(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.setWindowTitle("astrosaber lite")
        self.setWindowIcon(QIcon("images/icon.ico"))

        image_label = QLabel()
        image_label.setPixmap(
            QPixmap("images/astrosaber_lite_cutout.jpg").scaled(
                450, 100, QtCore.Qt.KeepAspectRatio
            )
        )
        image_label.setAlignment(QtCore.Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(image_label)
        self.tabwidget = tabWidget(app)

        layout.addWidget(self.tabwidget)

        self.setLayout(layout)

        self.setMinimumSize(self.sizeHint())

        # connect slots of info boxes to signals
        self.tabwidget.tab1.message.button(QMessageBox.Ok).clicked.connect(
            self.change_tab
        )
        self.tabwidget.tab1.message.button(QMessageBox.Cancel).clicked.connect(
            self.app.quit()
        )
        self.tabwidget.tab2.message.button(QMessageBox.Ok).clicked.connect(
            self.change_tab
        )
        self.tabwidget.tab2.message.button(QMessageBox.Cancel).clicked.connect(
            self.app.quit()
        )
        self.tabwidget.tab3.message.button(QMessageBox.Ok).clicked.connect(
            self.change_tab
        )
        self.tabwidget.tab3.message.button(QMessageBox.Cancel).clicked.connect(
            self.app.quit()
        )

    def change_tab(self):
        cur_index = self.tabwidget.currentIndex()
        if cur_index < self.tabwidget.count() - 1:
            self.tabwidget.setCurrentIndex(cur_index + 1)


class tabWidget(QTabWidget):
    def __init__(self, app):
        super().__init__()

        self.tab1 = prepareWidget(app)
        self.tab2 = optimizeWidget(app)
        self.tab3 = saberWidget(app)

        self.preparetab = self.addTab(self.tab1, "1. Prepare data")
        self.optimizetab = self.addTab(self.tab2, "2. Optimize")
        self.sabertab = self.addTab(self.tab3, "3. SABER")
