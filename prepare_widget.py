from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QGridLayout,
    QSizePolicy,
    QMessageBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QProgressBar,
)

from PySide6 import QtCore
from validators import NumbersOnly, FloatsOnly
from custom_style import set_highlight, set_normal_style, set_bold, set_normal_font
from astrosaber.prepare_training import saberPrepare


class prepareWidget(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.filename = None

        # self.resize(self.sizeHint())

        # initialize info box
        self.message = QMessageBox()
        self.message.setMinimumSize(700, 200)
        self.message.setWindowTitle("Done!")
        infotext = "Preparation run was successful!"
        self.message.setText(infotext)
        # message.setInformativeText("Do you want to do something about it?")
        self.message.setIcon(QMessageBox.Information)
        self.message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.message.setDefaultButton(QMessageBox.Ok)
        self.message.button(QMessageBox.Ok).setText("Continue")
        self.message.button(QMessageBox.Cancel).setText("Quit")

        # status label
        self.status_label = QLabel("\n\n")
        self.status_param = False

        # file browser
        self.button_fb = QPushButton("Browse file")
        self.button_fb.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button_fb.clicked.connect(self.get_file_name)
        # self.text_holder_label_selected = QLabel("Selected file:")
        self.text_holder_label_dialog = QLabel("No file selected")
        self.text_holder_label_dialog.setWordWrap(True)

        # training set size field
        self.text_holder_label_training = QLabel("Training set size*")
        self.line_edit_training = QLineEdit(placeholderText="e.g. 100")
        self.line_edit_training.setValidator(NumbersOnly())
        # get style
        self.ss_line_edit_training = self.line_edit_training.styleSheet()
        # connect returnKey signal to slot
        self.line_edit_training.returnPressed.connect(self.validate_record)
        ###

        # noise field
        self.text_holder_label_noise = QLabel("Noise*")
        self.text_holder_label_noise.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_edit_noise = QLineEdit(placeholderText="e.g. 4.")
        self.line_edit_noise.setValidator(FloatsOnly())
        # get style
        self.ss_line_edit_noise = self.line_edit_noise.styleSheet()
        # connect returnKey signal to slot
        self.line_edit_noise.returnPressed.connect(self.validate_record)
        ###

        # linewidth field
        self.text_holder_label_lw = QLabel("Mean line width*")
        self.line_edit_lw = QLineEdit(placeholderText="e.g. 4.")
        self.line_edit_lw.setValidator(FloatsOnly())

        self.text_holder_label_lw_std = QLabel("Standard deviation")
        self.line_edit_lw_std = QLineEdit(placeholderText="e.g. 1.")
        self.line_edit_lw_std.setValidator(FloatsOnly())
        # get style
        self.ss_line_edit_lw = self.line_edit_lw.styleSheet()
        self.ss_line_edit_lw_std = self.line_edit_lw_std.styleSheet()
        # connect returnKey signal to slot
        self.line_edit_lw.returnPressed.connect(self.validate_record)
        self.line_edit_lw_std.returnPressed.connect(self.validate_record)
        ###

        # button to set params
        button_set_param = QPushButton("Set Parameters")
        button_set_param.clicked.connect(self.validate_record)

        # NEW Create a progress bar and a button and add them to the main layout
        self.progressBar = ProgressBar()
        self.progressBar.setRange(0, 1)

        # button to run prepare
        button_run_prepare = QPushButton("Prepare data")
        set_bold(button_run_prepare)
        button_run_prepare.clicked.connect(self.run_prepare)

        # Layouts
        layout = QGridLayout()
        # layout.addWidget(image_label, 0, 0, 1, 4)
        layout.addWidget(self.button_fb, 1, 0, 1, 1)
        layout.addWidget(self.text_holder_label_dialog, 1, 1, 1, 3)

        layout.addWidget(self.text_holder_label_training, 2, 0, 1, 1)
        layout.addWidget(self.line_edit_training, 2, 1, 1, 2)

        layout.addWidget(self.text_holder_label_noise, 3, 0, 1, 1)
        layout.addWidget(self.line_edit_noise, 3, 1, 1, 2)

        layout.addWidget(self.text_holder_label_lw, 4, 0, 1, 1)
        layout.addWidget(self.line_edit_lw, 4, 1, 1, 1)
        layout.addWidget(self.text_holder_label_lw_std, 4, 2, 1, 1)
        layout.addWidget(self.line_edit_lw_std, 4, 3, 1, 1)

        # set_param button
        layout.addWidget(button_set_param, 5, 1, 1, 2)
        # status label
        layout.addWidget(self.status_label, 6, 0, 1, 4)
        # NEW
        layout.addWidget(self.progressBar, 7, 0, 1, 4)
        # run_prepare button
        layout.addWidget(button_run_prepare, 8, 1, 1, 2)

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
            # set_bold(self.text_holder_label_selected)
            self.button_fb.setFocus()
            return

        # training sect.
        if self.line_edit_training.text() == "":
            self.status_label.setText("Missing required fields.")
            self.line_edit_training.setFocus()
            set_highlight(self.line_edit_training)
            set_bold(self.text_holder_label_training)
            return

        # training sect.
        set_normal_style(self.line_edit_training, self.ss_line_edit_training)
        set_normal_font(self.text_holder_label_training)

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

        # linewidth sect.
        if self.line_edit_lw.text() == "":
            self.status_label.setText("Missing required fields.")
            self.line_edit_lw.setFocus()
            set_highlight(self.line_edit_lw)
            set_bold(self.text_holder_label_lw)
            return

        # linewidth sect.
        set_normal_style(self.line_edit_lw, self.ss_line_edit_lw)
        set_normal_font(self.text_holder_label_lw)

        # lw std sect.
        if self.line_edit_lw_std.text() == "":
            self.line_edit_lw_std.setText("1.")

        # set parameters of astrosaber prep
        self.set_params()
        self.status_update()

        self.status_param = True

    def set_params(self):
        ###initialize training set preparation
        self.prep = saberPrepare(fitsfile=self.filename[0])

        ###set the size of the training set
        self.prep.training_set_size = int(self.line_edit_training.text())

        ###path to noise map (or universal noise value)
        # prep.path_to_noise_map = os.path.join('.', 'dir', 'sub', '*.fits')
        self.prep.noise = float(self.line_edit_noise.text())  # Kelvin

        ###set the expected linewidth of self-absorption features; artificial self-absorption features will be generated from this distribution
        self.prep.mean_linewidth = float(self.line_edit_lw.text())  # FWHM [km/s]
        self.prep.std_linewidth = float(
            self.line_edit_lw_std.text()
        )  # standard deviation of the linewidth distribution [km/s]

        # NEW
        self.myLongTask = TaskThread(self.prep)
        self.myLongTask.taskFinished.connect(self.onFinished)

    # def run_prepare(self):
    #    if self.status_param:
    #        self.status_label.setText("Preparation run in progress...")
    #        self.prep.prepare_training()
    #        self.information_box()
    # NEW
    def run_prepare(self):
        if self.status_param:
            self.progressBar.setRange(0, 0)
            self.status_label.setText("Preparation in progress...")
            self.myLongTask.start()

    # NEW
    def onFinished(self):
        # Stop the pulsation
        self.progressBar.setRange(0, 1)
        self.progressBar.setValue(1)
        self.status_label.setText("Finished!")
        self.information_box()

    def status_update(self):
        # self.status_label.setAlignment(QtCore.Qt.AlignLeft)
        self.status_label.setText(
            f"Set training data size to {int(self.line_edit_training.text())}\nSet noise to {float(self.line_edit_noise.text())}\nSet line width to {float(self.line_edit_lw.text())}"
            + "\u00b1"
            + f"{float(self.line_edit_lw_std.text())}"
        )

    def information_box(self):
        # show message box
        ret = self.message.exec()
        if ret == QMessageBox.Cancel:
            self.app.quit()


class TaskThread(QtCore.QThread):
    taskFinished = QtCore.Signal()

    def __init__(self, hisa_obj):
        super().__init__()
        self.hisa = hisa_obj

    def run(self):
        self.hisa.prepare_training()
        self.taskFinished.emit()


class ProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setRange(0, 0)
        # self.change_style()

    def change_style(self):
        css = """
            ::chunk{
                width: 50px;
            }
        """
        self.setStyleSheet(css)
