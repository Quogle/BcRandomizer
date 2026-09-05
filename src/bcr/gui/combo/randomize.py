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


class ComboRandomization(QWidget):
    def refresh_from_config(self):
        randomize_config = self.config["catcombo"]["randomize"]
        self.enabled.setChecked(randomize_config["enabled"])
        self.units.setChecked(randomize_config["units"])
        self.multipliers.setChecked(randomize_config["multipliers"])
        self.effects.setChecked(randomize_config["effects"])
        self.max_uber_count.setValue(randomize_config["max_uber_count"])

    def __init__(self, config):
        super().__init__()

        self.config = config

        # main layout
        self.layout = QVBoxLayout(self)

        randomize_config = self.config["catcombo"]["randomize"]

        # Enable Randomization
        self.enabled = QCheckBox("Enabled")
        connect_checkbox(
            self.enabled,
            randomize_config,
            "enabled"
        )

        self.layout.addWidget(self.enabled)

        # Randomize Combo Units
        self.units = QCheckBox("Randomize Units")
        connect_checkbox(
            self.units,
            randomize_config,
            "units"
        )

        self.layout.addWidget(self.units)

        # Randomize Combo Multipliers
        self.multipliers = QCheckBox("Randomize Multipliers")
        connect_checkbox(
            self.multipliers,
            randomize_config,
            "multipliers"
        )

        self.layout.addWidget(self.multipliers)

        # Randomize Combo Effects
        self.effects = QCheckBox("Randomize Effects")
        connect_checkbox(
            self.effects,
            randomize_config,
            "effects"
        )

        self.layout.addWidget(self.effects)

        # Uber+ Max Amount
        max_uber_count_layout = QHBoxLayout()
        max_uber_count_label = QLabel("Maximum Uber+ Units Per Combo")

        self.max_uber_count = NoWheelSpinBox()
        self.max_uber_count.setMinimum(0)
        self.max_uber_count.setMaximum(5)
        connect_value(
            self.max_uber_count,
            randomize_config,
            "max_uber_count"
        )

        max_uber_count_layout.addWidget(max_uber_count_label)
        max_uber_count_layout.addWidget(self.max_uber_count)
        self.layout.addLayout(max_uber_count_layout)