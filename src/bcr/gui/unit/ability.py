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


class AbilityRandomization(QWidget):
    def refresh_from_config(self):
        ability_config = self.config["unit"]["ability"]
        self.randomize_abilities.setChecked(ability_config["randomize"])

    def __init__(self, config):
        super().__init__()

        self.config = config

        # main layout
        self.layout = QVBoxLayout(self)
        main_layout = QHBoxLayout()
        checkbox_layout = QVBoxLayout()
        spinbox_layout = QVBoxLayout()

        ability_config = self.config["unit"]["ability"]

        # Random Abilities
        self.randomize_abilities = QCheckBox("Randomize Abilities")
        connect_checkbox(
            self.randomize_abilities,
            ability_config,
            "randomize"
        )

        checkbox_layout.addWidget(self.randomize_abilities)


        main_layout.addLayout(checkbox_layout, 1)
        main_layout.addLayout(spinbox_layout, 1)
        self.layout.addLayout(main_layout)