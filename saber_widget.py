import multiprocessing
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QGridLayout,
    QSizePolicy,
    QMessageBox,
    QFileDialog,
    QLabel,
    QLineEdit,
)
from PySide6 import QtCore

from validators import NumbersOnly, FloatsOnly
from custom_style import (
    set_highlight,
    set_normal_style,
    set_bold,
    set_large_font,
    set_normal_font,
)
from animated_toggle import AnimatedToggle
from astrosaber.hisa import HisaExtraction


class saberWidget(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.filename = None

        self.resize(self.sizeHint())

        # initialize info box
        self.message = QMessageBox()
        self.message.setMinimumSize(700, 200)
        self.message.setWindowTitle("Done!")
        infotext = "SABER run was successful!"
        self.message.setText(infotext)
        # message.setInformativeText("Do you want to do something about it?")
        self.message.setIcon(QMessageBox.Information)
        self.message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.message.setDefaultButton(QMessageBox.Ok)
        self.message.button(QMessageBox.Ok).setText("Continue")
        self.message.button(QMessageBox.Cancel).setText("Quit")

        # status label
        self.status_label = QLabel("\n\n\n")
        self.status_param = False

        # file browser
        self.button_fb = QPushButton("Browse file")
        self.button_fb.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button_fb.clicked.connect(self.get_file_name)
        # self.text_holder_label_selected = QLabel("Selected file:")
        self.text_holder_label_dialog = QLabel("No file selected")
        self.text_holder_label_dialog.setWordWrap(True)

        # noise field
        self.text_holder_label_noise = QLabel("Noise*")
        self.line_edit_noise = QLineEdit(placeholderText="e.g. 4.")
        self.line_edit_noise.setValidator(FloatsOnly())
        # get style
        self.ss_line_edit_noise = self.line_edit_noise.styleSheet()
        # connect returnKey signal to slot
        self.line_edit_noise.returnPressed.connect(self.validate_record)

        # phase field
        self.text_holder_label_phase = QLabel("Two-phase")
        self.text_holder_label_phase.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        )
        self.phase_toggle = AnimatedToggle()
        self.phase_toggle.setFixedSize(self.phase_toggle.sizeHint())
        self.phase_toggle.setChecked(True)

        # add residual
        self.text_holder_label_addres = QLabel("Add residual")
        self.text_holder_label_addres.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        )
        self.addres_toggle = AnimatedToggle()
        self.addres_toggle.setFixedSize(self.addres_toggle.sizeHint())
        self.addres_toggle.setChecked(True)

        # lambda field
        self.text_holder_label_lam1 = QLabel("\u03BB\u2081*")
        set_large_font(self.text_holder_label_lam1)
        self.text_holder_label_lam1.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        )
        self.line_edit_lam1 = QLineEdit(placeholderText="e.g. 2.")
        self.line_edit_lam1.setValidator(FloatsOnly())

        self.text_holder_label_lam2 = QLabel("\u03BB\u2082*")
        set_large_font(self.text_holder_label_lam2)
        self.text_holder_label_lam2.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        )
        self.line_edit_lam2 = QLineEdit(placeholderText="e.g. 1.")
        self.line_edit_lam2.setValidator(FloatsOnly())
        # get style
        self.ss_line_edit_lam1 = self.line_edit_lam1.styleSheet()
        self.ss_line_edit_lam2 = self.line_edit_lam2.styleSheet()
        # connect returnKey signal to slot
        self.line_edit_lam1.returnPressed.connect(self.validate_record)
        self.line_edit_lam2.returnPressed.connect(self.validate_record)

        # ncpus field
        self.text_holder_label_ncpus = QLabel("#CPUs")
        self.line_edit_ncpus = QLineEdit(placeholderText="e.g. 4")
        self.line_edit_ncpus.setValidator(NumbersOnly())
        self.text_label_available_ncpus = QLabel("/" + str(multiprocessing.cpu_count()))
        # get style
        self.ss_line_edit_ncpus = self.line_edit_ncpus.styleSheet()
        # connect returnKey signal to slot
        self.line_edit_ncpus.returnPressed.connect(self.validate_record)
        ###

        # button to set params
        button_set_param = QPushButton("Set Parameters")
        button_set_param.clicked.connect(self.validate_record)

        # button to run prepare
        button_run_optimize = QPushButton("Run SABER")
        set_bold(button_run_optimize)
        button_run_optimize.clicked.connect(self.run_optimize)

        # Layouts
        layout = QGridLayout()

        layout.addWidget(self.button_fb, 1, 0, 1, 1)
        layout.addWidget(self.text_holder_label_dialog, 1, 1, 1, 3)

        layout.addWidget(self.text_holder_label_noise, 2, 0, 1, 1)
        layout.addWidget(self.line_edit_noise, 2, 1, 1, 2)

        layout.addWidget(self.text_holder_label_phase, 3, 0, 1, 1)
        layout.addWidget(self.phase_toggle, 3, 1, 1, 1)
        layout.addWidget(self.text_holder_label_addres, 3, 2, 1, 1)
        layout.addWidget(self.addres_toggle, 3, 3, 1, 1)

        layout.addWidget(self.text_holder_label_lam1, 4, 0, 1, 1)
        layout.addWidget(self.line_edit_lam1, 4, 1, 1, 1)
        layout.addWidget(self.text_holder_label_lam2, 4, 2, 1, 1)
        layout.addWidget(self.line_edit_lam2, 4, 3, 1, 1)

        layout.addWidget(self.text_holder_label_ncpus, 5, 0, 1, 1)
        layout.addWidget(self.line_edit_ncpus, 5, 1, 1, 1)
        layout.addWidget(self.text_label_available_ncpus, 5, 2, 1, 1)

        # set_param button
        layout.addWidget(button_set_param, 6, 1, 1, 2)
        # status label
        layout.addWidget(self.status_label, 7, 0, 1, 4)
        # run_optimize button
        layout.addWidget(button_run_optimize, 8, 1, 1, 2)

        self.setLayout(layout)

    def get_file_name(self):
        file_filter = "Data file (*.fits)"
        self.filename = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a file",
            filter=file_filter,
        )
        self.text_holder_label_dialog.setText(self.filename[0])

    def validate_record(self):
        if self.filename is None or self.filename[0] == "":
            self.status_label.setText("No file specified.")
            # self.set_bold(self.text_holder_label_selected)
            self.button_fb.setFocus()
            return

        # noise sect.
        if self.line_edit_noise.text() == "":
            self.status_label.setText("Missing required fields.")
            self.line_edit_noise.setFocus()
            set_highlight(self.line_edit_noise)
            set_bold(self.text_holder_label_noise)
            return

        # noise sect.
        set_normal_style(self.line_edit_noise, self.ss_line_edit_noise)
        set_normal_font(self.text_holder_label_noise)

        # lam1 sect.
        if self.line_edit_lam1.text() == "":
            self.status_label.setText("Missing required fields.")
            self.line_edit_lam1.setFocus()
            set_highlight(self.line_edit_lam1)
            set_bold(self.text_holder_label_lam1)
            return

        # lam1 sect.
        set_normal_style(self.line_edit_lam1, self.ss_line_edit_lam1)
        set_normal_font(self.text_holder_label_lam1)

        # lam2 sect.
        if self.line_edit_lam2.text() == "":
            self.status_label.setText("Missing required fields.")
            self.line_edit_lam2.setFocus()
            set_highlight(self.line_edit_lam2)
            set_bold(self.text_holder_label_lam2)
            return

        # lam2 sect.
        set_normal_style(self.line_edit_lam2, self.ss_line_edit_lam2)
        set_normal_font(self.text_holder_label_lam2)

        # ncpu sect.
        if self.line_edit_ncpus.text() == "":
            self.line_edit_ncpus.setText("1")

        # set parameters of astrosaber prep
        self.set_params()
        self.status_update()

        self.status_param = True

    def set_params(self):
        ###initialize training set preparation
        self.hisa = HisaExtraction(fitsfile=self.filename[0])

        ###you can adjust the number of cpus to use
        self.hisa.ncpus = int(self.line_edit_ncpus.text())

        ###smoothing phase and add residual
        if self.phase_toggle.isChecked():
            self.hisa.smoothing = "two"
        else:
            self.hisa.smoothing = "one"

        self.hisa.add_residual = self.addres_toggle.isChecked()

        ###set the initial guesses for the smoothing parameters (better to start low rather than high)
        self.hisa.lam1 = float(self.line_edit_lam1.text())
        self.hisa.lam2 = float(self.line_edit_lam2.text())

    def run_optimize(self):
        if self.status_param:
            self.hisa.saber()
            self.information_box()

    def status_update(self):
        # self.status_label.setAlignment(QtCore.Qt.AlignLeft)
        self.status_label.setText(
            f"Set noise to {float(self.line_edit_noise.text())}\nTwo-phase: {self.phase_toggle.isChecked()}, Add residual: {self.addres_toggle.isChecked()}\nSet \u03BB\u2081 to {float(self.line_edit_lam1.text())}, Set \u03BB\u2082 to {float(self.line_edit_lam2.text())}\nSet number of CPUs to {int(self.line_edit_ncpus.text())}"
        )

    def information_box(self):
        # show message box
        ret = self.message.exec()
        if ret == QMessageBox.Cancel:
            self.app.quit()
