from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QCheckBox,
    QPushButton,
)

MULT_NAMES = {
    "sm": "SM",
    "m": "M",
    "L": "L",
    "xl": "XL",
    "down": "DOWN"
}

from PySide6.QtCore import Qt

from ..helpers.widgets import *
from ..helpers.config_helpers import *


class ComboSize(QWidget):
    def refresh_from_config(self):
        size_config = self.config["catcombo"]["size"]
        self.keep_unit_count.setChecked(size_config["keep_unit_count"])

        for name, spinbox in self.size_weights.items.items():
            spinbox.setValue(size_config["custom_count_weights"][name])

        for size, weights in size_config["custom_mult_weights"].items():
            mult_weights = self.mult_weights[size]
            
            for name, spinbox in mult_weights.items.items():
                spinbox.setValue(weights[name])

    def __init__(self, config):
        super().__init__()

        self.config = config

        # main layout
        self.layout = QVBoxLayout(self)

        size_config = self.config["catcombo"]["size"]

        # Unit Count
        self.keep_unit_count = QCheckBox("Keep Unit Count")
        connect_checkbox(
            self.keep_unit_count,
            size_config,
            "keep_unit_count"
        )

        self.layout.addWidget(self.keep_unit_count)

        # Size Weights
        size_weights_label = QLabel("Size Weights")
        size_weights_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            margin-top: 8px;
        """)
        self.layout.addWidget(size_weights_label)

        self.size_weights = WeightedGrid(
            size_config["custom_count_weights"].items(),
            columns=5,
        )

        connect_weighted_list(
            self.size_weights,
            size_config["custom_count_weights"]
        )

        self.layout.addWidget(self.size_weights)


        # Mult Weights
        mult_weights_label = QLabel("Multiplier Weights")
        mult_weights_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            margin-top: 8px;
        """)
        self.layout.addWidget(mult_weights_label)

        self.mult_weights = {}

        for size, weights in size_config["custom_mult_weights"].items():
            size_layout = QHBoxLayout()

            size_label = QLabel(f"{size} Unit Combo")

            mult_weights = WeightedGrid(
                weights.items(),
                columns=5,
                names=MULT_NAMES
            )

            connect_weighted_list(
                mult_weights,
                weights
            )

            self.mult_weights[size] = mult_weights

            size_layout.addWidget(size_label)
            size_layout.addWidget(mult_weights)

            self.layout.addLayout(size_layout)