from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QGroupBox,
    QLabel,
    QComboBox,
    QCheckBox,
    QPushButton,
)
from PySide6.QtCore import Qt
from src.bcr.gui.themes.dark import DARK_THEME
from .randomize import ComboRandomization
from .blacklist import ComboBlacklist
from .size import ComboSize

class ComboWindow(QWidget):
    def refresh_from_config(self):
        self.combo_randomization.refresh_from_config()
        self.unit_blacklist.refresh_from_config()
        self.combo_size.refresh_from_config()

    def __init__(self, config):
        super().__init__()

        self.config = config

        self.setStyleSheet(DARK_THEME)

        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(16)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        ################ Combo Randomization ###########################################################################

        combo_randomization = QGroupBox("Combo Randomization")
        combo_randomization_layout = QVBoxLayout(combo_randomization)

        self.combo_randomization = ComboRandomization(self.config)
        combo_randomization_layout.addWidget(self.combo_randomization)

        content_layout.addWidget(combo_randomization)

        ################ Unit Blacklist ###########################################################################

        unit_blacklist = QGroupBox("Unit Blacklist")
        unit_blacklist_layout = QVBoxLayout(unit_blacklist)

        self.unit_blacklist = ComboBlacklist(self.config)
        unit_blacklist_layout.addWidget(self.unit_blacklist)

        content_layout.addWidget(unit_blacklist)

        ################ Combo Size Settings ###########################################################################

        combo_size = QGroupBox("Combo Size Settings")
        combo_size_layout = QVBoxLayout(combo_size)

        self.combo_size = ComboSize(self.config)
        combo_size_layout.addWidget(self.combo_size)

        content_layout.addWidget(combo_size)