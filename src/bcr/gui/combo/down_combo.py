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


class AllDownCombo(QWidget):
    def refresh_from_config(self):
        down_config = self.config["catcombo"]["all_unit_down_combos"]
        self.enabled.setChecked(down_config["enabled"])
        self.include_abnormal_effects.setChecked(down_config["include_abnormal_effects"])
        self.strength.setValue(down_config["weaken_down_combos_by"])

    def __init__(self, config):
        super().__init__()

        self.config = config

        # main layout
        self.layout = QVBoxLayout(self)

        down_config = self.config["catcombo"]["all_unit_down_combos"]

        # enabled all unit DOWN combos
        self.enabled = QCheckBox("Enabled")
        connect_checkbox(
            self.enabled,
            down_config,
            "enabled"
        )

        self.layout.addWidget(self.enabled)


        # allow down combos to have abnormal effects
        self.include_abnormal_effects = QCheckBox("Include Abnormal Effects")
        connect_checkbox(
            self.include_abnormal_effects,
            down_config,
            "include_abnormal_effects"
        )

        self.layout.addWidget(self.include_abnormal_effects)

        # Strength of Down Combos
        strength_label = QLabel("DOWN Combo Strength")
        strength_label.setFixedWidth(200)

        self.strength = NoWheelSpinBox()
        self.strength.setRange(1, 100)
        self.strength.setSuffix("%")

        connect_value(
            self.strength,
            down_config,
            "weaken_down_combos_by"
        )

        strength_layout = QHBoxLayout()
        strength_layout.addWidget(strength_label)
        strength_layout.addWidget(self.strength)

        self.layout.addLayout(strength_layout)