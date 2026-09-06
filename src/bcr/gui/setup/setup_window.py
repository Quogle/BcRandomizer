from PySide6.QtGui import QIntValidator
import random

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QPlainTextEdit,
    QProgressBar,
)

from PySide6.QtCore import Signal, QThread
from ..helpers.config_helpers import *
from .randomize_thread import RandomizeThread

class SetupWindow(QWidget):

    config_loaded = Signal()

    def __init__(self, config):
        super().__init__()

        self.config = config

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 18, 22, 22)
        layout.setSpacing(15)

        # Input APK
        input_layout = QHBoxLayout()

        input_label = QLabel("Input APK:")
        self.input_apk = QLineEdit()
        self.input_apk.setPlaceholderText("Select APK file...")
        input_button = QPushButton("Browse")

        input_button.clicked.connect(
            self.select_input_apk
        )

        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_apk)
        input_layout.addWidget(input_button)

        layout.addLayout(input_layout)

  
        # Config Laytout
        config_layout = QHBoxLayout()

        load_button = QPushButton("Load Config")
        save_button = QPushButton("Save Config")

        load_button.clicked.connect(
            self.load_configuration
        )

        save_button.clicked.connect(
            self.save_configuration
        )

        config_layout.addWidget(load_button)
        config_layout.addWidget(save_button)

        layout.addLayout(config_layout)

        randomizer_layout = QHBoxLayout()

        ######## SEED INPUT FIELD ############################################################################

        seed_label = QLabel("Seed:")
        self.seed = QLineEdit()
        self.seed.setValidator(QIntValidator(-2147483648, 2147483647))

        connect_line_edit(
            self.seed,
            self.config["mod"],
            "seed",
        )

        id_label = QLabel("Mod ID:")
        self.id = QLineEdit()

        connect_line_edit(
            self.id,
            self.config["mod"],
            "id",
        )

        randomize_button = QPushButton("Randomize")

        randomize_button.clicked.connect(
            self.randomize
        )

        randomizer_layout.addWidget(seed_label)
        randomizer_layout.addWidget(self.seed)
        randomizer_layout.addWidget(id_label)
        randomizer_layout.addWidget(self.id)

        layout.addLayout(randomizer_layout)
        layout.addWidget(randomize_button)

        # console
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)

        layout.addWidget(self.console)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        layout.addWidget(self.progress_bar)

        layout.addStretch()

    # APK Selection
    def select_input_apk(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select APK",
            "",
            "APK Files (*.apk)",
        )

        if path:
            self.input_apk.setText(path)

    # Config
    def save_configuration(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Configuration",
            "",
            "JSON Files (*.json)",
        )

        if path:
            save_config(
                self.config,
                path,
            )

    def load_configuration(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Configuration",
            "",
            "JSON Files (*.json)",
        )

        if path:
            loaded_config = load_config(path)
            update_config(self.config, loaded_config)

            self.seed.setText(
                "" if self.config["mod"]["seed"] is None
                else str(self.config["mod"]["seed"])
            )
            self.id.setText(self.config["mod"]["id"])

            self.config_loaded.emit()

    def log(self, message):
        self.console.appendPlainText(str(message))

    def randomize_finished(self):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)

    def randomize_error(self, message):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.log(f"ERROR: {message}")


    # Randomize Function 

    def randomize(self):

        self.progress_bar.setRange(0, 0)

        seed_text = self.seed.text().strip()

        if seed_text:
            seed = int(seed_text)
        else:
            seed = random.randint(
                -2147483648,
                2147483647,
            )

        self.config["mod"]["seed"] = seed
        self.seed.setText(str(seed))

        self.log(f"Seed: {seed}")

        apk_path = self.input_apk.text().strip()

        if not apk_path:
            self.randomize_error("No APK selected.")
            return

        self.thread = QThread(self)
        self.worker = RandomizeThread(
            apk_path,
            self.config.copy(),
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.log.connect(
            self.log
        )

        self.worker.finished.connect(
            self.randomize_finished
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.finished.connect(
            self.worker.deleteLater
        )

        self.worker.error.connect(
            self.randomize_error
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.start()