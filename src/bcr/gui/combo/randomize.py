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
        combo_config = self.config["catcombo"]
        randomize_config = self.config["catcombo"]["randomize"]
        self.enabled.setChecked(randomize_config["enabled"])
        self.units.setChecked(randomize_config["units"])
        self.mult.setChecked(randomize_config["mult"])
        self.effects.setChecked(randomize_config["effects"])
        self.allowed_abnormal_effects.setChecked(randomize_config["allowed_abnormal_effects"])
        self.max_uber_count.setValue(randomize_config["max_uber_count"])
        self.strength_of_downs.setValue(combo_config["strength_of_downs"])


    def __init__(self, config):
        super().__init__()

        self.config = config

        # main layout
        self.layout = QVBoxLayout(self)

        combo_config = self.config["catcombo"]
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

        # Randomize Combo Mult
        self.mult = QCheckBox("Randomize Multiplier")
        connect_checkbox(
            self.mult,
            randomize_config,
            "mult"
        )

        self.layout.addWidget(self.mult)

        # Randomize Combo Effects
        self.effects = QCheckBox("Randomize Effects")
        connect_checkbox(
            self.effects,
            randomize_config,
            "effects"
        )

        self.layout.addWidget(self.effects)

        # Allow abnormal effects
        self.allowed_abnormal_effects = QCheckBox("Include Abnormal Effects")
        connect_checkbox(
            self.allowed_abnormal_effects,
            randomize_config,
            "allowed_abnormal_effects"
        )

        self.layout.addWidget(self.allowed_abnormal_effects)


        # Uber+ Max Amount
        max_uber_count_layout = QHBoxLayout()
        max_uber_count_label = QLabel("Max Uber+ Units Per Combo")
        max_uber_count_label.setFixedWidth(200)

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

       # Strength of Down Combos
        strength_of_downs_label = QLabel("DOWN Combo Strength")
        strength_of_downs_label.setFixedWidth(200)

        self.strength_of_downs = NoWheelSpinBox()
        self.strength_of_downs.setRange(1, 100)
        self.strength_of_downs.setSuffix("%")

        connect_value(
            self.strength_of_downs,
            combo_config,
            "strength_of_downs"
        )

        strength_of_downs_layout = QHBoxLayout()
        strength_of_downs_layout.addWidget(strength_of_downs_label)
        strength_of_downs_layout.addWidget(self.strength_of_downs)

        self.layout.addLayout(strength_of_downs_layout)