from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QCheckBox,
    QPushButton,
)

from PySide6.QtCore import Qt

from ..helpers.widgets import *
from ..helpers.config_helpers import *


class ComboBlacklist(QWidget):
    def refresh_from_config(self):
        blacklist_config = self.config["catcombo"]["blacklist"]
        self.collab.setChecked(blacklist_config["collab"])
        self.version_exclusive.setChecked(blacklist_config["version_exclusive"])
        self.unobtainable.setChecked(blacklist_config["unobtainable"])
        self.limited.setChecked(blacklist_config["limited"])

    def __init__(self, config):
        super().__init__()

        self.config = config

        # main layout
        self.layout = QVBoxLayout(self)

        blacklist_config = self.config["catcombo"]["blacklist"]

        # Collab
        self.collab = QCheckBox("Collab Units")
        connect_checkbox(
            self.collab,
            blacklist_config,
            "collab"
        )

        self.layout.addWidget(self.collab)

        # Version Exclusive
        self.version_exclusive = QCheckBox("Version Exclusives")
        connect_checkbox(
            self.version_exclusive,
            blacklist_config,
            "version_exclusive"
        )

        self.layout.addWidget(self.version_exclusive)

        # Unobtainable Units
        self.unobtainable = QCheckBox("Unobtainable Units")
        connect_checkbox(
            self.unobtainable,
            blacklist_config,
            "unobtainable"
        )

        self.layout.addWidget(self.unobtainable)

        # Limited Units
        self.limited = QCheckBox("Limited Time Units")
        connect_checkbox(
            self.limited,
            blacklist_config,
            "limited"
        )

        self.layout.addWidget(self.limited)