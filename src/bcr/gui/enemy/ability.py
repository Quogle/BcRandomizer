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
        ability_config = self.config["enemy"]["ability"]

        self.randomize_abilities.setChecked(ability_config["randomize_abilities"])
        self.min_abilities.setValue(ability_config["min_abilities"])

        for name, spinbox in self.ability_weights.items.items():
            spinbox.setValue(ability_config["weights"][name])

    def __init__ (self, config):
        super().__init__()

        self.config = config

        # main layout 
        self.layout = QVBoxLayout(self)

        ability_config = self.config["enemy"]["ability"]

        ##### Randomize Abilities ##################################################

        self.randomize_abilities = QCheckBox("Randomize Abilities")
        connect_checkbox(
            self.randomize_abilities,
            ability_config,
            "randomize_abilities"
        )

        self.layout.addWidget(self.randomize_abilities)

        # Minimum Abilities 
        min_abilities_layout = QHBoxLayout()
        min_abilities_label = QLabel("Minimum Ability Amount")

        self.min_abilities = NoWheelSpinBox()
        self.min_abilities.setMinimum(-1)
        self.min_abilities.setMaximum(99)
        self.min_abilities.setSingleStep(1)
        connect_value(
            self.min_abilities,
            ability_config,
            "min_abilities"
        )

        min_abilities_layout.addWidget(min_abilities_label)
        min_abilities_layout.addWidget(self.min_abilities)

        self.layout.addLayout(min_abilities_layout)

        # Ability Weights
        weights_label = QLabel("Ability Weights")
        weights_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            margin-top: 8px;
        """)
        self.layout.addWidget(weights_label)

        self.ability_weights = WeightedGrid(
            ability_config["weights"].items(),
            3,
            {
                name: name.replace("_", " ").title()
                for name in ability_config["weights"]
            }
        )

        connect_weighted_list(
            self.ability_weights,
            ability_config["weights"]
        )

        self.layout.addWidget(self.ability_weights)