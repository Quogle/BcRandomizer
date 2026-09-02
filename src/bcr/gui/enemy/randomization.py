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

class EnemyRandomization(QWidget):
    def refresh_from_config(self):
        self.random_type.setCurrentIndex(
            self.random_type.findText(
                self.config["enemy"]["randomization"]["type"]
            )
        )

    def __init__ (self, config):
        super().__init__()

        self.config = config

        # main layout 
        self.layout = QVBoxLayout(self)

        rando_config = self.config["enemy"]["randomization"]

        ########## Randomization Type ##################################################
        random_type_label = QLabel("Randomization Type")

        self.random_type = NoWheelQComboBox()
        self.random_type.addItems([
            "None",
            "ID Swap",
            "Fully Random",
        ])
        connect_combobox(
            self.random_type,
            rando_config,
            "type"
        )
        random_type_layout = QHBoxLayout()
        random_type_layout.addWidget(random_type_label)
        random_type_layout.addWidget(self.random_type)

        self.layout.addLayout(random_type_layout)

        # Keep Class

        self.keep_class = QCheckBox("Keep Class")
        connect_checkbox(
            self.keep_class,
            rando_config,
            "keep_class"
        )

        self.layout.addWidget(self.keep_class)

        # Variant Swap

        self.variant_swap = QCheckBox("Variant Swap")
        connect_checkbox(
            self.variant_swap,
            rando_config,
            "variant_swap"
        )

        self.layout.addWidget(self.variant_swap)

        # Adjust Magnifications

        self.adjust_magnifications = QCheckBox("Balance Magnifications")
        connect_checkbox(
            self.adjust_magnifications,
            rando_config,
            "adjust_magnifications"
        )

        self.layout.addWidget(self.adjust_magnifications)

        # Include Eoc

        self.include_eoc = QCheckBox("Include Eoc")
        connect_checkbox(
            self.include_eoc,
            rando_config,
            "include_eoc"
        )

        self.layout.addWidget(self.include_eoc)


        # Max ID

        max_id_layout = QHBoxLayout()
        max_id_label = QLabel("Max ID")

        self.max_id = NoWheelSpinBox()
        self.max_id.setMinimum(-1)
        self.max_id.setMaximum(9999)
        self.max_id.setSingleStep(1)
        connect_value(
            self.max_id,
            rando_config,
            "max_id"
        )

        max_id_layout.addWidget(max_id_label)
        max_id_layout.addWidget(self.max_id)

        self.layout.addLayout(max_id_layout)

