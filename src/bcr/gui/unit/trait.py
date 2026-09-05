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


class TraitRandomization(QWidget):
    def refresh_from_config(self):
        trait_config = self.config["unit"]["trait"]

        self.randomization_mode.setCurrentText(trait_config["randomization_mode"])
        self.vary_form_traits.setChecked(trait_config["vary_form_traits"])
        self.avoid_old_traits.setChecked(trait_config["avoid_old_traits"])

    def __init__(self, config):
        super().__init__()

        self.config = config

        # main layout
        self.layout = QVBoxLayout(self)

        trait_config = self.config["unit"]["trait"]


        # Randomization Type
        randomization_mode_layout = QHBoxLayout()
        randomization_mode_label = QLabel("Randomization Type")

        self.randomization_mode = NoWheelQComboBox()
        self.randomization_mode.addItems([
            "None",
            "Random",
            "Swap",
        ])
        connect_combobox(
            self.randomization_mode,
            trait_config,
            "randomization_mode"
        )

        randomization_mode_layout.addWidget(randomization_mode_label)
        randomization_mode_layout.addWidget(self.randomization_mode)

        self.layout.addLayout(randomization_mode_layout)

        # Vary Trait Target Per Form
        self.vary_form_traits = QCheckBox("Different Traits Per Form")
        connect_checkbox(
            self.vary_form_traits,
            trait_config,
            "vary_form_traits"
        )

        self.layout.addWidget(self.vary_form_traits)

        # Avoid Old Traits
        self.avoid_old_traits = QCheckBox("Avoid Old Traits")
        connect_checkbox(
            self.avoid_old_traits,
            trait_config,
            "avoid_old_traits"
        )

        self.layout.addWidget(self.avoid_old_traits)