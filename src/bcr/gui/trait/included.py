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


class IncludedTraits(QWidget):
    def refresh_from_config(self):
        ...
    
    def __init__(self, config):
        super().__init__()

        self.config = config

        # Main layout for trait gimmicks widget
        self.layout = QVBoxLayout(self)

        included_config = self.config["trait"]["included"]

        self.included = CheckboxGrid(
            included_config.items(),
            3,
            {name: name.title() for name in included_config}
        )

        connect_checkbox_grid(
            self.included,
            included_config
        )

        self.layout.addWidget(self.included)
