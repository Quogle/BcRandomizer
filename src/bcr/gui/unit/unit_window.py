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
from .ability import AbilityRandomization
from .trait import TraitRandomization
from .talent import TalentRandomization

class UnitWindow(QWidget):
    def refresh_from_config(self):
        self.ability_randomization.refresh_from_config()
        self.trait_randomization.refresh_from_config()
        self.talent_randomization.refresh_from_config()

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

        ################ Ability Randomization ###########################################################################

        ability_randomization = QGroupBox("Ability Randomization")
        ability_randomization_layout = QVBoxLayout(ability_randomization)

        self.ability_randomization = AbilityRandomization(self.config)
        ability_randomization_layout.addWidget(self.ability_randomization)

        content_layout.addWidget(ability_randomization)

        ################ Trait Randomization ###########################################################################

        trait_randomization = QGroupBox("Trait Randomization")
        trait_randomization_layout = QVBoxLayout(trait_randomization)

        self.trait_randomization = TraitRandomization(self.config)
        trait_randomization_layout.addWidget(self.trait_randomization)

        content_layout.addWidget(trait_randomization)

        ################ Talent Randomization ###########################################################################

        talent_randomization = QGroupBox("Talent Randomization")
        talent_randomization_layout = QVBoxLayout(talent_randomization)

        self.talent_randomization = TalentRandomization(self.config)
        talent_randomization_layout.addWidget(self.talent_randomization)

        content_layout.addWidget(talent_randomization)