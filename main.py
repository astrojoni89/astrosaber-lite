from PySide6.QtWidgets import QApplication
from astrosaber_widget import mainWidget
import sys
import qdarktheme


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # set up theme
    qdarktheme.setup_theme()

    widget = mainWidget(app)
    widget.show()

    app.exec()
