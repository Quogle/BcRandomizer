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
from ..trait.e_trait_gimmicks import TraitGimmicks
from ..trait.u_trait import TraitRandomization
from ..trait.u_ability import AbilityTraitRandomization
from ..trait.included import IncludedTraits

class TraitWindow(QWidget):
    def refresh_from_config(self):
        self.u_trait_randomization.refresh_from_config()
        self.e_trait_gimmicks.refresh_from_config()

    def __init__(self, config):
        super().__init__()

        self.config = config

        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(16)

        scroll.setWidget(content)

        main_layout.addWidget(scroll)

        ################ Included Traits ###########################################################################

        included = QGroupBox("Included Traits")
        included_layout = QVBoxLayout(included)

        self.included = IncludedTraits(self.config)
        included_layout.addWidget(self.included)

        content_layout.addWidget(included)

        ################ Unit Trait Randomization ###########################################################################

        u_trait_randomization = QGroupBox("Unit Trait Randomization")
        u_trait_randomization_layout = QVBoxLayout(u_trait_randomization)

        self.u_trait_randomization = TraitRandomization(self.config)
        u_trait_randomization_layout.addWidget(self.u_trait_randomization)

        content_layout.addWidget(u_trait_randomization)

        ################ Unit Trait Based Ability Randomization ###########################################################################

        u_ability_randomization = QGroupBox("Unit Trait Specific Abilities")
        u_ability_randomization_layout = QVBoxLayout(u_ability_randomization)

        self.u_ability_randomization = AbilityTraitRandomization(self.config)
        u_ability_randomization_layout.addWidget(self.u_ability_randomization)

        content_layout.addWidget(u_ability_randomization)

        ################ Enemy Trait Gimmicks  ###########################################################################

        e_trait_gimmicks = QGroupBox("Enemy Trait Gimmicks")
        e_trait_gimmicks_layout = QVBoxLayout(e_trait_gimmicks)

        self.e_trait_gimmicks = TraitGimmicks(self.config)
        e_trait_gimmicks_layout.addWidget(self.e_trait_gimmicks)

        content_layout.addWidget(e_trait_gimmicks)

