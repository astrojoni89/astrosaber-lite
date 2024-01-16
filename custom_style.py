from PySide6.QtGui import QFont


# custom style settings
def set_highlight(widget):
    widget.setStyleSheet("border: 1px solid red;")

def set_normal_style(widget, ss):
    widget.setStyleSheet(ss)

def set_bold(widget):
    myBold = QFont()
    myBold.setBold(True)
    widget.setFont(myBold)

def set_large_font(widget):
    myLarge = QFont()
    myLarge.setPointSize(14)
    widget.setFont(myLarge)

def set_normal_font(widget):
    myBold = QFont()
    myBold.setBold(False)
    widget.setFont(myBold)
