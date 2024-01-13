from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtGui import QIcon, QPixmap
from PySide6 import QtCore

from prepare_widget import prepareWidget
from optimize_widget import optimizeWidget
from saber import saberWidget


class mainWidget(QWidget):
    def __init__(self, app):
        super().__init__()

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
        tabwidget = tabWidget(app)
        layout.addWidget(tabwidget)

        self.setLayout(layout)

        self.setMinimumSize(self.sizeHint())


class tabWidget(QTabWidget):
    def __init__(self, app):
        super().__init__()

        self.tab1 = prepareWidget(app)
        self.tab2 = optimizeWidget(app)
        self.tab3 = saberWidget(app)

        self.preparetab = self.addTab(self.tab1, "1. Prepare data")
        self.optimizetab = self.addTab(self.tab2, "2. Optimize")
        self.sabertab = self.addTab(self.tab3, "3. SABER")

    def change_tab(self, name):
        self.setCurrentIndex(name)