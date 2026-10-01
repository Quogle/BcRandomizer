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

        # Limited Units
        self.limited = QCheckBox("Limited Time Units")
        connect_checkbox(
            self.limited,
            blacklist_config,
            "limited"
        )

        self.layout.addWidget(self.limited)