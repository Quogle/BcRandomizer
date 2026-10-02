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
from ..helpers.widgets import *
from .randomize_thread import RandomizeThread
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
from .versions import Versions

class SetupWindow(QWidget):

    config_loaded = Signal()

    def __init__(self, config, menu_buttons):
        super().__init__()

        self.config = config
        self.menu_buttons = menu_buttons

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(22, 18, 22, 22)
        main_layout.setSpacing(15)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        main_layout.addLayout(layout)

        right_layout = QVBoxLayout()
        self.versions = Versions(self.config)
        right_layout.addWidget(self.versions)
        right_layout.addStretch()

        main_layout.addLayout(right_layout)

        main_layout.setStretch(0, 9)
        main_layout.setStretch(1, 3)

        # Input APK
        input_layout = QHBoxLayout()

        self.input_label = QLabel("Input APK:")
        self.input_apk = QLineEdit()
        self.input_apk.setPlaceholderText("Select APK file...")
        self.input_button = QPushButton("Browse")

        self.input_button.clicked.connect(
            self.select_input_apk
        )

        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_apk)
        input_layout.addWidget(self.input_button)

        layout.addLayout(input_layout)

  
        # Config Laytout
        config_layout = QHBoxLayout()

        self.load_button = QPushButton("Load Config")
        self.save_button = QPushButton("Save Config")

        self.load_button.clicked.connect(
            self.load_configuration
        )

        self.save_button.clicked.connect(
            self.save_configuration
        )

        config_layout.addWidget(self.load_button)
        config_layout.addWidget(self.save_button)

        layout.addLayout(config_layout)

        # SEED INPUT FIELD 

        self.seed_label = QLabel("Seed:")
        self.seed = QLineEdit()
        self.seed.setValidator(QIntValidator(-2147483648, 2147483647))

        connect_line_edit(
            self.seed,
            self.config["mod"],
            "seed",
        )

        # ID INPUT ####

        self.id_label = QLabel("Mod ID:")
        self.id = QLineEdit()

        self.id.setValidator(QRegularExpressionValidator(QRegularExpression(r"\S*")))

        connect_line_edit(
            self.id,
            self.config["mod"],
            "id",
        )

        # Randomize Button
        self.randomize_button = QPushButton("Randomize")

        self.randomize_button.clicked.connect(
            self.randomize
        )

        randomizer_layout = QHBoxLayout()
        randomizer_layout.addWidget(self.seed_label)
        randomizer_layout.addWidget(self.seed)
        randomizer_layout.addWidget(self.id_label)
        randomizer_layout.addWidget(self.id)


        layout.addLayout(randomizer_layout)
        layout.addWidget(self.randomize_button)

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
            
            self.versions.unit_version.setText(
                "" if self.config["mod"]["unit_version"] is None
                else str(self.config["mod"]["unit_version"])
            )

            self.versions.enemy_version.setText(
                "" if self.config["mod"]["enemy_version"] is None
                else str(self.config["mod"]["enemy_version"])
            )

            self.versions.talent_version.setText(
                "" if self.config["mod"]["talent_version"] is None
                else str(self.config["mod"]["talent_version"])
            )

            self.config_loaded.emit()

    def log(self, message):
        self.console.appendPlainText(str(message))

    def randomize_finished(self):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)

        self.set_ui_enabled(True)

    def randomize_error(self, message):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.set_ui_enabled(True)

        message = message.replace("\n", "<br>")

        self.console.appendHtml(
            f'<span style="color: red;">ERROR: {message}</span>'
        )


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

        self.set_ui_enabled(False)

        self.thread = QThread(self)
        self.worker = RandomizeThread(
            apk_path,
            self.config.copy(),
        )

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.log.connect(self.log)
        self.worker.html_log.connect(self.console.appendHtml)
        self.worker.finished.connect(self.randomize_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.randomize_error)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def set_ui_enabled(self, enabled):
        for button in self.menu_buttons:
            button.setEnabled(enabled)

        self.input_apk.setEnabled(enabled)
        self.seed.setEnabled(enabled)
        self.id.setEnabled(enabled)
        self.randomize_button.setEnabled(enabled)
        self.versions.setEnabled(enabled)
        self.save_button.setEnabled(enabled)
        self.load_button.setEnabled(enabled)
        self.input_button.setEnabled(enabled)
        self.input_label.setEnabled(enabled)
        self.id_label.setEnabled(enabled)
        self.seed_label.setEnabled(enabled)
