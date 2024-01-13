import re
from PySide6.QtGui import QValidator


class NumbersOnly(QValidator):
    def validate(self, string, index):
        pattern = re.compile("[0-9]+")

        if string == "":
            return QValidator.State.Acceptable, string, index

        if pattern.fullmatch(string):
            return QValidator.State.Acceptable, string, index

        else:
            return QValidator.State.Invalid, string, index


class FloatsOnly(QValidator):
    def validate(self, string, index):
        pattern = re.compile("^[+-]?((\d*(\.\d*)?)|(\.\d+))$")

        if string == "":
            return QValidator.State.Acceptable, string, index

        if pattern.fullmatch(string):
            return QValidator.State.Acceptable, string, index

        else:
            return QValidator.State.Invalid, string, index
