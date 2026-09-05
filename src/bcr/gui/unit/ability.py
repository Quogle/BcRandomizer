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
        self.grant_trait_abilities.setChecked(ability_config["grant_trait_abilities"])
        self.remove_trait_abilities.setChecked(ability_config["remove_trait_abilities"])
        self.zkill_frequency.setValue(ability_config["zkill_frequency"])
        self.shield_pierce_frequency.setValue(ability_config["shield_pierce_frequency"])
        self.curse_immune_frequency.setValue(ability_config["curse_immune_frequency"])

    def __init__(self, config):
        super().__init__()

        self.config = config

        # main layout
        self.layout = QVBoxLayout(self)

        ability_config = self.config["unit"]["ability"]

        # Random Abilities
        self.randomize_abilities = QCheckBox("Randomize Abilities")
        connect_checkbox(
            self.randomize_abilities,
            ability_config,
            "randomize"
        )

        self.layout.addWidget(self.randomize_abilities)

        # Trait Specific Abilities
        self.grant_trait_abilities = QCheckBox("Grant Abilities Based on Target Trait")
        connect_checkbox(
            self.grant_trait_abilities,
            ability_config,
            "grant_trait_abilities"
        )

        self.layout.addWidget(self.grant_trait_abilities)

        # Remove Trait Specific Abilities
        self.remove_trait_abilities = QCheckBox("Remove Abilities Based on Target Trait")
        connect_checkbox(
            self.remove_trait_abilities,
            ability_config,
            "remove_trait_abilities"
        )

        # Z Kill Frequency
        self.layout.addWidget(self.remove_trait_abilities)

        zkill_frequency_layout = QHBoxLayout()
        zkill_frequency_label = QLabel("Z Kill Frequency")

        self.zkill_frequency = NoWheelSpinBox()
        self.zkill_frequency.setMinimum(0)
        self.zkill_frequency.setMaximum(100)
        connect_value(
            self.zkill_frequency,
            ability_config,
            "zkill_frequency"
        )

        zkill_frequency_layout.addWidget(zkill_frequency_label)
        zkill_frequency_layout.addWidget(self.zkill_frequency)
        self.layout.addLayout(zkill_frequency_layout)

        # Shield Pierce Frequency
        shield_pierce_frequency_layout = QHBoxLayout()
        shield_pierce_frequency_label = QLabel("Shield Pierce Frequency")

        self.shield_pierce_frequency = NoWheelSpinBox()
        self.shield_pierce_frequency.setMinimum(0)
        self.shield_pierce_frequency.setMaximum(100)
        connect_value(
            self.shield_pierce_frequency,
            ability_config,
            "shield_pierce_frequency"
        )

        shield_pierce_frequency_layout.addWidget(shield_pierce_frequency_label)
        shield_pierce_frequency_layout.addWidget(self.shield_pierce_frequency)
        self.layout.addLayout(shield_pierce_frequency_layout)


        # Curse Immune Frequency
        curse_immune_frequency_layout = QHBoxLayout()
        curse_immune_frequency_label = QLabel("Curse Immune Frequency")

        self.curse_immune_frequency = NoWheelSpinBox()
        self.curse_immune_frequency.setMinimum(0)
        self.curse_immune_frequency.setMaximum(100)
        connect_value(
            self.curse_immune_frequency,
            ability_config,
            "curse_immune_frequency"
        )

        curse_immune_frequency_layout.addWidget(curse_immune_frequency_label)
        curse_immune_frequency_layout.addWidget(self.curse_immune_frequency)
        self.layout.addLayout(curse_immune_frequency_layout)